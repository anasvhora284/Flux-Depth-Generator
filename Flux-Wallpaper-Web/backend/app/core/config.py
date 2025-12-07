from pydantic_settings import BaseSettings
from typing import Optional, List
import secrets


class Settings(BaseSettings):
    PROJECT_NAME: str = "Flux Depth Generator API"
    API_V1_STR: str = "/api/v1"
    
    # Security - MUST set in production
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost/flux_depth_db"

    # CORS - Add your frontend URL in production
    BACKEND_CORS_ORIGINS: List[str] = []

    # Email Configuration
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.googlemail.com"
    MAIL_FROM_NAME: str = "Flux Depth Generator"
    
    # HTTP Email Provider (Brevo)
    EMAIL_API_KEY: str = ""

    # Image Processing
    MAX_BATCH_SIZE: int = 200
    BATCH_THRESHOLD: int = 5
    UPLOAD_DIR: str = "uploads"
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

