# Technical Architecture: TweetEval NLP Platform

**Version**: 1.0.0
**Created**: 2025-10-28
**Status**: Draft

## System Overview

The TweetEval NLP Platform is a cloud-native, microservices-based application that enables researchers and data scientists to analyze tweet datasets using state-of-the-art NLP models. The system follows a modular architecture with clear separation of concerns between data ingestion, processing, storage, and presentation layers.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  Vue.js 3 Application (TypeScript + Tailwind CSS)              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │ Dashboard   │ │ Search      │ │ Upload      │ │ Analytics   │ │
│  │ Component   │ │ Interface   │ │ Component   │ │ Dashboard   │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                  │
                              HTTP/HTTPS
                                  │
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                         │
├─────────────────────────────────────────────────────────────────┤
│                    Nginx Reverse Proxy                          │
│              (Load Balancing, SSL Termination)                 │
└─────────────────────────────────────────────────────────────────┘
                                  │
┌─────────────────────────────────────────────────────────────────┐
│                      Backend Services                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │   FastAPI       │ │   FastAPI       │ │   FastAPI       │   │
│  │  Core Service   │ │ Analysis Service│ │  Search Service │   │
│  │                 │ │                 │ │                 │   │
│  │ • Dataset Mgmt  │ │ • TweetEval     │ │ • Semantic      │   │
│  │ • File Upload   │ │ • Embeddings    │ │   Search        │   │
│  │ • Export        │ │ • Background    │ │ • Similarity    │   │
│  │                 │ │   Processing    │ │ • Ranking       │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                  │
        ┌─────────────────────────┐
        │                         │
┌─────────────┐         ┌─────────────────┐
│ PostgreSQL   │         │     Qdrant      │
│ Database     │         │ Vector Database │
│              │         │                 │
│ • Datasets   │         │ • Embeddings    │
│ • Tweets     │         │ • Semantic      │
│ • Analysis   │         │   Search        │
│ • Users      │         │ • Similarity    │
└─────────────┘         └─────────────────┘
```

## Component Details

### Frontend Layer

**Technology Stack:**
- Vue.js 3 with Composition API
- TypeScript for type safety
- Vite for development and build tooling
- Tailwind CSS for styling
- Pinia for state management
- Vue Router for navigation
- Chart.js and D3.js for visualizations

**Key Components:**

1. **Dashboard Component**
   - Overview statistics and metrics
   - Recent dataset activity
   - Processing status indicators
   - Quick access to main features

2. **Upload Component**
   - Drag-and-drop file interface
   - Format validation (CSV/JSON)
   - Real-time upload progress
   - Preprocessing options and settings

3. **Search Interface**
   - Natural language query input
   - Advanced filtering options
   - Results display with similarity scores
   - Export search results functionality

4. **Analytics Dashboard**
   - Interactive charts and visualizations
   - Time-series analysis
   - Correlation matrices
   - Custom report generation

### Backend Services

#### 1. Core Service (FastAPI)

**Responsibilities:**
- Dataset management (CRUD operations)
- File upload handling and validation
- User authentication and authorization
- Export job management
- API rate limiting and monitoring

**Key Endpoints:**
```
POST   /api/v1/datasets              # Create new dataset
GET    /api/v1/datasets              # List all datasets
GET    /api/v1/datasets/{id}         # Get dataset details
DELETE /api/v1/datasets/{id}         # Delete dataset
POST   /api/v1/datasets/{id}/export  # Export dataset results
```

#### 2. Analysis Service (FastAPI)

**Responsibilities:**
- TweetEval model inference
- Text embedding generation
- Background task coordination
- Batch processing management
- Model performance monitoring

**Key Endpoints:**
```
POST   /api/v1/analysis/process      # Start dataset processing
GET    /api/v1/analysis/status/{job_id}  # Get processing status
POST   /api/v1/analysis/sentiment    # Analyze sentiment for single text
POST   /api/v1/analysis/embeddings   # Generate embeddings for text
```

#### 3. Search Service (FastAPI)

**Responsibilities:**
- Semantic search functionality
- Similarity calculation and ranking
- Search result filtering
- Query optimization
- Search analytics

**Key Endpoints:**
```
POST   /api/v1/search/semantic       # Perform semantic search
GET    /api/v1/search/similar/{id}   # Find similar tweets
POST   /api/v1/search/filters        # Advanced filtered search
```

### Data Layer

#### PostgreSQL Database

**Schema Design:**
```sql
-- Datasets table
CREATE TABLE datasets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    file_name VARCHAR(255) NOT NULL,
    file_size BIGINT NOT NULL,
    tweet_count INTEGER DEFAULT 0,
    processing_status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tweets table
