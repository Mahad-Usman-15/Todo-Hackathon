"""
Unit tests for the Task model
"""

import sys
import os
# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.todo.models import Task


def test_task_creation():
    """Test creating a new task with required fields."""
    task = Task(1, "Test Title", "Test Description", False)
    
    assert task.id == 1
    assert task.title == "Test Title"
    assert task.description == "Test Description"
    assert task.completed == False
    
    print("PASS: Task creation test passed")


def test_task_defaults():
    """Test creating a task with default values."""
    task = Task(2, "Test Title")
    
    assert task.id == 2
    assert task.title == "Test Title"
    assert task.description == ""
    assert task.completed == False
    
    print("PASS: Task defaults test passed")


def test_task_string_representation():
    """Test the string representation of a task."""
    task_complete = Task(1, "Complete Task", "", True)
    task_incomplete = Task(2, "Incomplete Task", "", False)
    
    assert "✓" in str(task_complete)
    assert "○" in str(task_incomplete)
    assert "1:" in str(task_complete)
    assert "2:" in str(task_incomplete)
    
    print("PASS: Task string representation test passed")


def test_task_to_dict():
    """Test converting a task to dictionary."""
    task = Task(1, "Test Title", "Test Description", True)
    task_dict = task.to_dict()
    
    expected = {
        "id": 1,
        "title": "Test Title",
        "description": "Test Description",
        "completed": True
    }
    
    assert task_dict == expected
    
    print("PASS: Task to dictionary test passed")


def test_task_from_dict():
    """Test creating a task from dictionary."""
    data = {
        "id": 1,
        "title": "Test Title",
        "description": "Test Description",
        "completed": True
    }
    
    task = Task.from_dict(data)
    
    assert task.id == 1
    assert task.title == "Test Title"
    assert task.description == "Test Description"
    assert task.completed == True
    
    print("PASS: Task from dictionary test passed")


if __name__ == "__main__":
    print("Running Task model tests...")
    
    test_task_creation()
    test_task_defaults()
    test_task_string_representation()
    test_task_to_dict()
    test_task_from_dict()
    
    print("\nAll Task model tests passed! SUCCESS")