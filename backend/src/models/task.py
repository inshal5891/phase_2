from sqlmodel import Field, Relationship
from .sqlmodel_base import SQLModel
from typing import Optional
from datetime import datetime
from .user import User

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id")


class Task(TaskBase, table=True):
    """
    Task entity representing a todo item with attributes including ID, title,
    description, completion status, and creation timestamp.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: Optional[User] = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(SQLModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None


class TaskRead(TaskBase):
    """Schema for reading task data."""
    id: int
    created_at: datetime
    user: Optional["User"] = None

    @classmethod
    def from_orm(cls, obj):
        """Convert from ORM object to Pydantic model."""
        return cls(
            title=obj.title,
            description=obj.description,
            completed=obj.completed,
            user_id=obj.user_id,
            id=obj.id,
            created_at=obj.created_at,
            user=obj.user
        )