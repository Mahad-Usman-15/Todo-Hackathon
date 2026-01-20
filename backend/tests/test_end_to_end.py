"""End-to-end tests for the complete task management workflow"""

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


def test_complete_task_lifecycle_end_to_end(client: TestClient, session: Session):
    """
    Complete end-to-end test covering all user stories:
    1. Create a new task (User Story 1)
    2. View tasks (User Story 2)
    3. Update task (User Story 3)
    4. Toggle completion status (User Story 5)
    5. Delete task (User Story 4)
    """
    user_id = "e2e_test_user_123"

    # User Story 1: Create a new task
    print("Testing User Story 1: Create a new task")
    task_data = {
        "title": "E2E Test Task",
        "description": "This is a test task for end-to-end testing",
        "due_date": "2024-12-31T10:00:00Z"
    }

    response = client.post(f"/api/{user_id}/tasks", json=task_data)
    assert response.status_code == 201, f"Failed to create task: {response.text}"

    created_task = response.json()
    task_id = created_task["id"]
    assert created_task["title"] == task_data["title"]
    assert created_task["description"] == task_data["description"]
    assert created_task["completed"] is False
    print("✓ User Story 1 completed: Task created successfully")

    # User Story 2: View tasks
    print("\nTesting User Story 2: View tasks")
    response = client.get(f"/api/{user_id}/tasks")
    assert response.status_code == 200, f"Failed to get tasks: {response.text}"

    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    assert tasks[0]["title"] == task_data["title"]
    print("✓ User Story 2 completed: Tasks retrieved successfully")

    # User Story 3: Update task
    print("\nTesting User Story 3: Update task")
    update_data = {
        "title": "Updated E2E Test Task",
        "description": "Updated description for end-to-end testing",
        "due_date": "2024-11-30T15:00:00Z"
    }

    response = client.put(f"/api/{user_id}/tasks/{task_id}", json=update_data)
    assert response.status_code == 200, f"Failed to update task: {response.text}"

    updated_task = response.json()
    assert updated_task["id"] == task_id
    assert updated_task["title"] == update_data["title"]
    assert updated_task["description"] == update_data["description"]
    print("✓ User Story 3 completed: Task updated successfully")

    # User Story 5: Toggle completion status
    print("\nTesting User Story 5: Toggle completion status")
    completion_data = {"completed": True}

    response = client.patch(f"/api/{user_id}/tasks/{task_id}/complete", json=completion_data)
    assert response.status_code == 200, f"Failed to toggle completion: {response.text}"

    completed_task = response.json()
    assert completed_task["id"] == task_id
    assert completed_task["completed"] is True
    print("✓ User Story 5 completed: Completion status toggled successfully")

    # Verify the task is now completed by getting the list again
    response = client.get(f"/api/{user_id}/tasks?status=completed")
    assert response.status_code == 200
    completed_tasks = response.json()
    assert len(completed_tasks) == 1
    assert completed_tasks[0]["id"] == task_id
    assert completed_tasks[0]["completed"] is True

    # Toggle back to incomplete
    completion_data = {"completed": False}
    response = client.patch(f"/api/{user_id}/tasks/{task_id}/complete", json=completion_data)
    assert response.status_code == 200
    incomplete_task = response.json()
    assert incomplete_task["completed"] is False
    print("- Completion status toggled back to incomplete for next test")

    # User Story 4: Delete task
    print("\nTesting User Story 4: Delete task")
    response = client.delete(f"/api/{user_id}/tasks/{task_id}")
    assert response.status_code == 204, f"Failed to delete task: {response.text}"

    # Verify task is deleted
    response = client.get(f"/api/{user_id}/tasks")
    assert response.status_code == 200
    remaining_tasks = response.json()
    assert len(remaining_tasks) == 0
    print("✓ User Story 4 completed: Task deleted successfully")

    print("\n🎉 All user stories completed successfully in end-to-end test!")


def test_multiple_users_isolation_end_to_end(client: TestClient, session: Session):
    """
    Test user isolation to ensure users can only access their own tasks
    """
    user1_id = "user1_e2e_test"
    user2_id = "user2_e2e_test"

    # Create tasks for user 1
    task1_data = {
        "title": "User 1 Task",
        "description": "Task for user 1"
    }
    response1 = client.post(f"/api/{user1_id}/tasks", json=task1_data)
    assert response1.status_code == 201
    user1_task = response1.json()

    # Create tasks for user 2
    task2_data = {
        "title": "User 2 Task",
        "description": "Task for user 2"
    }
    response2 = client.post(f"/api/{user2_id}/tasks", json=task2_data)
    assert response2.status_code == 201
    user2_task = response2.json()

    # Verify user 1 can only see their own task
    response = client.get(f"/api/{user1_id}/tasks")
    assert response.status_code == 200
    user1_tasks = response.json()
    assert len(user1_tasks) == 1
    assert user1_tasks[0]["title"] == "User 1 Task"

    # Verify user 2 can only see their own task
    response = client.get(f"/api/{user2_id}/tasks")
    assert response.status_code == 200
    user2_tasks = response.json()
    assert len(user2_tasks) == 1
    assert user2_tasks[0]["title"] == "User 2 Task"

    # Verify users cannot access each other's tasks
    response = client.get(f"/api/{user1_id}/tasks")
    user1_tasks = response.json()
    assert len(user1_tasks) == 1
    assert user1_tasks[0]["id"] != user2_task["id"]

    response = client.get(f"/api/{user2_id}/tasks")
    user2_tasks = response.json()
    assert len(user2_tasks) == 1
    assert user2_tasks[0]["id"] != user1_task["id"]

    print("✅ User isolation verified: Each user can only access their own tasks")


def test_rate_limiting_end_to_end(client: TestClient, session: Session):
    """
    Test that rate limiting is working properly
    Although we can't easily test the actual rate limiting in this synchronous test,
    we can at least verify that multiple requests work normally within limits
    """
    user_id = "rate_limit_test_user"

    # Create several tasks to test normal operation
    for i in range(3):
        task_data = {
            "title": f"Rate Limit Test Task {i+1}",
            "description": f"Task {i+1} for rate limiting test"
        }
        response = client.post(f"/api/{user_id}/tasks", json=task_data)
        assert response.status_code == 201

    # Get all tasks
    response = client.get(f"/api/{user_id}/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 3

    print("✅ Multiple requests processed successfully - rate limiting doesn't interfere with normal operation")


if __name__ == "__main__":
    # This allows running the test file directly for debugging
    pytest.main([__file__, "-v"])