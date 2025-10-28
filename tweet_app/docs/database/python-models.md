# Python Data Models

**Version**: 1.0.0
**Created**: 2025-10-28
**Status**: Draft

## Overview

This document defines all Python Pydantic data models used in the Tweet NLP application. These models provide type validation, serialization, and documentation for API requests/responses and internal data structures.

## Base Models

### Base Schema

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
```

**Purpose**: Foundation for all Pydantic models with ORM compatibility

### Timestamp Mixin

```python
class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: Optional[datetime] = None
```

**Purpose**: Consistent timestamp fields across models

---

## 1. User Models

### UserRole Enum

```python
class UserRole(str, Enum):
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    ADMIN = "admin"
```

### UserCreate

```python
class UserCreate(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = Field(None, max_length=100)
    organization: Optional[str] = Field(None, max_length=255)
```

**Purpose**: Schema for user registration
**Validation Rules**:
- Username: 3-50 characters
- Email: Valid email format
- Password: Minimum 8 characters
- Full name: Optional, max 100 characters
- Organization: Optional, max 255 characters

### UserResponse

```python
class UserResponse(BaseSchema, TimestampMixin):
    id: uuid.UUID
    username: str
    email: str
    full_name: Optional[str]
    organization: Optional[str]
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime]
    role: UserRole = UserRole.RESEARCHER
```

**Purpose**: Schema for user data in API responses
**Note**: Does not include password_hash for security

### UserUpdate

```python
class UserUpdate(BaseSchema):
    full_name: Optional[str] = Field(None, max_length=100)
    organization: Optional[str] = Field(None, max_length=255)
    email: Optional[str] = Field(None, regex=r'^[^@]+@[^@]+\.[^@]+$')
```

**Purpose**: Schema for user profile updates
**Validation**: All fields are optional

---

## 2. Dataset Models

### ProcessingStatus Enum

```python
class ProcessingStatus(str, Enum):
    PENDING = "pending"
    UPLOADING = "uploading"
    VALIDATING = "validating"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
```

### DatasetCreate

```python
class DatasetCreate(BaseSchema):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    is_public: bool = False
    settings: Optional[Dict[str, Any]] = {}
```

**Purpose**: Schema for dataset creation
**Fields**:
- `name`: Required, 1-255 characters
- `description`: Optional markdown text
- `is_public`: Access control flag
- `settings`: Custom processing settings

### DatasetResponse

```python
class DatasetResponse(BaseSchema, TimestampMixin):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    description: Optional[str]
    file_name: str
    file_size: int
    mime_type: str
    total_rows: int
    processed_rows: int
    failed_rows: int
    processing_status: ProcessingStatus
    processing_started_at: Optional[datetime]
    processing_completed_at: Optional[datetime]
    error_message: Optional[str]
    metadata: Dict[str, Any]
    settings: Dict[str, Any]
    is_public: bool
```

**Purpose**: Complete dataset information in API responses
**Includes**: File metadata, processing progress, and error information

### DatasetUpdate

```python
class DatasetUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_public: Optional[bool] = None
    settings: Optional[Dict[str, Any]] = None
```

**Purpose**: Schema for dataset updates
**Note**: All fields optional for partial updates

---

## 3. Tweet Models

### TweetCreate

```python
class TweetCreate(BaseSchema):
    original_id: Optional[str] = None
    text: str = Field(..., min_length=1)
    language: str = "en"
    metadata: Optional[Dict[str, Any]] = {}
```

**Purpose**: Schema for adding tweets to a dataset
**Fields**:
- `original_id`: Optional external ID (e.g., Twitter API ID)
- `text`: Required tweet content
- `language`: ISO language code, defaults to 'en'
- `metadata`: Additional tweet metadata

### TweetResponse

```python
class TweetResponse(BaseSchema, TimestampMixin):
    id: uuid.UUID
    dataset_id: uuid.UUID
    original_id: Optional[str]
    text: str
    cleaned_text: Optional[str]
    language: str
    character_count: Optional[int]
    word_count: Optional[int]
    hashtag_count: int
    mention_count: int
    url_count: int
    created_at: Optional[datetime]
    processed_at: datetime
    metadata: Dict[str, Any]
    is_valid: bool
    validation_errors: Optional[List[str]]
    processing_errors: Optional[List[str]]
    qdrant_id: Optional[str]
