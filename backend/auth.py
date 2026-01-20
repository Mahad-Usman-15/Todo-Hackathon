# from datetime import datetime, timedelta
# from typing import Optional
# from jose import JWTError, jwt
# from fastapi import HTTPException, status, Depends
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from config import settings
# import bcrypt
# from sqlmodel import Session, select
# from db import get_session
# from models import User as BackendUser


# SECRET_KEY = settings.BETTER_AUTH_SECRET
# ALGORITHM = "HS256"
# security = HTTPBearer()


# def verify_jwt_token(token: str):
#     """
#     Verify JWT token and extract user information
#     Since Better Auth handles user authentication, we trust its JWT tokens.
#     We verify the token is valid and extract the user_id.
#     According to the Better Auth configuration, the token should have 'user_id' field.
#     """
#     try:
#         # First, decode the header without verification to see what algorithm is being used
#         from jose import jws
#         header = jws.get_unverified_header(token)
#         alg = header.get('alg', 'HS256')  # Default to HS256 if no algorithm specified

#         # Allow the detected algorithm plus common ones
#         allowed_algorithms = ["HS256", "HS384", "HS512", "RS256", "RS384", "RS512", "ES256", "ES384", "ES512", "PS256", "PS384", "PS512", "EdDSA"]

#         # Make sure the algorithm from the token is in our allowed list
#         if alg not in allowed_algorithms:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail=f"The specified alg value '{alg}' is not allowed. Allowed: {allowed_algorithms}",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )

#         # Verify token using the algorithm specified in the JWT header
#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=allowed_algorithms,  # Allow all supported algorithms
#             options={
#                 "verify_signature": True,
#                 "verify_aud": False,  # Don't verify audience
#                 "verify_iat": False,  # Don't verify issued at time
#                 "verify_exp": True,   # Do verify expiration
#                 "verify_nbf": False,  # Don't verify not before
#                 "verify_iss": False,  # Don't verify issuer
#                 "verify_sub": False,  # Don't verify subject
#             }
#         )

#         # According to Better Auth config in server-auth.ts, the JWT has 'user_id' field
#         user_id: str = payload.get("user_id") or payload.get("jti") or payload.get("sub")
#         user_email: str = payload.get("email")  # Get email from token as well

#         if user_id is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Could not validate credentials: Missing user_id in token. Expected 'user_id', 'jti', or 'sub' field.",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )

#         # Just verify the token is valid and return the user_id
#         # The actual user validation happens at the application level if needed
#         return user_id
#     except JWTError as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=f"Could not validate credentials: {str(e)}",
#             headers={"WWW-Authenticate": "Bearer"},
#         )


# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
#     session: Session = Depends(get_session)
# ):
#     """
#     Get current user from JWT token
#     """
#     token = credentials.credentials
#     user_id = verify_jwt_token(token)

#     # Verify that the user exists in the backend database
#     # If not, create the user in the backend's users table based on JWT payload
#     statement = select(BackendUser).where(BackendUser.id == user_id)
#     user = session.exec(statement).first()

#     if not user:
#         # User doesn't exist in backend, extract info from JWT and create them
#         try:
#             # Use the same decoding approach as in verify_jwt_token to avoid algorithm errors
#             payload = jwt.decode(
#                 token,
#                 SECRET_KEY,
#                 algorithms=[ALGORITHM],
#                 options={
#                     "verify_signature": True,
#                     "verify_aud": False,
#                     "verify_iat": False,
#                     "verify_exp": True,
#                     "verify_nbf": False,
#                     "verify_iss": False,
#                     "verify_sub": False,
#                     "require_aud": False,
#                     "require_iat": False,
#                     "require_exp": False,
#                     "require_nbf": False,
#                     "require_iss": False,
#                     "require_sub": False,
#                 }
#             )
#             user_email = payload.get("email")

#             if user_email:
#                 # Create user in backend with the same ID as in Better Auth
#                 new_user = BackendUser(
#                     id=user_id,
#                     email=user_email,
#                     hashed_password="",  # Empty since Better Auth handles passwords
#                     created_at=datetime.utcnow(),
#                     updated_at=datetime.utcnow()
#                 )

#                 session.add(new_user)
#                 session.commit()
#                 session.refresh(new_user)  # Refresh to ensure the user is properly stored
#         except JWTError:
#             # If JWT decode fails, just return the user_id
#             pass

#     return user_id



# backend/auth.py
from datetime import datetime
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings
from sqlmodel import Session, select
from db import get_session
from models import User as BackendUser
import base64

security = HTTPBearer()

def verify_jwt_token(token: str) -> str:
    """
    Verify JWT token issued by Better Auth using the shared secret
    """
    try:
        # Decode the token using the shared secret
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"],  # Better Auth typically uses HS256 for symmetric encryption
            options={"verify_exp": True}  # Verify expiration
        )

        # Extract user_id from the token (Better Auth should put user_id in the payload)
        user_id = payload.get("user_id") or payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Authenticated token missing user identifier"
            )

        return user_id

    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Could not validate credentials: {str(e)}"
        )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """
    Get current user from JWT token issued by Better Auth
    """
    token = credentials.credentials
    user_id = verify_jwt_token(token)

    # Verify that the user exists in the backend database
    # If not, create the user in the backend's users table based on JWT payload
    statement = select(BackendUser).where(BackendUser.id == user_id)
    user = session.exec(statement).first()

    if not user:
        try:
            # Decode token again to get user details
            payload = jwt.decode(
                token,
                settings.BETTER_AUTH_SECRET,
                algorithms=["HS256"],
                options={"verify_exp": True}
            )
            user_email = payload.get("email")

            if user_email:
                # Create user in backend with the same ID as in Better Auth
                new_user = BackendUser(
                    id=user_id,
                    email=user_email,
                    hashed_password="",  # Empty since Better Auth handles passwords
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )

                session.add(new_user)
                session.commit()
                session.refresh(new_user)  # Refresh to ensure the user is properly stored
        except JWTError:
            # If JWT decode fails, just return the user_id
            pass

    return user_id
