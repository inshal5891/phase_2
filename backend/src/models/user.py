from sqlmodel import Field
from .sqlmodel_base import SQLModel
from typing import Optional
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)


class User(UserBase, table=True):
    """
    User entity representing a logical user context for organizing tasks.
    Note: Authentication/authorization is deferred to Spec 2;
    currently only used for data isolation.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    """Schema for creating a new user."""
    pass


class UserRead(UserBase):
    """Schema for reading user data without sensitive information."""
    id: int
    created_at: datetime