```

**Purpose**: Complete tweet information including preprocessing results
**Fields**:
- `cleaned_text`: Preprocessed text after NLP cleaning
- `character_count`, `word_count`: Text statistics
- `hashtag_count`, `mention_count`, `url_count`: Extracted features
- `is_valid`: Validation status flag
- `qdrant_id`: Reference to vector embedding

### TweetAnalysisResponse

```python
class TweetAnalysisResponse(BaseSchema):
    tweet: TweetResponse
    analysis: "AnalysisResultResponse"
```

**Purpose**: Combined tweet and analysis data
**Use Case**: API endpoint returning tweet with its NLP analysis

---

## 4. Analysis Result Models

### Sentiment Enum

```python
class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
```

### Emotion Enum

```python
class EmotionLabel(str, Enum):
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    OTHERS = "others"
```

### Hate Speech Enum

```python
class HateSpeechLabel(str, Enum):
    HATEFUL = "hateful"
    TARGETED = "targeted"
    AGGRESSIVE = "aggressive"
    NONE = "none"
```

### AnalysisResultResponse

```python
class AnalysisResultResponse(BaseSchema, TimestampMixin):
    id: uuid.UUID
    tweet_id: uuid.UUID
    model_version: str

    # Sentiment
    sentiment: SentimentLabel
    sentiment_confidence: float = Field(..., ge=0, le=1)
    sentiment_scores: Dict[str, float]

    # Emotion
    emotion: EmotionLabel
    emotion_confidence: float = Field(..., ge=0, le=1)
    emotion_scores: Dict[str, float]

    # Offensive language
    offensive_language: bool
    offensive_confidence: float = Field(..., ge=0, le=1)
    offensive_scores: Dict[str, float]

    # Hate speech
    hate_speech: Optional[HateSpeechLabel]
    hate_confidence: Optional[float] = Field(None, ge=0, le=1)
    hate_scores: Optional[Dict[str, float]]

    # Irony
    irony: Optional[bool]
    irony_confidence: Optional[float] = Field(None, ge=0, le=1)

    # Processing metadata
    processing_time_ms: Optional[int]
    model_used: Optional[str]
    analyzed_at: datetime
    confidence_threshold: float
    is_high_confidence: bool
```

**Purpose**: Complete NLP analysis results
**Features**:
- Multi-label predictions (sentiment, emotion, offensive, hate speech, irony)
- Confidence scores for each prediction (0-1)
- Full probability distributions for all labels
- Model version tracking for reproducibility
- High-confidence flag based on threshold

**Confidence Ranges**:
- All confidence scores must be between 0 and 1 (exclusive of endpoints)
- Typical threshold: 0.5 or higher for production use

---

## 5. Search Models

### SearchQuery

```python
class SearchQuery(BaseSchema):
    query: str = Field(..., min_length=1)
    query_type: str = "semantic"
    filters: Optional[Dict[str, Any]] = {}
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)
    similarity_threshold: float = Field(0.5, ge=0, le=1)
```

**Purpose**: Schema for search requests
**Validation**:
- Query: Non-empty string
- Limit: 1-100 results
- Offset: Non-negative
- Similarity threshold: 0-1

**Query Types**:
- `semantic`: Vector similarity search
- `keyword`: Full-text search
- `hybrid`: Combination of both

### SearchFilters

```python
class SearchFilters(BaseSchema):
    sentiment: Optional[List[SentimentLabel]] = None
    emotion: Optional[List[EmotionLabel]] = None
    offensive_language: Optional[bool] = None
    hate_speech: Optional[List[HateSpeechLabel]] = None
    language: Optional[str] = None
    date_range: Optional[Dict[str, datetime]] = None
    confidence_threshold: Optional[float] = Field(None, ge=0, le=1)
    character_count_range: Optional[Dict[str, int]] = None
    word_count_range: Optional[Dict[str, int]] = None
```

**Purpose**: Optional filters for refining searches
**Examples**:
```python
filters = SearchFilters(
    sentiment=["positive"],
    emotion=["joy", "surprise"],
    offensive_language=False,
    date_range={"start": datetime(2025, 1, 1), "end": datetime(2025, 12, 31)},
    confidence_threshold=0.7
)
```

### SearchResult

```python
class SearchResult(BaseSchema):
    tweet_id: uuid.UUID
    text: str
    similarity_score: float
    analysis: Optional[AnalysisResultResponse]
    metadata: Dict[str, Any]
```

**Purpose**: Individual search result
**Fields**:
- `similarity_score`: Cosine similarity (0-1) for semantic search
- `analysis`: Full analysis results if available
- `metadata`: Additional tweet metadata

### SearchResponse

```python
class SearchResponse(BaseSchema):
    results: List[SearchResult]
    total_count: int
    query_time_ms: int
    max_similarity: float
    avg_similarity: float
