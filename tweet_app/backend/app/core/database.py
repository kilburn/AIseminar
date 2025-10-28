from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import redis.asyncio as redis
try:
    from qdrant_client import QdrantClient
    from qdrant_client.async_client import AsyncQdrantClient
    QDRANT_AVAILABLE = True
except ImportError:
    QdrantClient = None
    AsyncQdrantClient = None
    QDRANT_AVAILABLE = False
from typing import Generator

from app.core.config import settings

# SQLAlchemy Database
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.debug
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis Client
redis_client = redis.from_url(settings.redis_url, decode_responses=True)

# Qdrant Clients (only initialize if available)
qdrant_client = QdrantClient(url=settings.qdrant_url) if QDRANT_AVAILABLE else None
async_qdrant_client = AsyncQdrantClient(url=settings.qdrant_url) if QDRANT_AVAILABLE else None


def get_db() -> Generator:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_redis() -> redis.Redis:
    """Get Redis client"""
    return redis_client


async def get_qdrant() -> AsyncQdrantClient:
    """Get Qdrant client"""
    return async_qdrant_client


def init_db() -> None:
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


async def init_qdrant_collection() -> None:
    """Initialize Qdrant collection for tweets"""
    if not QDRANT_AVAILABLE or async_qdrant_client is None:
        print("Qdrant client not available, skipping collection initialization")
        return

    try:
        from qdrant_client.models import Distance, VectorParams, QuantizationConfig

        collection_name = settings.qdrant_collection_name

        # Check if collection exists
        collections = await async_qdrant_client.get_collections()
        if collection_name in [c.name for c in collections.collections]:
            return

        # Create collection
        await async_qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=768,  # Sentence transformer embedding size
                distance=Distance.COSINE,
                hnsw_config={
                    "m": 16,
                    "ef_construct": 200,
                    "full_scan_threshold": 20000
                }
            ),
            quantization_config=QuantizationConfig(
                scalar={
                    "type": "int8",
                    "quantile": 0.99,
                    "always_ram": True
                }
            )
        )
    except Exception as e:
        print(f"Failed to initialize Qdrant collection: {e}")
        # Don't raise exception, allow application to start without Qdrant