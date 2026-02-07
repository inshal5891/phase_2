from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
from ..database.session import get_session
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..services.task_service import TaskService
from ..models.user import User, UserRegister, UserLogin, UserPublic
from ..services.user_service import UserService
from ..auth.security import create_access_token, get_current_user_from_header
from datetime import timedelta
import os

router = APIRouter(prefix="/api", tags=["tasks", "auth"])

# Authentication endpoints
@router.post("/auth/register", response_model=UserPublic, status_code=201)
def register_user(
    user_data: UserRegister,
    session: Session = Depends(get_session)
):
    """
    Register a new user account.

    Args:
        user_data: User registration data (email and password)
        session: Database session dependency

    Returns:
        Created user information (public fields only)
    """
    # Check if user already exists
    existing_user = UserService.get_user_by_email(session, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    try:
        user = UserService.create_user(session, user_data)
        return UserPublic.from_orm(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}"
        )


@router.post("/auth/login")
def login_user(
    user_credentials: UserLogin,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return JWT token.

    Args:
        user_credentials: User login data (email and password)
        session: Database session dependency

    Returns:
        Access token and user information
    """
    user = UserService.authenticate_user(session, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT access token
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")))
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )

    # Update last login time
    UserService.update_user_last_login(session, user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserPublic.from_orm(user)
    }


@router.get("/auth/me", response_model=UserPublic)
def get_current_user(
    current_user: User = Depends(get_current_user_from_header)
):
    """
    Get information about the currently authenticated user.

    Args:
        current_user: The authenticated user (extracted from JWT token)

    Returns:
        Current user information (public fields only)
    """
    return UserPublic.from_orm(current_user)


# Protected task endpoints (require authentication)
@router.get("/tasks")
def get_tasks(
    current_user: User = Depends(get_current_user_from_header),
    completed: Optional[bool] = None,
    session: Session = Depends(get_session)
):
    """
    Retrieve a list of all tasks for the authenticated user.

    Args:
        current_user: The authenticated user (extracted from JWT token)
        completed: Optional filter for completion status
        session: Database session dependency

    Returns:
        List of Task objects for the authenticated user
    """
    tasks = TaskService.get_tasks_by_user(session, current_user.id, completed)
    # Return as dictionaries to bypass Pydantic serialization issues
    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "user_id": task.user_id,
            "created_at": task.created_at.isoformat()
        }
        for task in tasks
    ]


@router.post("/tasks", response_model=TaskRead, status_code=201)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user_from_header),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Args:
        task_data: Task creation data
        current_user: The authenticated user (extracted from JWT token)
        session: Database session dependency

    Returns:
        Created Task object
    """
    try:
        # Add user_id to the task data to associate it with the authenticated user
        task = TaskService.create_task_for_user(session, task_data, current_user.id)
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating task: {str(e)}")


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user_from_header),
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific task by its ID (must belong to authenticated user).

    Args:
        task_id: The ID of the task to retrieve
        current_user: The authenticated user (extracted from JWT token)
        session: Database session dependency

    Returns:
        Task object
    """
    task = TaskService.get_task_by_id(session, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or does not belong to user")
    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user_from_header),
    session: Session = Depends(get_session)
):
    """
    Update an existing task (must belong to authenticated user).

    Args:
        task_id: The ID of the task to update
        task_update: Task update data
        current_user: The authenticated user (extracted from JWT token)
        session: Database session dependency

    Returns:
        Updated Task object
    """
    task = TaskService.update_task(session, task_id, current_user.id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or does not belong to user")
    return task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user_from_header),
    session: Session = Depends(get_session)
):
    """
    Remove a task from the system (must belong to authenticated user).

    Args:
        task_id: The ID of the task to delete
        current_user: The authenticated user (extracted from JWT token)
        session: Database session dependency

    Returns:
        Success message
    """
    success = TaskService.delete_task(session, task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found or does not belong to user")
    return {"message": "Task deleted successfully"}


@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
def update_task_completion(
    task_id: int,
    completed: bool,
    current_user: User = Depends(get_current_user_from_header),
    session: Session = Depends(get_session)
):
    """
    Mark a task as complete or incomplete (must belong to authenticated user).

    Args:
        task_id: The ID of the task to update
        completed: New completion status for the task
        current_user: The authenticated user (extracted from JWT token)
        session: Database session dependency

    Returns:
        Updated Task object
    """
    task = TaskService.toggle_task_completion(session, task_id, current_user.id, completed)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or does not belong to user")
    return task