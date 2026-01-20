import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from main import app
from models import Task
from db import get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_task_crud_integration(client: TestClient, session: Session):
    """
    Integration test for full task CRUD operations
    """
    user_id = "integration_test_user_123"

    # 1. Create a task
    task_data = {
        "title": "Integration Test Task",
        "description": "This is an integration test task",
        "due_date": "2023-12-31T10:00:00"
    }

    response = client.post(f"/api/{user_id}/tasks", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]
    assert created_task["title"] == task_data["title"]
    assert created_task["user_id"] == user_id

    # 2. Get the created task
    response = client.get(f"/api/{user_id}/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    assert tasks[0]["title"] == task_data["title"]

    # 3. Update the task
    update_data = {
        "title": "Updated Integration Test Task",
        "completed": True
    }

    response = client.put(f"/api/{user_id}/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == update_data["title"]
    assert updated_task["completed"] == update_data["completed"]

    # 4. Toggle completion status
    completion_data = {"completed": False}
    response = client.patch(f"/api/{user_id}/tasks/{task_id}/complete", json=completion_data)
    assert response.status_code == 200
    toggled_task = response.json()
    assert toggled_task["completed"] == completion_data["completed"]

    # 5. Delete the task
    response = client.delete(f"/api/{user_id}/tasks/{task_id}")
    assert response.status_code == 204

    # 6. Verify task is deleted
    response = client.get(f"/api/{user_id}/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 0


def test_user_isolation_integration(client: TestClient, session: Session):
    """
    Integration test to verify user isolation
    """
    user_id_1 = "user_123"
    user_id_2 = "user_456"

    # Create task for user 1
    task_data = {
        "title": "User 1 Task",
        "description": "Task for user 1"
    }

    response = client.post(f"/api/{user_id_1}/tasks", json=task_data)
    assert response.status_code == 201

    # Create task for user 2
    task_data["title"] = "User 2 Task"
    response = client.post(f"/api/{user_id_2}/tasks", json=task_data)
    assert response.status_code == 201

    # Verify user 1 only sees their own task
    response = client.get(f"/api/{user_id_1}/tasks")
    assert response.status_code == 200
    user1_tasks = response.json()
    assert len(user1_tasks) == 1
    assert user1_tasks[0]["title"] == "User 1 Task"

    # Verify user 2 only sees their own task
    response = client.get(f"/api/{user_id_2}/tasks")
    assert response.status_code == 200
    user2_tasks = response.json()
    assert len(user2_tasks) == 1
    assert user2_tasks[0]["title"] == "User 2 Task"