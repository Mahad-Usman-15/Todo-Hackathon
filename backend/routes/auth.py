from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session, select
from models import User, UserCreate, UserLogin, UserRead
from db import get_session
from config import settings
import uuid
from datetime import datetime
import logging




# Initialize logging
logger = logging.getLogger(__name__)

# Security schemes
security = HTTPBearer()


pwd_context = CryptContext(
    schemes=["argon2"],
    argon2__type="ID",   # ensures Argon2id
    deprecated="auto"
)



# JWT Configuration
SECRET_KEY = settings.BETTER_AUTH_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/auth", tags=["authentication"])

# Pydantic models for request/response
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserRead

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    # Validate password length before hashing to prevent bcrypt errors
    if len(password.encode('utf-8')) > 72:
        raise ValueError("password cannot be longer than 72 bytes, truncate manually if necessary (e.g. my_password[:72])")

    # Attempt to hash the password, catching any bcrypt-related errors
    try:
        return pwd_context.hash(password)
    except Exception as e:
        # Check if this is the specific bcrypt version error or length error
        error_str = str(e).lower()
        if "password cannot be longer than 72 bytes" in error_str or "72 bytes" in error_str:
            raise ValueError("password cannot be longer than 72 bytes, truncate manually if necessary (e.g. my_password[:72])")
        else:
            # Re-raise the original exception if it's a different error
            raise e

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(session: Session, email: str, password: str):
    # Check password length to prevent bcrypt errors during verification
    if len(password.encode('utf-8')) > 72:
        raise ValueError("password cannot be longer than 72 bytes, truncate manually if necessary (e.g. my_password[:72])")

    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user:
        return False

    # Verify password, handling any bcrypt-related errors
    try:
        if not verify_password(password, user.hashed_password):
            return False
    except Exception as e:
        error_str = str(e).lower()
        if "password cannot be longer than 72 bytes" in error_str or "72 bytes" in error_str:
            raise ValueError("password cannot be longer than 72 bytes, truncate manually if necessary (e.g. my_password[:72])")
        else:
            # For other errors, return False to indicate authentication failure
            return False

    return user

def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        email: str = payload.get("email")
        if not user_id or not email:
            raise HTTPException(status_code=401, detail="Invalid session. Please log in again.")
        return {"user_id": user_id, "email": email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid session. Please log in again.")



@router.post("/register", response_model=LoginResponse)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user
    """
    try:
        # Check if user already exists
        statement = select(User).where(User.email == user_data.email)
        existing_user = session.exec(statement).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Check password length before attempting to hash
        if len(user_data.password.encode('utf-8')) > 72:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must not exceed 72 bytes"
            )

        # Hash the password
        hashed_password = get_password_hash(user_data.password)

        # Create new user
        user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            hashed_password=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": user.id, "email": user.email},
            expires_delta=access_token_expires
        )

        logger.info(f"User registered successfully: {user.email}")

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserRead.from_orm(user)
        )
    except ValueError as e:
        # Handle password length errors specifically
        logger.error(f"Password validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must not exceed 72 bytes"
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=LoginResponse)
def login(user_data: UserLogin, session: Session = Depends(get_session)):
    """
    Authenticate user and return access token
    """
    try:
        # Validate password length before calling authenticate_user
        if len(user_data.password.encode('utf-8')) > 72:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must not exceed 72 bytes"
            )

        user = authenticate_user(session, user_data.email, user_data.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password. Please check your credentials and try again.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": user.id, "email": user.email},
            expires_delta=access_token_expires
        )

        logger.info(f"User logged in successfully: {user.email}")

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserRead.from_orm(user)
        )
    except ValueError as e:
        # Handle password length errors specifically
        logger.error(f"Password validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must not exceed 72 bytes"
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.get("/profile", response_model=UserRead)
def get_profile(current_user: dict = Depends(get_current_user_from_token), session: Session = Depends(get_session)):
    """
    Get current user profile
    """
    try:
        user_id = current_user["user_id"]

        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserRead.from_orm(user)
    except Exception as e:
        logger.error(f"Get profile error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve profile"
        )


@router.post("/logout")
def logout(request: Request):
    """
    Logout user (currently just a placeholder for Better Auth integration)
    In a real implementation with Better Auth, this would invalidate the session
    """
    try:
        # In a real Better Auth implementation, this would call the logout endpoint
        # to clear the httpOnly cookie on the client side
        logger.info(f"User logout initiated from {request.client.host}")

        # For now, just return success - the actual session invalidation would happen
        # on the client side by clearing the Better Auth session

        return {"success": True, "message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )