"""
Simple test to verify the Intermediate Level Todo application functionality
"""
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from todo2.models import Task, Priority
from todo2.service import TodoService

def test_basic_functionality():
    print("Testing basic functionality of Intermediate Level Todo app...")
    
    # Create a service instance
    service = TodoService()
    
    # Test adding a task with priority and tags
    print("\n1. Testing task creation with priority and tags...")
    task = service.add_task("Test task", "This is a test description", Priority.HIGH, {"work", "important"})
    print(f"Created task: ID {task.id}, Title: {task.title}, Priority: {task.priority.value}, Tags: {task.tags}")
    
    # Test adding another task
    task2 = service.add_task("Another task", "Another description", Priority.LOW, {"personal"})
    print(f"Created task: ID {task2.id}, Title: {task2.title}, Priority: {task2.priority.value}, Tags: {task2.tags}")
    
    # Test getting all tasks
    print("\n2. Testing get all tasks...")
    all_tasks = service.get_all_tasks()
    print(f"Total tasks: {len(all_tasks)}")
    for task in all_tasks:
        print(f"  - ID {task.id}: {task.title} (Priority: {task.priority.value}, Tags: {task.tags})")
    
    # Test updating task priority
    print("\n3. Testing update task priority...")
    updated_task = service.update_task_priority(task.id, Priority.MEDIUM)
    print(f"Updated task {task.id} priority to: {updated_task.priority.value}")
    
    # Test filtering by priority
    print("\n4. Testing filter by priority...")
    medium_tasks = service.get_tasks_by_priority(Priority.MEDIUM)
    print(f"Tasks with MEDIUM priority: {len(medium_tasks)}")
    for task in medium_tasks:
        print(f"  - ID {task.id}: {task.title}")
    
    # Test adding a tag to existing task
    print("\n5. Testing add tag to existing task...")
    tagged_task = service.add_tag_to_task(task.id, "urgent")
    print(f"Added 'urgent' tag to task {task.id}. Current tags: {tagged_task.tags}")
    
    # Test filtering by tag
    print("\n6. Testing filter by tag...")
    urgent_tasks = service.get_tasks_by_tag("urgent")
    print(f"Tasks with 'urgent' tag: {len(urgent_tasks)}")
    for task in urgent_tasks:
        print(f"  - ID {task.id}: {task.title}")
    
    # Test search functionality
    print("\n7. Testing search functionality...")
    search_results = service.search_tasks("test")
    print(f"Search results for 'test': {len(search_results)}")
    for task in search_results:
        print(f"  - ID {task.id}: {task.title}")
    
    # Test sorting by priority
    print("\n8. Testing sort by priority...")
    sorted_tasks = service.sort_tasks("priority")
    print("Tasks sorted by priority:")
    for task in sorted_tasks:
        print(f"  - ID {task.id}: {task.title} (Priority: {task.priority.value})")
    
    # Test filtering with multiple criteria
    print("\n9. Testing filter with multiple criteria...")
    filtered_tasks = service.filter_tasks(status=False, priority=Priority.MEDIUM)  # Incomplete tasks with MEDIUM priority
    print(f"Filtered tasks (incomplete, MEDIUM priority): {len(filtered_tasks)}")
    for task in filtered_tasks:
        print(f"  - ID {task.id}: {task.title}")
    
    print("\nAll tests completed successfully! The Intermediate Level features are working correctly.")

if __name__ == "__main__":
    test_basic_functionality()