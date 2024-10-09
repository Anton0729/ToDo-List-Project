from typing import Optional, List
from pydantic import BaseModel, constr
from app.models import TaskStatusEnum


# Base User Schema
class UserBase(BaseModel):
    username: str


# Schema for User Creation (Signup)
class UserCreate(UserBase):
    first_name: str
    last_name: Optional[str] = None  # Make last_name optional if needed
    password: constr(min_length=6)


# Response Schema for User Details
class UserResponse(UserBase):
    id: int
    first_name: str
    last_name: Optional[str] = None  # last_name can be optional in the response

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: constr(min_length=1)  # Title must be a non-empty string
    description: Optional[str] = None
    status: TaskStatusEnum


class TaskCreate(TaskBase):
    status: TaskStatusEnum = TaskStatusEnum.NEW


class TaskUpdate(BaseModel):
    title: constr(min_length=1)  # Title must be a non-empty string
    description: Optional[str]
    status: TaskStatusEnum


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatusEnum
    user_id: int

    class Config:
        from_attributes = True


class PaginationInfo(BaseModel):
    page: int
    size: int
    total: int


class AllTasksResponse(BaseModel):
    pagination: PaginationInfo
    tasks: List[TaskResponse]
