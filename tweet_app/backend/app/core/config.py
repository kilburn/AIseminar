from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Optional, Union
import os


class Settings(BaseSettings):
    """Application settings"""

    # Application
    app_name: str = "TweetEval NLP Platform"
    version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    api_v1_str: str = "/api/v1"

    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    jwt_secret_key: str = "dev-jwt-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # CORS
    cors_origins: Union[List[str], str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ]

    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # Database
    database_url: str = "postgresql://tweeteval_user:tweeteval_pass@localhost:5432/tweeteval"

    # Vector Database
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection_name: str = "tweets"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # File Upload
    max_upload_size: int = 100 * 1024 * 1024  # 100MB
    upload_dir: str = "./uploads"
    export_dir: str = "./exports"
    allowed_mime_types: List[str] = [
        "text/csv",
        "application/json",
        "text/plain"
    ]

    # NLP Models
    sentiment_model: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    emotion_model: str = "cardiffnlp/twitter-roberta-base-emotion"
    offensive_model: str = "cardiffnlp/twitter-roberta-base-offensive"
    embedding_model: str = "all-MiniLM-L6-v2"

    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Processing
    batch_size: int = 100
    max_workers: int = 2
    processing_timeout: int = 3600  # 1 hour

    # Search
    default_search_limit: int = 20
    max_search_limit: int = 100
    similarity_threshold: float = 0.5

    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()

# Ensure upload and export directories exist
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(settings.export_dir, exist_ok=True)