# PostgreSQL Schema

**Version**: 1.0.0
**Created**: 2025-10-28
**Status**: Draft

## Overview

This document defines the complete PostgreSQL database schema for the Tweet NLP application. The design supports efficient storage, retrieval, and analysis of tweet datasets with NLP processing results.

## 1. Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    organization VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_active ON users(is_active);
```

**Purpose**: User authentication and account management
**Key Features**:
- Secure password storage with bcrypt
- Email verification workflow
- Organization tracking for analytics

## 2. Datasets Table

```sql
CREATE TABLE datasets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    file_hash VARCHAR(64) NOT NULL, -- SHA-256 hash for integrity
    mime_type VARCHAR(100) NOT NULL,
    encoding VARCHAR(50) DEFAULT 'utf-8',
    delimiter VARCHAR(10) DEFAULT ',',
    has_header BOOLEAN DEFAULT true,
    total_rows INTEGER DEFAULT 0,
    processed_rows INTEGER DEFAULT 0,
    failed_rows INTEGER DEFAULT 0,
    processing_status VARCHAR(50) DEFAULT 'pending' CHECK (
        processing_status IN ('pending', 'uploading', 'validating', 'processing', 'completed', 'failed', 'cancelled')
    ),
    processing_started_at TIMESTAMP WITH TIME ZONE,
    processing_completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    metadata JSONB DEFAULT '{}', -- Additional dataset metadata
    settings JSONB DEFAULT '{}', -- Processing settings and preferences
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_datasets_user_id ON datasets(user_id);
CREATE INDEX idx_datasets_status ON datasets(processing_status);
CREATE INDEX idx_datasets_created_at ON datasets(created_at);
CREATE INDEX idx_datasets_public ON datasets(is_public);
CREATE INDEX idx_datasets_file_hash ON datasets(file_hash);
```

**Purpose**: Dataset metadata and processing tracking
**Key Features**:
- File integrity verification with SHA-256
- Processing progress tracking
- Flexible metadata storage
- Public/private dataset access control

## 3. Tweets Table

```sql
CREATE TABLE tweets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_id UUID NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    original_id VARCHAR(255), -- Original tweet ID if available
    text TEXT NOT NULL,
    cleaned_text TEXT, -- Preprocessed text for analysis
    language VARCHAR(10) DEFAULT 'en',
    character_count INTEGER,
    word_count INTEGER,
    hashtag_count INTEGER DEFAULT 0,
    mention_count INTEGER DEFAULT 0,
    url_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE, -- Original tweet creation time
    processed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}', -- Tweet metadata (likes, retweets, etc.)
    is_valid BOOLEAN DEFAULT true,
    validation_errors TEXT[],
    processing_errors TEXT[],
    qdrant_id VARCHAR(255), -- Reference to Qdrant vector ID
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_tweets_dataset_id ON tweets(dataset_id);
CREATE INDEX idx_tweets_original_id ON tweets(original_id);
CREATE INDEX idx_tweets_language ON tweets(language);
CREATE INDEX idx_tweets_processed_at ON tweets(processed_at);
CREATE INDEX idx_tweets_is_valid ON tweets(is_valid);
CREATE INDEX idx_tweets_qdrant_id ON tweets(qdrant_id);

-- Full-text search index
CREATE INDEX idx_tweets_text_gin ON tweets USING gin(to_tsvector('english', text));
```

**Purpose**: Store individual tweet data and preprocessing results
**Key Features**:
- Text cleaning and preprocessing
- Metadata extraction (hashtags, mentions, URLs)
- Processing error tracking
- Full-text search capability

## 4. Analysis Results Table

```sql
CREATE TABLE analysis_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tweet_id UUID NOT NULL REFERENCES tweets(id) ON DELETE CASCADE,
    model_version VARCHAR(50) NOT NULL DEFAULT 'tweeteval-v1',

    -- Sentiment Analysis
    sentiment VARCHAR(20) NOT NULL CHECK (sentiment IN ('positive', 'negative', 'neutral')),
    sentiment_confidence FLOAT NOT NULL CHECK (sentiment_confidence >= 0 AND sentiment_confidence <= 1),
    sentiment_scores JSONB DEFAULT '{}', -- All sentiment probabilities

    -- Emotion Classification
    emotion VARCHAR(50) NOT NULL CHECK (emotion IN ('joy', 'sadness', 'anger', 'fear', 'surprise', 'disgust', 'others')),
    emotion_confidence FLOAT NOT NULL CHECK (emotion_confidence >= 0 AND emotion_confidence <= 1),
    emotion_scores JSONB DEFAULT '{}', -- All emotion probabilities

    -- Offensive Language Detection
    offensive_language BOOLEAN NOT NULL,
    offensive_confidence FLOAT NOT NULL CHECK (offensive_confidence >= 0 AND offensive_confidence <= 1),
    offensive_scores JSONB DEFAULT '{}', -- Offensive classification probabilities

    -- Hate Speech Detection
    hate_speech VARCHAR(50) CHECK (hate_speech IN ('hateful', 'targeted', 'aggressive', 'none')),
    hate_confidence FLOAT CHECK (hate_confidence >= 0 AND hate_confidence <= 1),
    hate_scores JSONB DEFAULT '{}', -- Hate speech probabilities

    -- Irony Detection
    irony BOOLEAN,
    irony_confidence FLOAT CHECK (irony_confidence >= 0 AND irony_confidence <= 1),

    -- Processing metadata
    processing_time_ms INTEGER,
    model_used VARCHAR(100),
    analyzed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Quality metrics
    confidence_threshold FLOAT DEFAULT 0.5,
    is_high_confidence BOOLEAN GENERATED ALWAYS AS (
        (sentiment_confidence >= confidence_threshold AND
         emotion_confidence >= confidence_threshold AND
         offensive_confidence >= confidence_threshold)
    ) STORED
);

-- Indexes for performance
CREATE INDEX idx_analysis_tweet_id ON analysis_results(tweet_id);
CREATE INDEX idx_analysis_sentiment ON analysis_results(sentiment);
CREATE INDEX idx_analysis_emotion ON analysis_results(emotion);
CREATE INDEX idx_analysis_offensive ON analysis_results(offensive_language);
CREATE INDEX idx_analysis_hate_speech ON analysis_results(hate_speech);
CREATE INDEX idx_analysis_high_confidence ON analysis_results(is_high_confidence);
CREATE INDEX idx_analysis_analyzed_at ON analysis_results(analyzed_at);
```

**Purpose**: Store NLP analysis results from TweetEval models
**Key Features**:
- Complete sentiment, emotion, and offensive language analysis
- Confidence scores for all predictions
- Model version tracking for reproducibility
- High-confidence result filtering

## 5. Search History Table

```sql
CREATE TABLE search_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    session_id VARCHAR(255),
    query TEXT NOT NULL,
    query_type VARCHAR(50) DEFAULT 'semantic' CHECK (query_type IN ('semantic', 'keyword', 'hybrid')),

    -- Search parameters
    filters JSONB DEFAULT '{}', -- Applied filters (sentiment, emotion, date range, etc.)
    limit INTEGER DEFAULT 20,
    offset INTEGER DEFAULT 0,

    -- Results
    result_count INTEGER NOT NULL,
    result_ids UUID[], -- Array of tweet IDs returned
    max_similarity FLOAT,
    avg_similarity FLOAT,

    -- Performance metrics
    execution_time_ms INTEGER,
    vector_search_time_ms INTEGER,
    filter_time_ms INTEGER,

    -- Metadata
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_search_user_id ON search_history(user_id);
CREATE INDEX idx_search_session_id ON search_history(session_id);
CREATE INDEX idx_search_created_at ON search_history(created_at);
CREATE INDEX idx_search_query_gin ON search_history USING gin(to_tsvector('english', query));
```

**Purpose**: Track search queries for analytics and optimization
**Key Features**:
- Query performance tracking
- Search analytics
- User behavior analysis

## 6. Export Jobs Table

```sql
CREATE TABLE export_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    dataset_id UUID REFERENCES datasets(id) ON DELETE CASCADE,

    -- Export configuration
    export_type VARCHAR(50) NOT NULL CHECK (export_type IN ('csv', 'json', 'pdf', 'excel')),
    format_options JSONB DEFAULT '{}',
    filters JSONB DEFAULT '{}', -- Applied filters for export

    -- Processing status
    status VARCHAR(50) DEFAULT 'pending' CHECK (
        status IN ('pending', 'processing', 'completed', 'failed', 'cancelled')
    ),
    progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),

    -- File information
    file_path VARCHAR(500),
    file_name VARCHAR(255),
    file_size BIGINT,
    download_url VARCHAR(500),
    expires_at TIMESTAMP WITH TIME ZONE,

    -- Processing details
    total_records INTEGER,
    processed_records INTEGER DEFAULT 0,
    processing_time_ms INTEGER,

    -- Metadata
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Indexes for performance
CREATE INDEX idx_export_user_id ON export_jobs(user_id);
CREATE INDEX idx_export_dataset_id ON export_jobs(dataset_id);
CREATE INDEX idx_export_status ON export_jobs(status);
CREATE INDEX idx_export_created_at ON export_jobs(created_at);
CREATE INDEX idx_export_expires_at ON export_jobs(expires_at);
```

**Purpose**: Track and manage data export jobs
**Key Features**:
- Multiple export formats
- Progress tracking
- File expiration management
- Download analytics

## 7. System Configuration Table

```sql
CREATE TABLE system_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key VARCHAR(255) UNIQUE NOT NULL,
    value JSONB NOT NULL,
    description TEXT,
    category VARCHAR(100) DEFAULT 'general',
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_system_config_key ON system_config(key);
CREATE INDEX idx_system_config_category ON system_config(category);
CREATE INDEX idx_system_config_public ON system_config(is_public);
```

**Purpose**: Store system configuration and settings
**Key Features**:
- Flexible key-value configuration
- Public/private setting separation
- Categorized organization

## Database Optimization

### 1. Indexing Strategy

**PostgreSQL Indexes:**
- B-tree indexes for foreign keys and frequently queried columns
- GIN indexes for full-text search and JSONB queries
- Partial indexes for common filtered queries
- Composite indexes for multi-column queries

### 2. Query Optimization

**Common Query Patterns:**
```sql
-- Efficient filtering with indexes
SELECT t.*, ar.*
FROM tweets t
JOIN analysis_results ar ON t.id = ar.tweet_id
WHERE t.dataset_id = $1
  AND ar.sentiment = $2
  AND ar.analyzed_at >= $3
ORDER BY ar.analyzed_at DESC
LIMIT $4;

-- Full-text search with ranking
SELECT t.*, ar.*, ts_rank(to_tsvector('english', t.text), query) as rank
FROM tweets t, plainto_tsquery('english', $1) query
JOIN analysis_results ar ON t.id = ar.tweet_id
WHERE to_tsvector('english', t.text) @@ query
  AND t.dataset_id = $2
ORDER BY rank DESC
LIMIT $3;
```

### 3. Data Archiving Strategy

**Partitioning:**
- Monthly partitioning for tweets table based on created_at
- Automatic partition creation and management
- Archive old partitions to cold storage

**Cleanup Policies:**
- Automatic cleanup of expired export files
- Search history retention based on privacy policy
- Temporary file cleanup after processing
