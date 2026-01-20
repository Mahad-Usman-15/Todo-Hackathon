import logging
import threading
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from models import Task, TaskRead
from schemas.task import TaskCreate as TaskCreateSchema, TaskUpdate as TaskUpdateSchema, TaskCompletionUpdate as TaskCompletionUpdateSchema
from db import get_session
from dependencies import get_current_active_user
from utils.validators import validate_task_title, validate_task_description, validate_due_date_format
from datetime import datetime

# Create a lock dictionary to manage concurrent access to individual tasks
task_locks = {}
lock_manager = threading.Lock()


def get_task_lock(task_id: int):
    """
    Get or create a lock for a specific task to handle concurrent access safely
    """
    with lock_manager:
        if task_id not in task_locks:
            task_locks[task_id] = threading.Lock()
        return task_locks[task_id]

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/{user_id}", tags=["tasks"])


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    task_data: TaskCreateSchema,
    current_user: str = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user
    """
    logger.info(f"Creating task for user {user_id} by authenticated user {current_user}")

    # Add authentication check to ensure user is authorized to create task
    if not current_user:
        logger.warning(f"Unauthorized attempt to create task for user {user_id} - no current user")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in to continue."
        )

    # Add user isolation check to ensure user can only create tasks for themselves
    if user_id != current_user:
        logger.warning(f"User {current_user} attempted to create task for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Validate the input data
    if not validate_task_title(task_data.title):
        logger.warning(f"Invalid title provided when creating task for user {user_id}: {task_data.title}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Task title must be between 1 and 200 characters"
        )

    if not validate_task_description(task_data.description):
        logger.warning(f"Invalid description length when creating task for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Task description exceeds 1000 characters"
        )

    if not validate_due_date_format(task_data.due_date):
        logger.warning(f"Invalid due date format when creating task for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid due date format"
        )

    try:
        # Create the task object
        task = Task(
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            user_id=user_id,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Add to database with transaction handling
        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"Successfully created task {task.id} for user {user_id}")
        return task
    except Exception as e:
        logger.error(f"Failed to create task for user {user_id}: {str(e)}")
        # Add validation error handling for invalid task data
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )


@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    user_id: str,
    current_user: str = Depends(get_current_active_user),
    session: Session = Depends(get_session),
    status_query: str = None,
    sort: str = "created_at",
    limit: int = None,
    offset: int = 0
):
    """
    Retrieve user's tasks with optional filtering and sorting
    """
    logger.info(f"Retrieving tasks for user {user_id} by authenticated user {current_user}, filters: status={status_query}, sort={sort}, limit={limit}, offset={offset}")

    # Add authentication validation for viewing tasks
    if not current_user:
        logger.warning(f"Unauthorized attempt to retrieve tasks for user {user_id} - no current user")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in to continue."
        )

    # Implement user isolation to ensure user only sees their own tasks
    if user_id != current_user:
        logger.warning(f"User {current_user} attempted to retrieve tasks for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view tasks for this user"
        )

    # Build query with user isolation
    query = select(Task).where(Task.user_id == user_id)

    # Add status filtering (all/pending/completed)
    if status_query and status_query.lower() != "all":
        if status_query.lower() == "pending":
            query = query.where(Task.completed == False)
        elif status_query.lower() == "completed":
            query = query.where(Task.completed == True)

    # Add sorting
    if sort == "title":
        query = query.order_by(Task.title)
    elif sort == "due_date":
        query = query.order_by(Task.due_date)
    else:  # Default to created_at
        query = query.order_by(Task.created_at)

    # Add pagination
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)

    try:
        # Execute query
        tasks = session.exec(query).all()
        logger.info(f"Successfully retrieved {len(tasks)} tasks for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to retrieve tasks for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve tasks: {str(e)}"
        )

    # Add proper response formatting for task list
    return tasks


@router.put("/tasks/{id}", response_model=TaskRead)
def update_task(
    user_id: str,
    id: int,
    task_data: TaskUpdateSchema,
    current_user: str = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user
    """
    logger.info(f"Updating task {id} for user {user_id} by authenticated user {current_user}")

    # Acquire lock for this specific task to prevent race conditions during update
    task_lock = get_task_lock(id)
    with task_lock:
        # Add authentication check to ensure user is authorized to update task
        if not current_user:
            logger.warning(f"Unauthorized attempt to update task {id} for user {user_id} - no current user")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required. Please log in to continue."
            )

        # Add user isolation check to prevent unauthorized task modifications
        if user_id != current_user:
            logger.warning(f"User {current_user} attempted to update task {id} for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update tasks for this user"
            )

        # Validate the input data
        if task_data.title is not None and not validate_task_title(task_data.title):
            logger.warning(f"Invalid title provided when updating task {id} for user {user_id}: {task_data.title}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task title must be between 1 and 200 characters"
            )

        if task_data.description is not None and not validate_task_description(task_data.description):
            logger.warning(f"Invalid description length when updating task {id} for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task description exceeds 1000 characters"
            )

        if task_data.due_date is not None and not validate_due_date_format(task_data.due_date):
            logger.warning(f"Invalid due date format when updating task {id} for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid due date format"
            )

        try:
            # Find the task by ID and user ID to ensure user isolation
            statement = select(Task).where(Task.id == id, Task.user_id == user_id)
            task = session.exec(statement).first()

            # Add validation error handling for invalid update data
            if not task:
                logger.warning(f"Attempt to update non-existent task {id} for user {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )

            # Implement business logic to verify user owns the task being updated
            if task.user_id != user_id:
                logger.warning(f"User {user_id} attempted to update task {id} they don't own")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to update this task"
                )

            # Update the task
            update_data = task_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(task, field, value)

            # Update timestamp management (updated_at) for task updates
            task.updated_at = datetime.utcnow()

            # Add database transaction handling for task updates
            session.add(task)
            session.commit()
            session.refresh(task)

            logger.info(f"Successfully updated task {id} for user {user_id}")

            # Add proper response formatting for updated task
            return task
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            logger.error(f"Failed to update task {id} for user {user_id}: {str(e)}")
            # Handle unexpected errors
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update task: {str(e)}"
            )


