# Qdrant Vector Database Schema

**Version**: 1.0.0
**Created**: 2025-10-28
**Status**: Draft

## Overview

This document defines the Qdrant vector database schema and configuration for the Tweet NLP application. Qdrant is used for efficient semantic search and similarity operations on tweet embeddings.

**Important**: This project uses a custom Qdrant Dockerfile (`qdrant.Dockerfile`) that extends the official Qdrant image to include curl for healthcheck functionality. The custom Dockerfile installs curl and ca-certificates to enable HTTP health checks against the Qdrant service.

## 1. Tweets Collection

```python
# Collection configuration
TWEETS_COLLECTION = {
    "vectors": {
        "size": 768,  # Sentence transformer embedding dimension
        "distance": "Cosine",
        "hnsw_config": {
            "m": 16,  # HNSW parameter
            "ef_construct": 200,  # Indexing time/accuracy tradeoff
            "full_scan_threshold": 20000  # Switch to full scan for small collections
        }
    },
    "payload_schema": {
        "tweet_id": "keyword",      # UUID from PostgreSQL
        "dataset_id": "keyword",    # Dataset UUID
        "text": "text",             # Original tweet text
        "sentiment": "keyword",     # Sentiment label
        "emotion": "keyword",       # Emotion label
        "offensive": "bool",        # Offensive language flag
        "language": "keyword",      # Language code
        "created_at": "integer",    # Unix timestamp for filtering
        "has_hashtags": "bool",     # Has hashtag presence
        "has_mentions": "bool",     # Has mention presence
        "char_count": "integer",    # Character count for filtering
        "word_count": "integer"     # Word count for filtering
    },
    "quantization_config": {
        "scalar": {
            "type": "int8",
            "quantile": 0.99,
            "always_ram": True
        }
    }
}
```

**Purpose**: Store and retrieve tweet embeddings for semantic search
**Key Features**:
- 768-dimensional embeddings from sentence transformers
- HNSW indexing for fast approximate nearest neighbor search
- Scalar quantization for memory efficiency
- Rich payload schema for metadata filtering
- Cosine distance metric for similarity computation

## 2. Search Operations

### Semantic Search Query

```python
semantic_search_query = {
    "vector": query_embedding,
    "limit": 20,
    "score_threshold": 0.5,
    "with_payload": True,
    "with_vector": False,
    "filter": {
        "must": [
            {"key": "sentiment", "match": {"value": "positive"}},
            {"key": "offensive", "match": {"value": False}},
            {"key": "created_at", "range": {"gte": start_timestamp, "lte": end_timestamp}}
        ]
    },
    "params": {
        "hnsw_ef": 128,  # Search accuracy vs speed tradeoff
        "exact": False   # Use approximate search
    }
}
```

**Use Case**: Find tweets semantically similar to a query
**Parameters**:
- `vector`: Query embedding (768-dimensional)
- `limit`: Maximum number of results
- `score_threshold`: Minimum similarity score (0-1)
- `hnsw_ef`: Trade-off between speed and accuracy
- `filter`: Apply sentiment, offensive language, and date range filters

### Hybrid Search Query

```python
hybrid_search_query = {
    "vector": query_embedding,
    "limit": 50,
    "score_threshold": 0.3,
    "with_payload": True,
    "filter": {
        "must": [
            {
                "key": "text",
                "match": {"text": "important keywords"}
            }
        ]
    }
}
```

**Use Case**: Combine semantic similarity with keyword matching
**Parameters**:
- `vector`: Query embedding for semantic similarity
- `filter`: Apply keyword text filtering
- `limit`: Larger limit for hybrid results

## 3. Collection Configuration Details

### Vector Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| `size` | 768 | Dimension of embeddings from sentence-transformers |
| `distance` | Cosine | Similarity metric (alternatives: Euclidean, Manhattan, Dot) |
| `hnsw_config.m` | 16 | Maximum connections per node in HNSW graph |
| `hnsw_config.ef_construct` | 200 | Trade-off between indexing time and accuracy |
| `full_scan_threshold` | 20000 | Size at which to use full scan instead of HNSW |

### Payload Schema Details

| Field | Type | Purpose |
|-------|------|---------|
| `tweet_id` | keyword | Reference to PostgreSQL tweet UUID |
| `dataset_id` | keyword | Reference to PostgreSQL dataset UUID |
| `text` | text | Full tweet text for keyword search |
| `sentiment` | keyword | Sentiment classification result |
| `emotion` | keyword | Emotion classification result |
| `offensive` | bool | Offensive language flag |
| `language` | keyword | Language code (e.g., 'en', 'es') |
| `created_at` | integer | Unix timestamp for date range filtering |
| `has_hashtags` | bool | Presence of hashtags in tweet |
| `has_mentions` | bool | Presence of mentions in tweet |
| `char_count` | integer | Character count for range filtering |
| `word_count` | integer | Word count for range filtering |