CREATE TABLE tweets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_id UUID REFERENCES datasets(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    original_id VARCHAR(255), -- Original tweet ID if available
    metadata JSONB, -- Additional tweet metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Analysis results table
CREATE TABLE analysis_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tweet_id UUID REFERENCES tweets(id) ON DELETE CASCADE,
    sentiment VARCHAR(20) NOT NULL, -- positive, negative, neutral
    sentiment_confidence FLOAT NOT NULL,
    emotion VARCHAR(50) NOT NULL, -- joy, sadness, anger, etc.
    emotion_confidence FLOAT NOT NULL,
    offensive_language BOOLEAN NOT NULL,
    offensive_confidence FLOAT NOT NULL,
    hate_speech VARCHAR(50), -- hateful, targeted, aggressive, none
    hate_confidence FLOAT,
    analyzed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Search history table
CREATE TABLE search_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query TEXT NOT NULL,
    filters JSONB,
    result_count INTEGER,
    execution_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Qdrant Vector Database

**Collection Configuration:**
```python
# Embeddings collection for semantic search
collection_config = {
    "vectors": {
        "size": 768,  # Sentence transformer embedding size
        "distance": "Cosine"
    },
    "payload_schema": {
        "tweet_id": "keyword",
        "dataset_id": "keyword",
        "sentiment": "keyword",
        "emotion": "keyword",
        "offensive": "bool"
    }
}
```

**Operations:**
- **Insert**: Store embeddings with metadata
- **Search**: Find similar vectors using cosine similarity
- **Filter**: Search with metadata filters
- **Update**: Modify vectors and metadata
- **Delete**: Remove embeddings for deleted tweets

## Security Architecture

### Authentication & Authorization

**Implementation:**
- JWT-based authentication with refresh tokens
- Role-based access control (RBAC)
- API key management for programmatic access
- OAuth2 integration for third-party authentication

**Security Layers:**
1. **Network Security**: TLS/SSL encryption, firewall rules
2. **Application Security**: Input validation, SQL injection prevention
3. **Data Security**: Encryption at rest and in transit
4. **Access Control**: Principle of least privilege

### Data Privacy

**Compliance Considerations:**
- GDPR compliance for EU users
- Data anonymization options
- Retention policies
- Right to deletion implementation

## Performance Considerations

### Scalability Design

**Horizontal Scaling:**
- Stateless backend services for easy scaling
- Database connection pooling
- Vector database sharding for large datasets
- CDN for static asset delivery

**Caching Strategy:**
- Database query result caching
- Embedding cache for frequently searched texts
- Static asset caching with CDN

### Monitoring & Observability

**Metrics Collection:**
- Application performance monitoring (APM)
- Database performance metrics
- Vector database query performance
- Background task processing times

**Logging Strategy:**
- Structured JSON logging
- Centralized log aggregation
- Error tracking and alerting
- Audit logging for sensitive operations

## Deployment Architecture

### Container Strategy

**Service Containers:**
1. **Frontend**: Nginx + Vue.js build artifacts
2. **Backend API**: FastAPI application
3. **Databases**: PostgreSQL, Qdrant
4. **Monitoring**: Prometheus, Grafana

### Infrastructure Requirements

**Minimum Resources:**
- **CPU**: 4 cores for processing, 2 cores for services
- **Memory**: 8GB RAM (4GB for databases, 4GB for applications)
- **Storage**: 100GB SSD (databases) + 50GB (application)
- **Network**: 1Gbps for data transfer

**Production Scaling:**
- **Application**: Auto-scaling based on CPU/memory usage
- **Database**: Read replicas for query scaling
- **Vector DB**: Horizontal scaling with sharding
- **Load Balancer**: Multiple availability zones

## Development Workflow

### Local Development

**Docker Compose Setup:**
```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/tweeteval
      - QDRANT_URL=http://qdrant:6333
    volumes:
      - ./backend:/app

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=tweeteval
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
```

This architecture provides a solid foundation for building a scalable, maintainable TweetEval NLP analysis platform that can handle large datasets while providing excellent user experience and performance.