```

**Purpose**: Complete search response with metrics
**Performance Metrics**:
- `query_time_ms`: Total query execution time
- `max_similarity`: Highest similarity score in results
- `avg_similarity`: Average similarity across results

---

## 6. Export Models

### ExportType Enum

```python
class ExportType(str, Enum):
    CSV = "csv"
    JSON = "json"
    PDF = "pdf"
    EXCEL = "excel"
```

### ExportJobCreate

```python
class ExportJobCreate(BaseSchema):
    dataset_id: uuid.UUID
    export_type: ExportType
    format_options: Optional[Dict[str, Any]] = {}
    filters: Optional[Dict[str, Any]] = {}
```

**Purpose**: Schema for initiating export jobs
**Format Options Examples**:
```python
# CSV options
format_options = {"delimiter": ",", "include_headers": True}

# PDF options
format_options = {"page_size": "A4", "include_charts": True}

# Excel options
format_options = {"sheet_name": "tweets", "include_analysis": True}
```

### ExportJobResponse

```python
class ExportJobResponse(BaseSchema, TimestampMixin):
    id: uuid.UUID
    user_id: uuid.UUID
    dataset_id: uuid.UUID
    export_type: ExportType
    format_options: Dict[str, Any]
    filters: Dict[str, Any]
    status: ProcessingStatus
    progress_percentage: int
    file_path: Optional[str]
    file_name: Optional[str]
    file_size: Optional[int]
    download_url: Optional[str]
    expires_at: Optional[datetime]
    total_records: Optional[int]
    processed_records: int
    processing_time_ms: Optional[int]
    error_message: Optional[str]
    completed_at: Optional[datetime]
```

**Purpose**: Export job status and information
**Lifecycle**:
1. Status: `pending` → Download URL: None
2. Status: `processing` → Progress updates
3. Status: `completed` → Download URL available, expires_at set
4. Status: `failed` → Error message populated

---

## 7. Data Validation Rules

### Common Validators

```python
from pydantic import validator

class ValidatedSchema(BaseSchema):
    @validator('email')
    def validate_email(cls, v):
        if not v or '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()

    @validator('confidence_threshold')
    def validate_confidence(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Confidence must be between 0 and 1')
        return v

    @validator('date_range')
    def validate_date_range(cls, v):
        if v and 'start' in v and 'end' in v:
            if v['start'] > v['end']:
                raise ValueError('Start date must be before end date')
        return v
```

### Validation Best Practices

1. **String Length**: Use `min_length` and `max_length`
2. **Numeric Ranges**: Use `ge` (greater or equal) and `le` (less or equal)
3. **Format Validation**: Use regex patterns for emails, URLs, etc.
4. **Cross-field Validation**: Use `@validator` with `values` parameter
5. **Enum Validation**: Use Enum classes for restricted values

---

## 8. Model Relationships

```
User
├── Dataset (user_id)
│   ├── Tweet (dataset_id)
│   │   └── AnalysisResult (tweet_id)
│   └── ExportJob (dataset_id)
└── SearchHistory (user_id)
```

**Foreign Key References**:
- `User.id` → `Dataset.user_id`
- `Dataset.id` → `Tweet.dataset_id`
- `Tweet.id` → `AnalysisResult.tweet_id`
- `User.id` → `ExportJob.user_id`
- `Dataset.id` → `ExportJob.dataset_id`

---

## 9. Serialization Examples

### Converting ORM Objects to Response Models

```python
from sqlalchemy.orm import Session

# Single object
def get_tweet_response(tweet: TweetORM) -> TweetResponse:
    return TweetResponse.from_orm(tweet)

# List of objects
def get_tweets_response(tweets: List[TweetORM]) -> List[TweetResponse]:
    return [TweetResponse.from_orm(t) for t in tweets]

# With nested relationships
def get_tweet_analysis_response(tweet: TweetORM, analysis: AnalysisResultORM) -> TweetAnalysisResponse:
    return TweetAnalysisResponse(
        tweet=TweetResponse.from_orm(tweet),
        analysis=AnalysisResultResponse.from_orm(analysis)
    )
```

### JSON Serialization

```python
import json

# To JSON
response_data = tweet_response.json()

# With custom settings
response_data = tweet_response.json(
    exclude_none=True,  # Exclude None values
    exclude_unset=True,  # Exclude unset fields
    indent=2
)

# Parse from JSON
tweet_data = json.loads(response_json)
tweet_response = TweetResponse(**tweet_data)
```
