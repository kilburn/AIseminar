# Database Documentation Index

**Version**: 1.0.0
**Last Updated**: 2025-10-28
**Status**: Draft

## 📚 Overview

This directory contains comprehensive documentation for the Tweet NLP platform's database architecture, split into three focused documents for easier navigation and maintenance.

The database consists of:
- **PostgreSQL**: Relational data storage for structured information
- **Qdrant**: Vector database for semantic search and similarity operations
- **Python Models**: Pydantic schemas for API validation and ORM mapping

---

## 📖 Documentation Files

### 1. [`postgres.md`](./postgres.md) - PostgreSQL Schema
**For**: Backend developers, DBAs, database architects

**Contains**:
- 7 main tables (Users, Datasets, Tweets, Analysis Results, Search History, Export Jobs, System Config)
- Index strategies for performance optimization
- Query optimization patterns
- Data archiving and partitioning strategies
- Relationship diagram and constraints

**When to read**:
- Setting up the database
- Designing database queries
- Understanding data relationships
- Optimizing query performance
- Planning backup/recovery procedures

**Key Tables**:
```
users → datasets → tweets → analysis_results
              ↓
          export_jobs → (stores export jobs)
              ↓
          search_history → (tracks searches)
```

---

### 2. [`qdrant.md`](./qdrant.md) - Qdrant Vector Database Schema
**For**: ML engineers, search specialists, backend developers

**Contains**:
- Tweets vector collection configuration (768-dimensional embeddings)
- Semantic search query patterns
- Hybrid search (semantic + keyword) implementation
- HNSW indexing strategy and parameters
- Scalar quantization for memory efficiency
- Performance considerations and optimization
- Migration strategy from PostgreSQL
- Backup and recovery procedures

**When to read**:
- Implementing semantic search
- Tuning search performance
- Understanding embedding storage
- Planning vector database optimization
- Monitoring search latency

**Collection Structure**:
```
TWEETS_COLLECTION
├── Vectors: 768-dimensional embeddings
├── Payload: Tweet metadata and analysis results
├── Index: HNSW (Hierarchical Navigable Small World)
└── Quantization: Scalar int8 for memory efficiency
```

---

### 3. [`python-models.md`](./python-models.md) - Python Data Models
**For**: API developers, frontend developers, data engineers

**Contains**:
- Base model classes and mixins
- User management models
- Dataset models with processing status
- Tweet models with preprocessing fields
- Analysis result models with confidence scores
- Search request/response models
- Export job models
- Data validation rules and best practices
- Model serialization examples
- Relationships between models

**When to read**:
- Developing API endpoints
- Understanding request/response formats
- Implementing data validation
- Creating ORM mappings
- Working with API clients

**Model Hierarchy**:
```
BaseSchema (ORM-compatible base)
├── UserResponse
├── DatasetResponse
├── TweetResponse
├── AnalysisResultResponse
├── SearchQuery / SearchResponse
└── ExportJobResponse
```

---

## 🔄 Quick Navigation

### By Use Case

**I want to...**

| Task | Document | Section |
|------|----------|---------|
| Create database schema | [`postgres.md`](./postgres.md) | Tables 1-7 |
| Query tweets efficiently | [`postgres.md`](./postgres.md) | Query Optimization, Indexing Strategy |
| Implement semantic search | [`qdrant.md`](./qdrant.md) | Semantic Search Query, HNSW Indexing |
| Add a new API endpoint | [`python-models.md`](./python-models.md) | User/Dataset/Tweet/Analysis Models |
| Optimize search performance | [`qdrant.md`](./qdrant.md) | Performance Considerations, Quantization |
| Set up data export | [`postgres.md`](./postgres.md) | Export Jobs Table |
| Validate API input | [`python-models.md`](./python-models.md) | Data Validation Rules |
| Load vectors to Qdrant | [`qdrant.md`](./qdrant.md) | Migration from PostgreSQL |

### By Role

**Database Administrator**
- Start with: [`postgres.md`](./postgres.md)
- Review: Indexing, partitioning, backup strategies
- Monitor: Query performance, table sizes

**Backend/API Developer**
- Start with: [`python-models.md`](./python-models.md)
- Reference: [`postgres.md`](./postgres.md) for queries
- Use: Model examples for endpoint implementation

**Machine Learning Engineer**
- Start with: [`qdrant.md`](./qdrant.md)
- Reference: [`python-models.md`](./python-models.md) for model structures
- Focus on: Embedding generation, search tuning

**Frontend Developer**
- Start with: [`python-models.md`](./python-models.md)
- Focus on: API response formats, validation errors
- Reference: Model examples for form handling

---

## 🔑 Key Concepts

### Data Flow

```
User Upload
    ↓
Dataset (PostgreSQL)
    ↓
Tweet Extraction & Cleaning
    ↓
Analysis (NLP Models)
    ├→ PostgreSQL (analysis_results table)
    └→ Qdrant (Tweet embeddings collection)
    ↓
Search/Export Operations
```

### Database Separation

| Concern | Database | Reason |
|---------|----------|--------|
| Structured data | PostgreSQL | ACID compliance, complex queries, relationships |
| Semantic search | Qdrant | Vector similarity, fast approximate search |
| API validation | Python Models | Type safety, auto-documentation |

### Performance Optimization Layers

1. **Database Level**: Indexes, partitioning (PostgreSQL)
2. **Vector Level**: HNSW, quantization (Qdrant)
3. **API Level**: Pagination, filtering, caching (Python)

---

## 📊 Schema Statistics

### PostgreSQL

| Table | Purpose | Est. Growth |
|-------|---------|------------|
| users | User accounts | Slow |
| datasets | Dataset metadata | Medium |
| tweets | Tweet content | Fast |
| analysis_results | NLP results | Fast |
| search_history | Query log | Medium |
| export_jobs | Export tracking | Slow |
| system_config | Settings | Static |

### Qdrant

| Collection | Size | Dimension | Growth |
|------------|------|-----------|--------|
| tweets | Grows with tweets | 768 | Fast |

---

## 🔗 Related Documentation

- **Backend Architecture**: See main README.md
- **API Specification**: See API docs
- **NLP Models**: See models documentation
- **Infrastructure**: See Docker/deployment docs

---

## ✅ Maintenance Checklist

- [ ] Review and update indexes quarterly
- [ ] Monitor Qdrant collection size
- [ ] Verify backup procedures monthly
- [ ] Update model versions in analysis_results
- [ ] Clean up expired export files
- [ ] Archive old search history
- [ ] Review and test partition archival strategy

---

## 📝 Notes

- All timestamps are stored with timezone awareness
- UUIDs are used for primary keys (distributed systems friendly)
- JSONB fields provide schema flexibility
- Foreign key constraints ensure referential integrity
- Vector embeddings use 768-dimensional sentence transformers
- Confidence scores are normalized to [0, 1] range

---

## 🚀 Getting Started

1. **First time setup**: Read [`postgres.md`](./postgres.md) Table 1-7 to understand all tables
2. **API development**: Reference [`python-models.md`](./python-models.md) for request/response formats
3. **Search implementation**: Study [`qdrant.md`](./qdrant.md) for semantic search patterns
4. **Performance tuning**: Refer to optimization sections in relevant documents

---

**For questions or updates to this documentation, please refer to the main project README or contact the data team.**
