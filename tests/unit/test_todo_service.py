"""
Unit tests for the TodoService
"""

import sys
import os
# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.todo.service import TodoService


def test_add_task():
    """Test adding a new task."""
    service = TodoService()
    
    task = service.add_task("Test Task", "Test Description")
    
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed == False
    assert len(service.get_all_tasks()) == 1
    
    print("PASS: Add task test passed")


def test_add_task_required_title():
    """Test that adding a task requires a title."""
    service = TodoService()
    
    try:
        service.add_task("")
        assert False, "Expected ValueError for empty title"
    except ValueError:
        pass  # Expected
    
    print("PASS: Add task required title test passed")


def test_get_all_tasks():
    """Test getting all tasks."""
    service = TodoService()
    
    service.add_task("Task 1")
    service.add_task("Task 2")
    
    tasks = service.get_all_tasks()
    
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"
    
    print("PASS: Get all tasks test passed")


def test_get_task_by_id():
    """Test getting a task by its ID."""
    service = TodoService()
    
    task = service.add_task("Test Task")
    retrieved_task = service.get_task_by_id(task.id)
    
    assert retrieved_task is not None
    assert retrieved_task.id == task.id
    assert retrieved_task.title == task.title
    
    # Test with non-existent ID
    non_existent_task = service.get_task_by_id(999)
    assert non_existent_task is None
    
    print("PASS: Get task by ID test passed")


def test_update_task():
    """Test updating a task."""
    service = TodoService()
    
    task = service.add_task("Original Title", "Original Description")
    
    updated_task = service.update_task(task.id, "New Title", "New Description")
    
    assert updated_task.id == task.id
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"
    
    # Test updating only title
    updated_task = service.update_task(task.id, "Updated Title Again")
    assert updated_task.title == "Updated Title Again"
    assert updated_task.description == "New Description"  # Should remain unchanged
    
    # Test updating only description
    updated_task = service.update_task(task.id, description="Updated Description")
    assert updated_task.title == "Updated Title Again"  # Should remain unchanged
    assert updated_task.description == "Updated Description"
    
    print("PASS: Update task test passed")


def test_update_task_empty_title():
    """Test that updating a task with an empty title raises an error."""
    service = TodoService()
    
    task = service.add_task("Original Title")
    
    try:
        service.update_task(task.id, "")
        assert False, "Expected ValueError for empty title"
    except ValueError:
        pass  # Expected
    
    print("PASS: Update task empty title test passed")


def test_delete_task():
    """Test deleting a task."""
    service = TodoService()
    
    task = service.add_task("Test Task")
    initial_count = len(service.get_all_tasks())
    
    success = service.delete_task(task.id)
    
    assert success == True
    assert len(service.get_all_tasks()) == initial_count - 1
    assert service.get_task_by_id(task.id) is None
    
    # Test deleting non-existent task
    success = service.delete_task(999)
    assert success == False
    
    print("PASS: Delete task test passed")


def test_toggle_task_status():
    """Test toggling a task's completion status."""
    service = TodoService()
    
    task = service.add_task("Test Task")
    
    # Initially should be incomplete
    assert task.completed == False
    
    # Toggle to complete
    toggled_task = service.toggle_task_status(task.id)
    assert toggled_task.completed == True
    
    # Toggle back to incomplete
    toggled_task = service.toggle_task_status(task.id)
    assert toggled_task.completed == False
    
    # Test toggling non-existent task
    result = service.toggle_task_status(999)
    assert result is None
    
    print("PASS: Toggle task status test passed")


if __name__ == "__main__":
    print("Running TodoService tests...")
    
    test_add_task()
    test_add_task_required_title()
    test_get_all_tasks()
    test_get_task_by_id()
    test_update_task()
    test_update_task_empty_title()
    test_delete_task()
    test_toggle_task_status()
    
    print("\nAll TodoService tests passed! SUCCESS")