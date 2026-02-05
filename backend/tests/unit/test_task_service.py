import pytest
from sqlmodel import Session, SQLModel, create_engine
from backend.src.models.task import Task, TaskCreate, TaskUpdate
from backend.src.services.task_service import TaskService
from backend.src.models.user import User, UserCreate

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_create_task(session: Session):
    # Create a user first
    user = User(email="test@example.com")
    session.add(user)
    session.commit()

    # Create task data
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        user_id=user.id
    )

    # Create the task
    created_task = TaskService.create_task(session, task_data)

    # Assert the task was created correctly
    assert created_task.title == "Test Task"
    assert created_task.description == "This is a test task"
    assert created_task.completed is False
    assert created_task.user_id == user.id

def test_get_task_by_id(session: Session):
    # Create a user first
    user = User(email="test@example.com")
    session.add(user)
    session.commit()

    # Create a task
    task_data = TaskCreate(
        title="Test Task",
        description="This is a test task",
        user_id=user.id
    )
    created_task = TaskService.create_task(session, task_data)

    # Get the task by ID
    retrieved_task = TaskService.get_task_by_id(session, created_task.id, user.id)

    # Assert the task was retrieved correctly
    assert retrieved_task is not None
    assert retrieved_task.title == "Test Task"
    assert retrieved_task.id == created_task.id

def test_get_tasks_by_user(session: Session):
    # Create a user first
    user = User(email="test@example.com")
    session.add(user)
    session.commit()

    # Create multiple tasks for the user
    task_data_1 = TaskCreate(title="Task 1", user_id=user.id)
    task_data_2 = TaskCreate(title="Task 2", user_id=user.id)

    TaskService.create_task(session, task_data_1)
    TaskService.create_task(session, task_data_2)

    # Get all tasks for the user
    tasks = TaskService.get_tasks_by_user(session, user.id)

    # Assert we got the right number of tasks
    assert len(tasks) == 2

    # Assert the tasks belong to the correct user
    for task in tasks:
        assert task.user_id == user.id

def test_update_task(session: Session):
    # Create a user first
    user = User(email="test@example.com")
    session.add(user)
    session.commit()

    # Create a task
    task_data = TaskCreate(
        title="Original Task",
        description="Original description",
        user_id=user.id
    )
    created_task = TaskService.create_task(session, task_data)

    # Update the task
    update_data = TaskUpdate(
        title="Updated Task",
        completed=True
    )
    updated_task = TaskService.update_task(session, created_task.id, user.id, update_data)

    # Assert the task was updated correctly
    assert updated_task.title == "Updated Task"
    assert updated_task.completed is True
    assert updated_task.description == "Original description"  # Unchanged

def test_delete_task(session: Session):
    # Create a user first
    user = User(email="test@example.com")
    session.add(user)
    session.commit()

    # Create a task
    task_data = TaskCreate(
        title="Task to Delete",
        user_id=user.id
    )
    created_task = TaskService.create_task(session, task_data)

    # Delete the task
    result = TaskService.delete_task(session, created_task.id, user.id)

    # Assert the task was deleted
    assert result is True

    # Verify the task no longer exists
    retrieved_task = TaskService.get_task_by_id(session, created_task.id, user.id)
    assert retrieved_task is None