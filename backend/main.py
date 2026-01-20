import sys
import os
import logging
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from config import settings
from db import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Todo Backend API",
    description="A secure task management API with user isolation, authentication via JWT tokens, and persistent storage using SQLModel ORM with Neon Serverless PostgreSQL.",
    version="1.0.0",
    # contact={
    #     "name": "Todo App Team",
    #     "url": "https://todoapp.com/support",
    #     "email": "support@todoapp.com",
    # },
    # license_info={
    #     "name": "MIT License",
    #     "url": "https://opensource.org/licenses/MIT",
    # },
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend Next.js app
        "http://localhost:8000",  # Backend API for direct calls if needed
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ],  # In production, change this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include the auth routes for backend user management
from routes.auth import router as auth_router
app.include_router(auth_router)

# Include the task routes
from routes.tasks import router as tasks_router
app.include_router(tasks_router)

# Add authentication dependencies to task routes instead of global middleware
# This allows auth endpoints to remain public while protecting task endpoints


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.on_event("shutdown")
def on_shutdown():
    """Cleanup operations when the application shuts down"""
    logger.info("Shutting down the application...")
    # Any cleanup operations for database connections or resources
    # In this case, SQLModel/FastAPI handles the connection pools automatically
    logger.info("Application shutdown completed")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Backend API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": [
                {
                    "loc": error["loc"],
                    "msg": error["msg"],
                    "type": error["type"]
                } for error in exc.errors()
            ]
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )






# backend/main.py


# import sys, os, logging
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import JSONResponse
# from starlette.exceptions import HTTPException as StarletteHTTPException
# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.util import get_remote_address
# from slowapi.errors import RateLimitExceeded
# from config import settings
# from db import create_db_and_tables

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# limiter = Limiter(key_func=get_remote_address)

# app = FastAPI(
#     title="Todo Backend API",
#     description="Secure task management API with Better Auth and strict user isolation.",
#     version="1.0.1"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[settings.FRONTEND_URL],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# from routes.auth import router as auth_router
# from routes.tasks import router as tasks_router

# app.include_router(auth_router, prefix="/auth")
# app.include_router(tasks_router, prefix="/api")

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()
#     logger.info("Database tables created/verified.")

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Todo Backend API"}

# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return JSONResponse(status_code=422, content={"detail": exc.errors()})
