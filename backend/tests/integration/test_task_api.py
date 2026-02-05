import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.database.session import engine
from backend.src.models import SQLModel
from backend.src.models.user import User
from backend.src.models.task import Task
from sqlmodel import Session, delete

# Create a test client
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: Create all tables
    SQLModel.metadata.create_all(bind=engine)
    yield
    # Teardown: Drop all tables
    with Session(engine) as session:
        session.exec(delete(Task))
        session.exec(delete(User))
        session.commit()

def test_create_task():
    # Create a task
    response = client.post("/api/tasks", json={
        "title": "Test Task",
        "description": "This is a test task",
        "user_id": 1  # Using a fixed user ID for this spec
    })

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["completed"] is False

def test_get_tasks():
    # Create a task first
    client.post("/api/tasks", json={
        "title": "Test Task",
        "user_id": 1
    })

    # Get all tasks
    response = client.get("/api/tasks", params={"user_id": 1})

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_get_task_by_id():
    # Create a task
    create_response = client.post("/api/tasks", json={
        "title": "Test Task",
        "user_id": 1
    })

    task_id = create_response.json()["id"]

    # Get the specific task
    response = client.get(f"/api/tasks/{task_id}", params={"user_id": 1})

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"

def test_update_task():
    # Create a task
    create_response = client.post("/api/tasks", json={
        "title": "Original Task",
        "user_id": 1
    })

    task_id = create_response.json()["id"]

    # Update the task
    response = client.put(f"/api/tasks/{task_id}", params={"user_id": 1}, json={
        "title": "Updated Task",
        "completed": True
    })

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["completed"] is True

def test_delete_task():
    # Create a task
    create_response = client.post("/api/tasks", json={
        "title": "Task to Delete",
        "user_id": 1
    })

    task_id = create_response.json()["id"]

    # Delete the task
    response = client.delete(f"/api/tasks/{task_id}", params={"user_id": 1})

    assert response.status_code == 200

    # Verify the task is gone
    get_response = client.get(f"/api/tasks/{task_id}", params={"user_id": 1})
    assert get_response.status_code == 404

def test_toggle_task_completion():
    # Create a task
    create_response = client.post("/api/tasks", json={
        "title": "Test Task",
        "user_id": 1
    })

    task_id = create_response.json()["id"]

    # Toggle the task completion
    response = client.patch(f"/api/tasks/{task_id}/complete",
                           params={"user_id": 1},
                           json={"completed": True})

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True