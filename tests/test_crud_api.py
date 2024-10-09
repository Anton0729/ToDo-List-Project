from fastapi.testclient import TestClient

from app.main import app
from tests.conftest import create_user, create_task

client = TestClient(app)


def test_read_users_tasks_successfully(create_user, create_task):
    """
    Test case to read user's tasks successfully.
    """
    task = create_task
    response = client.get("/tasks/", headers={"Authorization": f"Bearer {create_user}"})

    assert response.status_code == 200
    assert (el["id"] == task["id"] for el in response.json())  # Check that user has created task
    assert (el["user_id"] == task["user_id"] for el in
            response.json())  # Check that created and received task belongs to one user


def test_read_users_tasks_unsuccessfully(create_user):
    """
    Test case to read user's tasks unsuccessfully.
    """

    response = client.get("/tasks/", headers={"Authorization": f"Bearer {create_user}"})
    assert response.status_code == 404


def test_read_specific_task(create_user, create_task):
    """
    Test case to reading task by its ID.
    """
    task = create_task
    task_id = task["id"]
    response = client.get(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {create_user}"})

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == task["title"]
    assert response.json()["description"] == task["description"]


def test_read_all_tasks(create_user):
    """
    Test case for reading all tasks with pagination and optional status filtering.
    """
    user = create_user
    # Create a few tasks for testing
    tasks_to_create = [
        {"title": "Task 1", "description": "This is task 1.", "status": "New"},
        {"title": "Task 2", "description": "This is task 2.", "status": "In Progress"},
        {"title": "Task 3", "description": "This is task 3.", "status": "Completed"},
    ]

    for task_data in tasks_to_create:
        client.post(
            "/tasks/",
            json=task_data,
            headers={"Authorization": f"Bearer {user}"}
        )

    response = client.get("/tasks/all", headers={"Authorization": f"Bearer {user}"})
    assert response.status_code == 200

    # Test with status filter
    response_filtered = client.get("/tasks/all?page=1&size=2&status=New", headers={"Authorization": f"Bearer {user}"})
    assert response_filtered.status_code == 200
    assert len(response_filtered.json()["tasks"]) == 1
    assert response_filtered.json()["tasks"][0]["title"] == "Task 1"


def test_read_all_tasks_no_tasks_found(create_user):
    """
    Test case for read_all_tasks raising 404 if no tasks are found.
    """
    user = create_user
    response = client.get("/tasks/all", headers={"Authorization": f"Bearer {user}"}, params={"page": 1, "size": 10})

    assert response.status_code == 404
    assert response.json()["detail"] == "No tasks found"


def test_update_task_successfully(create_user, create_task):
    """
    Test case for updating a task by its ID successfully.
    """
    user = create_user
    task = create_task
    task_id = task["id"]

    updated_data = {
        "title": "Updated Task",
        "description": None,
        "status": "Completed"
    }

    response = client.put(f"/tasks/{task_id}", json=updated_data, headers={"Authorization": f"Bearer {user}"})

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["status"] == "Completed"


def test_update_task_unauthorized(create_task, create_user):
    """
    Test case for updating a task by its ID unauthorized.
    """
    task = create_task
    task_id = task["id"]

    updated_data = {
        "title": "Updated Task",
        "description": None,
        "status": "Completed"
    }

    response = client.put(f"/tasks/{task_id}", json=updated_data)

    assert response.status_code == 401


def test_delete_task_successfully(create_task, create_user):
    """
    Test case for deleting a task by its ID successfully.
    """
    user = create_user
    task = create_task
    task_id = task["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user}"}
    )

    assert response.status_code == 200


def test_delete_task_unauthorized(create_task, create_user):
    """
    Test case for deleting a task by its ID unauthorized.
    """
    task = create_task
    task_id = task["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 401


def test_mark_task_as_completed(create_task, create_user):
    """
    Test case for marking a task as completed by its ID.
    """
    user = create_user
    task = create_task
    task_id = task["id"]

    response = client.put(
        f"/tasks/{task_id}/complete",
        headers={"Authorization": f"Bearer {user}"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Completed"
