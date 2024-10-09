import enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Enum
from .database import Base


class TaskStatusEnum(enum.Enum):
    NEW = "New"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Correct relationship to tasks
    tasks = relationship("Task", back_populates="user", cascade="all, delete", lazy="selectin")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatusEnum, name="status_task"), nullable=False, default=TaskStatusEnum.NEW)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Correct relationship to user (owner of a task)
    user = relationship("User", back_populates="tasks", lazy="selectin")
