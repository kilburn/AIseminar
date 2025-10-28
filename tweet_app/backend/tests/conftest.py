import pytest
import asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient

from app.main import app
from app.core.config import settings
from app.core.database import get_db, Base
from app.models import user, dataset, tweet, analysis_result


# Test database URL (in-memory SQLite for tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
    class_=AsyncSession,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with database dependency override."""
    def override_get_db():
        return db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def sync_client() -> TestClient:
    """Create a synchronous test client."""
    return TestClient(app)


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "organization": "Test Organization"
    }


@pytest.fixture
def sample_dataset_data():
    """Sample dataset data for testing."""
    return {
        "name": "Test Dataset",
        "description": "A test dataset for unit testing",
        "is_public": False,
        "settings": {
            "processing_batch_size": 100,
            "sentiment_threshold": 0.5
        }
    }


@pytest.fixture
def sample_tweet_data():
    """Sample tweet data for testing."""
    return {
        "original_id": "1234567890",
        "text": "This is a sample tweet for testing purposes. It's a happy tweet! 😊",
        "language": "en",
        "metadata": {
            "likes": 10,
            "retweets": 5,
            "hashtags": ["#testing", "#sample"],
            "mentions": ["@test"]
        }
    }


@pytest.fixture
def sample_analysis_result():
    """Sample analysis result for testing."""
    return {
        "sentiment": "positive",
        "sentiment_confidence": 0.85,
        "sentiment_scores": {
            "positive": 0.85,
            "negative": 0.05,
            "neutral": 0.10
        },
        "emotion": "joy",
        "emotion_confidence": 0.78,
        "emotion_scores": {
            "joy": 0.78,
            "sadness": 0.05,
            "anger": 0.02,
            "fear": 0.03,
            "surprise": 0.08,
            "disgust": 0.02,
            "others": 0.02
        },
        "offensive_language": False,
        "offensive_confidence": 0.95,
        "offensive_scores": {
            "offensive": 0.05,
            "not_offensive": 0.95
        },
        "hate_speech": None,
        "hate_confidence": None,
        "hate_scores": None,
        "irony": False,
        "irony_confidence": 0.92,
        "processing_time_ms": 150,
        "model_used": "tweeteval-v1",
        "confidence_threshold": 0.5
    }