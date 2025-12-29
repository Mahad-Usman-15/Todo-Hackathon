"""
Integration test for the Todo Console Application
"""

import sys
import os
# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.todo.models import Task
from src.todo.service import TodoService
from src.todo.cli import TodoCLI


def test_integration():
    """Test that all components work together."""
    print("Testing integration of all components...")
    
    # Test the service layer
    service = TodoService()
    
    # Add a task
    task1 = service.add_task("Integration Test Task", "This is an integration test")
    assert task1.id == 1
    assert task1.title == "Integration Test Task"
    assert task1.description == "This is an integration test"
    assert task1.completed == False
    
    # Add another task
    task2 = service.add_task("Second Integration Task")
    assert task2.id == 2
    assert task2.title == "Second Integration Task"
    assert task2.description == ""
    assert task2.completed == False
    
    # Verify both tasks exist
    all_tasks = service.get_all_tasks()
    assert len(all_tasks) == 2
    assert all_tasks[0].id == 1
    assert all_tasks[1].id == 2
    
    # Test updating a task
    updated_task = service.update_task(1, "Updated Integration Task", "Updated description")
    assert updated_task.title == "Updated Integration Task"
    assert updated_task.description == "Updated description"
    
    # Test toggling completion status
    toggled_task = service.toggle_task_status(1)
    assert toggled_task.completed == True
    
    # Test deleting a task
    delete_success = service.delete_task(2)
    assert delete_success == True
    assert len(service.get_all_tasks()) == 1
    
    # Verify the remaining task is the one we expect
    remaining_tasks = service.get_all_tasks()
    assert len(remaining_tasks) == 1
    assert remaining_tasks[0].id == 1
    assert remaining_tasks[0].title == "Updated Integration Task"
    
    print("PASS: All integration tests passed")


def test_cli_initialization():
    """Test that CLI initializes properly."""
    print("Testing CLI initialization...")
    
    cli = TodoCLI()
    assert cli.service is not None
    assert hasattr(cli.service, 'add_task')
    assert hasattr(cli.service, 'get_all_tasks')
    assert hasattr(cli.service, 'get_task_by_id')
    assert hasattr(cli.service, 'update_task')
    assert hasattr(cli.service, 'delete_task')
    assert hasattr(cli.service, 'toggle_task_status')
    
    print("PASS: CLI initialization test passed")


def test_task_model():
    """Test the Task model directly."""
    print("Testing Task model...")
    
    task = Task(1, "Test Task", "Test Description", False)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed == False
    
    # Test string representation
    task_str = str(task)
    assert "○" in task_str  # Should show as incomplete
    assert "1:" in task_str
    assert "Test Task" in task_str
    
    # Toggle completion and test again
    task.completed = True
    task_str = str(task)
    assert "✓" in task_str  # Should show as complete
    
    # Test to_dict and from_dict
    task_dict = task.to_dict()
    expected_dict = {
        "id": 1,
        "title": "Test Task",
        "description": "Test Description",
        "completed": True
    }
    assert task_dict == expected_dict
    
    # Test from_dict
    new_task = Task.from_dict(task_dict)
    assert new_task.id == 1
    assert new_task.title == "Test Task"
    assert new_task.description == "Test Description"
    assert new_task.completed == True
    
    print("PASS: Task model test passed")


if __name__ == "__main__":
    print("Running integration tests...")
    
    test_task_model()
    test_integration()
    test_cli_initialization()
    
    print("\nAll integration tests passed! SUCCESS")