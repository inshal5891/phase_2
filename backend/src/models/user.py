from sqlmodel import Field, Relationship
from .sqlmodel_base import SQLModel
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .task import Task

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)


class User(UserBase, table=True):
    """
    User entity representing a registered user with authentication-specific fields
    in addition to the original user context from Spec 1.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)  # BCrypt hashed password
    is_active: bool = Field(default=True)  # Account status flag
    email_verified: bool = Field(default=False)  # Email verification status
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = Field(default=None)  # Timestamp of last successful login

    # Relationship to tasks
    tasks: list["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str


class UserRegister(UserBase):
    """Schema for user registration."""
    password: str


class UserLogin(SQLModel):
    """Schema for user login."""
    email: str
    password: str


class UserRead(UserBase):
    """Schema for reading user data without sensitive information."""
    id: int
    is_active: bool
    email_verified: bool
    created_at: datetime
    last_login: Optional[datetime]


class UserUpdate(SQLModel):
    """Schema for updating user information."""
    email: Optional[str] = None
    is_active: Optional[bool] = None
    email_verified: Optional[bool] = None


class UserPublic(UserBase):
    """Public representation of user (without sensitive data)."""
    id: int
    is_active: bool
    email_verified: bool
    created_at: datetime

    @classmethod
    def from_orm(cls, obj):
        """Convert from ORM object to Pydantic model."""
        return cls(
            email=obj.email,
            id=obj.id,
            is_active=obj.is_active,
            email_verified=obj.email_verified,
            created_at=obj.created_at
        )