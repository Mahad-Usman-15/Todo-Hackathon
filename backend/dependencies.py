from fastapi import Depends, HTTPException, status
from auth import get_current_user
from db import get_session
from sqlmodel import Session
from fastapi import Request, Header


def get_current_active_user(current_user: str = Depends(get_current_user)):
    """
    Get current active user from JWT token
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


def get_db_session():
    """
    Get database session dependency
    """
    yield from get_session()


def get_token_from_request_header(authorization: str = Header(None)):
    """
    Extract token from Authorization header in request
    """
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must start with 'Bearer '",
        )

    token = authorization.split(" ")[1]
    return token