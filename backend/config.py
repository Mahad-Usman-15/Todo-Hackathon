from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str
    BETTER_AUTH_SECRET: str
    BETTER_AUTH_URL: str = "http://localhost:3000"
    API_PREFIX: str = "/api"

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra environment variables


settings = Settings()


# backend/config.py
# backend/config.py
# backend/config.py

# from pydantic_settings import BaseSettings, SettingsConfigDict

# class Settings(BaseSettings):
#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         extra="ignore"  # ignore extra vars not defined below
#     )

#     DATABASE_URL: str
#     BETTER_AUTH_SECRET: str
#     BETTER_AUTH_URL: str
#     FRONTEND_URL: str = "http://localhost:3000"  # default if not provided

# settings = Settings()
