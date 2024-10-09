from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi_pagination import add_pagination

from sqlalchemy.orm import selectinload, Session
from sqlalchemy.future import select

from typing import Optional

from app.dependencies import get_db
from app.models import Task, User, TaskStatusEnum
from app.models import User as UserModel
from app.schemas import TaskResponse, TaskCreate, AllTasksResponse, TaskUpdate
from auth.dependencies import get_current_user
from auth.routes import router as auth_router

app = FastAPI(
    title="To-Do List"
)

# Include authentication routes from the auth module
app.include_router(auth_router, prefix="/auth", tags=["auth"])


def get_user_or_404(user_id: int, session: Session):
    result = session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def get_task_or_404(task_id: int, session: Session):
    query = select(Task).where(Task.id == task_id)
    result = session.execute(query)
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# Endpoint to get all user's tasks with pagination
@app.get("/tasks/", response_model=AllTasksResponse, status_code=200)
def read_users_tasks(
        session: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user),
        page: int = Query(1, ge=1),  # Page number, default is 1
        size: int = Query(10, ge=1, le=100),  # Page size, default is 10, max 100
):
    """
    Retrieve a paginated list of user's tasks.

    - **page**: Page number to retrieve (default is 1).
    - **size**: Number of tasks per page (default is 10, max 100).
    """
    offset = (page - 1) * size  # Calculate the offset for pagination
    query = select(Task).where(Task.user_id == current_user.id).options(selectinload(Task.user)).offset(offset).limit(
        size)

    result = session.execute(query)
    tasks = result.scalars().all()

    # If not tasks are found, raise error
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")

    # Transform tasks to TaskResponse
    task_responses = []
    for task in tasks:
        task_responses.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "user_id": task.user_id,
                "status": task.status,
            }
        )

    # Build pagination info
    pagination_info = {
        "page": page,
        "size": size,
        "total": len(tasks),
    }

    return {
        "pagination": pagination_info,
        "tasks": task_responses,
    }


# Endpoint to get all tasks with pagination and optional status filtering
@app.get("/tasks/all", response_model=AllTasksResponse, status_code=200)
def read_all_tasks(
        session: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user),
        page: int = Query(1, ge=1),  # Page number, default is 1
        size: int = Query(10, ge=1, le=100),  # Page size, default is 10, max 100
        status: Optional[TaskStatusEnum] = Query(None)  # Optional status filter
):
    """
    Retrieve a paginated list of tasks, optionally filtered by status.

    - **page**: Page number to retrieve (default is 1).
    - **size**: Number of tasks per page (default is 10, max 100).
    - **status**: Optional status filter ('New', 'In progress', 'Completed').
    """
    offset = (page - 1) * size  # Calculate the offset for pagination

    # Build the base query
    query = select(Task).options(selectinload(Task.user)).offset(offset).limit(size)

    # Add status filter if provided
    if status:
        query = query.where(Task.status == status)

    result = session.execute(query)
    tasks = result.scalars().all()

    # If no tasks are found, raise error
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")

    # Transform tasks to TaskResponse
    task_responses = []
    for task in tasks:
        task_responses.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "user_id": task.user_id,
                "status": task.status,
            }
        )

    # Build pagination info
    pagination_info = {
        "page": page,
        "size": size,
        "total": len(tasks),
    }

    return {
        "pagination": pagination_info,
        "tasks": task_responses,
    }


# Endpoint to get a specific task by ID
@app.get("/tasks/{task_id}", response_model=TaskResponse, status_code=200)
def read_task(
        task_id: int,
        session: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user),
):
    """
    Retrieve information about a specific task by its ID.

    - **task_id**: ID of the task to retrieve.
    """
    task = get_task_or_404(task_id, session)

    return task


# Endpoint to create a new task
@app.post("/tasks/", response_model=TaskResponse, status_code=201)
def create_task(
        task_create: TaskCreate,
        session: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user),
):
    """
    Create a new task.

     **Request Body:**

    - **title** (string): The title of the task.
    - **description** (string): The description of the task
    - **user_id** (integer): The ID of the user responsible for the task.
    - **status** (string): The status of the task. Valid values are "New", "In progress", "Completed".

    **Example Request Body:**

    ```json
    {
      "title": "Fix login bug",
      "description": "",
      "status": "New",
    }
    ```
    """

    # Create new task
    new_task = Task(
        title=task_create.title,
        description=task_create.description,
        user_id=current_user.id,
        status=task_create.status,
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)  # Refresh the task to get the updated values

    return new_task


# Endpoint to update task. Can be updated only by owner
@app.put("/tasks/{task_id}", response_model=TaskResponse, status_code=200)
def update_task(
        task_id: int,
        task_update: TaskUpdate,
        session: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user),
):
    """
    Update information about a specific task by its ID. Can be updated only by owner.

    - **task_id**: ID of the task to update.
    - **title** (string): The title of the task.
    - **description** (string): The description of the task
    - **status** (string): The status of the task. Valid values are "New", "In progress", "Completed".
    """
    task = get_task_or_404(task_id, session)

    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to update this task.")

    # Update the task with the provided data
    if task_update.title is not None:
        task.title = task_update.title
    task.description = task_update.description
    task.status = task_update.status

    session.commit()
    session.refresh(task)  # Refresh the task to get the updated values

    return task


# Endpoint to delete task. Can be deleted only by owner
@app.delete("/tasks/{task_id}", response_model=dict, status_code=200)
def delete_task(
        task_id: int,
        session: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user),
):
    """
    Delete a task by its ID. Can be deleted only by owner

    - **task_id**: ID of the task to delete.
    """
    task = get_task_or_404(task_id, session)

    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this task.")

    session.delete(task)
    session.commit()

    return {"detail": "Task deleted successfully"}


# Endpoint for marking a task as completed
@app.put("/tasks/{task_id}/complete", response_model=TaskResponse, status_code=200)
def mark_task_as_completed(
        task_id: int,
        session: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user),
):
    """
    Mark a task completed by its ID. Can be changed only by owner

    - **task_id**: ID of the task to delete.
    """
    task = get_task_or_404(task_id, session)

    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to change status of this task.")

    task.status = TaskStatusEnum.COMPLETED

    session.commit()
    session.refresh(task)
    return task


add_pagination(app)