### Quantization Configuration

```python
"quantization_config": {
    "scalar": {
        "type": "int8",      # 8-bit integer quantization
        "quantile": 0.99,    # Use 99th percentile for quantization
        "always_ram": True   # Keep quantization values in RAM
    }
}
```

**Purpose**: Reduce memory footprint while maintaining search quality
**Benefits**:
- ~4x memory reduction compared to float32
- Minimal accuracy loss
- Faster similarity computations

## 4. Indexing Strategy

### HNSW (Hierarchical Navigable Small World)

The HNSW algorithm creates a hierarchical graph structure that enables fast approximate nearest neighbor search:

- **m=16**: Each node connects to at most 16 other nodes
- **ef_construct=200**: During index construction, maintain 200 candidates per layer
- **ef (search)=128**: During search, explore 128 candidates

**Trade-offs:**
- Higher `m` → Better recall, higher memory usage, slower inserts
- Higher `ef_construct` → Better index quality, slower construction
- Higher search `ef` → Better recall, slower queries

### Payload Indexing

Qdrant automatically creates indexes on payload fields for efficient filtering:

- **keyword fields**: Exact matching and set operations
- **text fields**: Full-text search capability
- **bool/integer fields**: Range queries and comparisons

## 5. Performance Considerations

### Memory Usage

```
Total Memory = Vector Size + Payload Size + Index Overhead

Per Vector:
- Float32 vector: 768 × 4 bytes = 3,072 bytes
- Int8 quantized: 768 × 1 byte = 768 bytes
- HNSW graph (m=16): ~64 bytes
- Payload overhead: Variable

Example for 1M vectors:
- Unquantized: ~3.2 GB
- Quantized: ~0.8 GB + payload
```

### Query Performance

**Typical latency (with 1M vectors):**
- Semantic search (top 20): 10-50ms
- Semantic + filters: 20-100ms
- Full collection scan: 100-500ms

**Optimization strategies:**
- Use filters to reduce search space
- Increase `ef_construct` for better recall
- Batch multiple queries
- Use scalar quantization for memory constraints

## 6. Migration from PostgreSQL

### Initial Load Strategy

```python
# Pseudocode for batch uploading vectors to Qdrant
def load_vectors_to_qdrant(batch_size=1000):
    for batch in get_tweets_in_batches(batch_size):
        # Generate embeddings for batch
        embeddings = embedding_model.encode([t.cleaned_text for t in batch])
        
        # Prepare points for Qdrant
        points = [
            PointStruct(
                id=hash(tweet.id),
                vector=embedding,
                payload={
                    "tweet_id": str(tweet.id),
                    "dataset_id": str(tweet.dataset_id),
                    "text": tweet.text,
                    "sentiment": analysis.sentiment,
                    "emotion": analysis.emotion,
                    "offensive": analysis.offensive_language,
                    "language": tweet.language,
                    "created_at": int(tweet.created_at.timestamp()),
                    "has_hashtags": tweet.hashtag_count > 0,
                    "has_mentions": tweet.mention_count > 0,
                    "char_count": tweet.character_count,
                    "word_count": tweet.word_count
                }
            )
            for tweet, embedding in zip(batch, embeddings)
        ]
        
        # Upload to Qdrant
        client.upsert(collection_name="tweets", points=points)
```

## 7. Docker Configuration

### Custom Dockerfile

The project uses a custom Qdrant Dockerfile (`qdrant.Dockerfile`) to add curl for healthcheck functionality:

```dockerfile
FROM qdrant/qdrant:v1.7.4

# Install curl for healthcheck and clean up apt cache
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*
```

**Why curl is needed:**
- Healthcheck endpoints for container orchestration
- Service discovery and monitoring
- API connectivity testing
- Container startup validation

**Usage in Docker Compose:**
The custom Dockerfile is referenced in `docker-compose.dev.yml` to build the Qdrant service with curl capabilities.

## 8. Backup and Recovery

### Collection Snapshots

```python
# Create a snapshot
snapshot_path = client.create_snapshot(collection_name="tweets")

# Restore from snapshot
client.recover_snapshot(collection_name="tweets", snapshot=snapshot_path)
```

**Best Practices:**
- Create snapshots before major operations
- Store snapshots in persistent storage (S3, etc.)
- Test recovery procedures regularly
- Keep multiple backup versions
