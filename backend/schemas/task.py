from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None


class TaskCompletionUpdate(BaseModel):
    completed: bool


class TaskListQuery(BaseModel):
    status: Optional[str] = None  # "all", "pending", "completed"
    sort: Optional[str] = None  # "created_at", "title", "due_date"
    limit: Optional[int] = None
    offset: Optional[int] = None