@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: str,
    id: int,
    current_user: str = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user
    """
    logger.info(f"Deleting task {id} for user {user_id} by authenticated user {current_user}")

    # Acquire lock for this specific task to prevent race conditions during deletion
    task_lock = get_task_lock(id)
    with task_lock:
        # Add authentication check to ensure user is authorized to delete task
        if not current_user:
            logger.warning(f"Unauthorized attempt to delete task {id} for user {user_id} - no current user")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required. Please log in to continue."
            )

        # Add user isolation check to prevent unauthorized task deletions
        if user_id != current_user:
            logger.warning(f"User {current_user} attempted to delete task {id} for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete tasks for this user"
            )

        try:
            # Find the task by ID and user ID to ensure user isolation
            statement = select(Task).where(Task.id == id, Task.user_id == user_id)
            task = session.exec(statement).first()

            # Add proper error handling for non-existent tasks
            if not task:
                logger.warning(f"Attempt to delete non-existent task {id} for user {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )

            # Implement business logic to verify user owns the task being deleted
            if task.user_id != user_id:
                logger.warning(f"User {user_id} attempted to delete task {id} they don't own")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to delete this task"
                )

            # Add database transaction handling for task deletion
            session.delete(task)
            session.commit()

            logger.info(f"Successfully deleted task {id} for user {user_id}")

            # Add proper response formatting for successful deletion (204 status)
            # Response is empty for 204 status
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            logger.error(f"Failed to delete task {id} for user {user_id}: {str(e)}")
            # Handle unexpected errors
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete task: {str(e)}"
            )


@router.patch("/tasks/{id}/complete", response_model=TaskRead)
def toggle_task_completion(
    user_id: str,
    id: int,
    task_data: TaskCompletionUpdateSchema,
    current_user: str = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task for the authenticated user
    """
    logger.info(f"Toggling completion status for task {id} for user {user_id} by authenticated user {current_user}")

    # Acquire lock for this specific task to prevent race conditions during completion status update
    # This is critical for preventing inconsistent completion states
    task_lock = get_task_lock(id)
    with task_lock:
        # Add authentication check to ensure user is authorized to update task
        if not current_user:
            logger.warning(f"Unauthorized attempt to update completion status for task {id} for user {user_id} - no current user")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required. Please log in to continue."
            )

        # Add user isolation check to prevent unauthorized completion updates
        if user_id != current_user:
            logger.warning(f"User {current_user} attempted to update completion status for task {id} for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update tasks for this user"
            )

        try:
            # Find the task by ID and user ID to ensure user isolation
            statement = select(Task).where(Task.id == id, Task.user_id == user_id)
            task = session.exec(statement).first()

            # Add proper error handling for non-existent tasks
            if not task:
                logger.warning(f"Attempt to update completion status for non-existent task {id} for user {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )

            # Implement business logic to verify user owns the task being updated
            if task.user_id != user_id:
                logger.warning(f"User {user_id} attempted to update completion status for task {id} they don't own")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to update this task"
                )

            # Update the completion status
            task.completed = task_data.completed

            # Update timestamp management (updated_at) for completion updates
            task.updated_at = datetime.utcnow()

            # Add database transaction handling for completion updates
            session.add(task)
            session.commit()
            session.refresh(task)

            logger.info(f"Successfully updated completion status for task {id} for user {user_id}")

            # Add proper response formatting for updated task
            return task
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            logger.error(f"Failed to update completion status for task {id} for user {user_id}: {str(e)}")
            # Handle unexpected errors
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update task completion status: {str(e)}"
            )