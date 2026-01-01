"""
Todo Console Application - Basic Models
Shared models that can be imported by advanced levels
"""

from enum import Enum


class Priority(Enum):
    """Priority levels for tasks."""
    HIGH = "high"
    MEDIUM = "medium"  # Default
    LOW = "low"