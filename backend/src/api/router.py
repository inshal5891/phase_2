from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from ..database.session import get_session
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..services.task_service import TaskService
from ..models.user import User

router = APIRouter(prefix="/api", tags=["tasks"])

@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    user_id: int = Query(..., description="User ID for the tasks"),
    completed: Optional[bool] = Query(None, description="Filter by completion status (true for completed, false for pending)"),
    session: Session = Depends(get_session)
):
    """
    Retrieve a list of all tasks for the user.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        completed: Optional filter for completion status
        session: Database session dependency

    Returns:
        List of Task objects
    """
    tasks = TaskService.get_tasks_by_user(session, user_id, completed)
    return tasks

@router.post("/tasks", response_model=TaskRead, status_code=201)
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new todo task.

    Args:
        task_data: Task creation data
        session: Database session dependency

    Returns:
        Created Task object
    """
    try:
        task = TaskService.create_task(session, task_data)
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating task: {str(e)}")

@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    user_id: int = Query(..., description="User ID for the task"),
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific task by its ID.

    Args:
        task_id: The ID of the task to retrieve
        user_id: The ID of the user who owns the task
        session: Database session dependency

    Returns:
        Task object
    """
    task = TaskService.get_task_by_id(session, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    user_id: int = Query(..., description="User ID for the task"),
    session: Session = Depends(get_session)
):
    """
    Update an existing task with new information.

    Args:
        task_id: The ID of the task to update
        task_update: Task update data
        user_id: The ID of the user who owns the task
        session: Database session dependency

    Returns:
        Updated Task object
    """
    task = TaskService.update_task(session, task_id, user_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    user_id: int = Query(..., description="User ID for the task"),
    session: Session = Depends(get_session)
):
    """
    Remove a task from the system.

    Args:
        task_id: The ID of the task to delete
        user_id: The ID of the user who owns the task
        session: Database session dependency

    Returns:
        Success message
    """
    success = TaskService.delete_task(session, task_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
def update_task_completion(
    task_id: int,
    completed: bool,
    user_id: int = Query(..., description="User ID for the task"),
    session: Session = Depends(get_session)
):
    """
    Mark a task as complete or incomplete.

    Args:
        task_id: The ID of the task to update
        completed: New completion status for the task
        user_id: The ID of the user who owns the task
        session: Database session dependency

    Returns:
        Updated Task object
    """
    task = TaskService.toggle_task_completion(session, task_id, user_id, completed)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task