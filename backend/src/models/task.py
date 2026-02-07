from sqlmodel import Field, Relationship
from .sqlmodel_base import SQLModel
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from .user import User

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: Optional[TaskPriority] = Field(default=TaskPriority.medium)
    due_date: Optional[datetime] = Field(default=None)
    user_id: int = Field(foreign_key="user.id")


class Task(TaskBase, table=True):
    """
    Task entity representing a todo item with attributes including ID, title,
    description, completion status, priority, due date, and creation timestamp.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")


class TaskCreate(SQLModel):
    """Schema for creating a new task. user_id is extracted from JWT token."""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: Optional[TaskPriority] = Field(default=TaskPriority.medium)
    due_date: Optional[datetime] = Field(default=None)


class TaskUpdate(SQLModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None


class TaskRead(TaskBase):
    """Schema for reading task data."""
    id: int
    created_at: datetime