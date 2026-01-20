from pydantic import BaseModel
from typing import Optional


class Error(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: Optional[str] = None