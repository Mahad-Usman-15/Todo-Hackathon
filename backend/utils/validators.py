import re
from datetime import datetime
from typing import Optional


def sanitize_input(input_str: str) -> str:
    """
    Sanitize input string to prevent injection attacks
    """
    if not input_str or not isinstance(input_str, str):
        return input_str

    # Remove potentially dangerous characters/sequences
    sanitized = input_str.strip()

    # Prevent SQL injection attempts
    dangerous_patterns = [
        r"(?i)(union\s+select)",
        r"(?i)(drop\s+\w+)",
        r"(?i)(delete\s+from)",
        r"(?i)(insert\s+into)",
        r"(?i)(update\s+\w+\s+set)",
        r"(?i)(exec\s*\()",
        r"(?i)(execute\s*\()",
        r"--",  # SQL comment
        r";",   # Statement terminator
        r"\*",  # Could be used in wildcards for SQL
        r"'",   # Quote character
        r'"',   # Double quote character
    ]

    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, "", sanitized)

    return sanitized


def validate_task_title(title: str) -> bool:
    """
    Validate task title: 1-200 characters, safe characters only
    """
    if not title or not isinstance(title, str):
        return False

    # Sanitize the input first
    sanitized_title = sanitize_input(title)

    # Check length after sanitization
    if len(sanitized_title) < 1 or len(sanitized_title) > 200:
        return False

    # Ensure it contains only safe characters (letters, numbers, spaces, common punctuation)
    if not re.match(r'^[a-zA-Z0-9\s\-\_\.!,?\'\":;\(\)\[\]\{\}/\\]+$', sanitized_title):
        return False

    return True


def validate_task_description(description: Optional[str]) -> bool:
    """
    Validate task description: 0-1000 characters if provided, safe characters only
    """
    if description is None:
        return True
    if not isinstance(description, str):
        return False

    # Sanitize the input first
    sanitized_description = sanitize_input(description)

    # Check length after sanitization
    if len(sanitized_description) > 1000:
        return False

    # Ensure it contains only safe characters (letters, numbers, spaces, common punctuation)
    if not re.match(r'^[a-zA-Z0-9\s\-\_\.!,?\'\":;\(\)\[\]\{\}/\\<>\n\r]*$', sanitized_description):
        return False

    return True


def validate_due_date_format(due_date: Optional[datetime]) -> bool:
    """
    Validate due date format if provided
    """
    if due_date is None:
        return True
    return isinstance(due_date, datetime)


def validate_user_id(user_id: str) -> bool:
    """
    Validate user ID format - alphanumeric, hyphens, underscores only
    """
    if not user_id or not isinstance(user_id, str):
        return False

    # Sanitize the user ID
    sanitized_user_id = sanitize_input(user_id)

    # Check length
    if len(sanitized_user_id) == 0 or len(sanitized_user_id) > 255:
        return False

    # Ensure it contains only safe characters (alphanumeric, hyphens, underscores)
    if not re.match(r'^[a-zA-Z0-9_-]+$', sanitized_user_id):
        return False

    return True