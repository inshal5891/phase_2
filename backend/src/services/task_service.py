from sqlmodel import Session, select, and_
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate
from sqlalchemy.exc import IntegrityError


class TaskService:
    """Service class for handling task-related business logic."""

    @staticmethod
    def create_task_for_user(session: Session, task_data: TaskCreate, user_id: int) -> Task:
        """
        Create a new task for a specific user.

        Args:
            session: Database session
            task_data: Task creation data
            user_id: ID of the user who will own the task

        Returns:
            The created Task object
        """
        # Create task with the provided data and assign to user
        task = Task.from_orm(task_data)
        task.user_id = user_id
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate) -> Task:
        """
        Create a new task in the database (original method, kept for backward compatibility).

        Args:
            session: Database session
            task_data: Task creation data

        Returns:
            The created Task object
        """
        task = Task.from_orm(task_data)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_task_by_id(session: Session, task_id: int, user_id: int) -> Optional[Task]:
        """
        Retrieve a specific task by its ID for a specific user.

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user who owns the task

        Returns:
            The Task object if found, None otherwise
        """
        statement = select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        task = session.exec(statement).first()
        return task

    @staticmethod
    def get_tasks_by_user(session: Session, user_id: int, completed: Optional[bool] = None) -> List[Task]:
        """
        Retrieve all tasks for a specific user with optional completion status filter.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve
            completed: Optional filter for completion status (True=completed, False=pending, None=all)

        Returns:
            List of Task objects
        """
        query = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            query = query.where(Task.completed == completed)

        tasks = session.exec(query).all()
        return tasks

    @staticmethod
    def update_task(session: Session, task_id: int, user_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """
        Update an existing task with new information.

        Args:
            session: Database session
            task_id: ID of the task to update
            user_id: ID of the user who owns the task
            task_update: Task update data

        Returns:
            The updated Task object if successful, None if task not found
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return None

        # Update only the fields that are provided in task_update
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: int) -> bool:
        """
        Delete a task from the database.

        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the user who owns the task

        Returns:
            True if task was deleted, False if task was not found
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(session: Session, task_id: int, user_id: int, completed: bool) -> Optional[Task]:
        """
        Toggle the completion status of a task.

        Args:
            session: Database session
            task_id: ID of the task to update
            user_id: ID of the user who owns the task
            completed: New completion status

        Returns:
            The updated Task object if successful, None if task not found
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return None

        task.completed = completed
        session.add(task)
        session.commit()
        session.refresh(task)
        return task