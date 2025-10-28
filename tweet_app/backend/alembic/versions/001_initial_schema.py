"""Initial database schema

Revision ID: 001
Revises:
Create Date: 2025-10-28 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create uuid-ossp extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Create pg_trgm extension for trigram matching (needed for GIN indexes on text)
    op.execute('CREATE EXTENSION IF NOT EXISTS "pg_trgm"')

    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=True),
        sa.Column('organization', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_index('ix_users_active', 'users', ['is_active'], unique=False)

    # Create datasets table
    op.create_table('datasets',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('file_name', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('file_size', sa.BigInteger(), nullable=False),
        sa.Column('file_hash', sa.String(length=64), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=False),
        sa.Column('encoding', sa.String(length=50), nullable=True, default='utf-8'),
        sa.Column('delimiter', sa.String(length=10), nullable=True, default=','),
        sa.Column('has_header', sa.Boolean(), nullable=True, default=True),
        sa.Column('total_rows', sa.Integer(), nullable=True, default=0),
        sa.Column('processed_rows', sa.Integer(), nullable=True, default=0),
        sa.Column('failed_rows', sa.Integer(), nullable=True, default=0),
        sa.Column('processing_status', sa.String(length=50), nullable=True, default='pending'),
        sa.Column('processing_started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('processing_completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True, default=sa.text("'{}'::jsonb")),
        sa.Column('settings', postgresql.JSONB(astext_type=sa.Text()), nullable=True, default=sa.text("'{}'::jsonb")),
        sa.Column('is_public', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("processing_status IN ('pending', 'uploading', 'validating', 'processing', 'completed', 'failed', 'cancelled')", name='processing_status_check')
    )
    op.create_index(op.f('ix_datasets_created_at'), 'datasets', ['created_at'], unique=False)
    op.create_index('ix_datasets_file_hash', 'datasets', ['file_hash'], unique=False)
    op.create_index('ix_datasets_public', 'datasets', ['is_public'], unique=False)
    op.create_index('ix_datasets_status', 'datasets', ['processing_status'], unique=False)
    op.create_index('ix_datasets_user_id', 'datasets', ['user_id'], unique=False)

    # Create tweets table
    op.create_table('tweets',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('dataset_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('original_id', sa.String(length=255), nullable=True),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('cleaned_text', sa.Text(), nullable=True),
        sa.Column('language', sa.String(length=10), nullable=True, default='en'),
        sa.Column('character_count', sa.Integer(), nullable=True),
        sa.Column('word_count', sa.Integer(), nullable=True),
        sa.Column('hashtag_count', sa.Integer(), nullable=True, default=0),
        sa.Column('mention_count', sa.Integer(), nullable=True, default=0),
        sa.Column('url_count', sa.Integer(), nullable=True, default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),  # Original tweet creation time
        sa.Column('processed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True, default=sa.text("'{}'::jsonb")),
        sa.Column('is_valid', sa.Boolean(), nullable=True, default=True),
        sa.Column('validation_errors', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('processing_errors', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('qdrant_id', sa.String(length=255), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['dataset_id'], ['datasets.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tweets_dataset_id', 'tweets', ['dataset_id'], unique=False)
    op.create_index('ix_tweets_is_valid', 'tweets', ['is_valid'], unique=False)
    op.create_index('ix_tweets_language', 'tweets', ['language'], unique=False)
    op.create_index('ix_tweets_original_id', 'tweets', ['original_id'], unique=False)
    op.create_index('ix_tweets_processed_at', 'tweets', ['processed_at'], unique=False)
    op.create_index('ix_tweets_qdrant_id', 'tweets', ['qdrant_id'], unique=False)
    op.create_index('idx_tweets_text_gin', 'tweets', ['text'], unique=False, postgresql_using='gin', postgresql_ops={'text': 'gin_trgm_ops'})

    # Create analysis_results table
    op.create_table('analysis_results',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('tweet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('model_version', sa.String(length=50), nullable=False, default='tweeteval-v1'),
        sa.Column('sentiment', sa.String(length=20), nullable=False),
        sa.Column('sentiment_confidence', sa.Float(), nullable=False),
        sa.Column('sentiment_scores', postgresql.JSONB(astext_type=sa.Text()), nullable=True, default=sa.text("'{}'::jsonb")),
        sa.Column('emotion', sa.String(length=50), nullable=False),
        sa.Column('emotion_confidence', sa.Float(), nullable=False),
        sa.Column('emotion_scores', postgresql.JSONB(astext_type=sa.Text()), nullable=True, default=sa.text("'{}'::jsonb")),
        sa.Column('offensive_language', sa.Boolean(), nullable=False),
        sa.Column('offensive_confidence', sa.Float(), nullable=False),
        sa.Column('offensive_scores', postgresql.JSONB(astext_type=sa.Text()), nullable=True, default=sa.text("'{}'::jsonb")),
        sa.Column('hate_speech', sa.String(length=50), nullable=True),
        sa.Column('hate_confidence', sa.Float(), nullable=True),
        sa.Column('hate_scores', postgresql.JSONB(astext_type=sa.Text()), nullable=True, default=sa.text("'{}'::jsonb")),
        sa.Column('irony', sa.Boolean(), nullable=True),
        sa.Column('irony_confidence', sa.Float(), nullable=True),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True),
        sa.Column('model_used', sa.String(length=100), nullable=True),
        sa.Column('analyzed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('confidence_threshold', sa.Float(), nullable=True, default=0.5),
        sa.ForeignKeyConstraint(['tweet_id'], ['tweets.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("sentiment IN ('positive', 'negative', 'neutral')", name='sentiment_check'),
        sa.CheckConstraint("emotion IN ('joy', 'sadness', 'anger', 'fear', 'surprise', 'disgust', 'others')", name='emotion_check'),
        sa.CheckConstraint("hate_speech IN ('hateful', 'targeted', 'aggressive', 'none')", name='hate_speech_check'),
        sa.CheckConstraint("sentiment_confidence >= 0 AND sentiment_confidence <= 1", name='sentiment_confidence_check'),
        sa.CheckConstraint("emotion_confidence >= 0 AND emotion_confidence <= 1", name='emotion_confidence_check'),
        sa.CheckConstraint("offensive_confidence >= 0 AND offensive_confidence <= 1", name='offensive_confidence_check'),
        sa.CheckConstraint("hate_confidence >= 0 AND hate_confidence <= 1", name='hate_confidence_check'),
        sa.CheckConstraint("irony_confidence >= 0 AND irony_confidence <= 1", name='irony_confidence_check'),
        sa.CheckConstraint("confidence_threshold >= 0 AND confidence_threshold <= 1", name='confidence_threshold_check')
    )
    op.create_index('ix_analysis_analyzed_at', 'analysis_results', ['analyzed_at'], unique=False)
    op.create_index('ix_analysis_emotion', 'analysis_results', ['emotion'], unique=False)
    op.create_index('ix_analysis_offensive', 'analysis_results', ['offensive_language'], unique=False)
    op.create_index('ix_analysis_sentiment', 'analysis_results', ['sentiment'], unique=False)
    op.create_index('ix_analysis_tweet_id', 'analysis_results', ['tweet_id'], unique=False)
    op.create_index('ix_analysis_hate_speech', 'analysis_results', ['hate_speech'], unique=False)

    # Create search_history table
    op.create_table('search_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('session_id', sa.String(length=255), nullable=True),
        sa.Column('query', sa.Text(), nullable=False),
        sa.Column('query_type', sa.String(length=50), nullable=True, default='semantic'),
        sa.Column('filters', postgresql.JSONB(astext_type=sa.Text()), nullable=True, default=sa.text("'{}'::jsonb")),
        sa.Column('limit', sa.Integer(), nullable=True, default=20),
        sa.Column('offset', sa.Integer(), nullable=True, default=0),
        sa.Column('result_count', sa.Integer(), nullable=False),
        sa.Column('result_ids', postgresql.ARRAY(postgresql.UUID()), nullable=True),
        sa.Column('max_similarity', sa.Float(), nullable=True),
        sa.Column('avg_similarity', sa.Float(), nullable=True),
        sa.Column('execution_time_ms', sa.Integer(), nullable=True),
        sa.Column('vector_search_time_ms', sa.Integer(), nullable=True),
        sa.Column('filter_time_ms', sa.Integer(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("query_type IN ('semantic', 'keyword', 'hybrid')", name='query_type_check')
    )
    op.create_index('ix_search_created_at', 'search_history', ['created_at'], unique=False)
    op.create_index('ix_search_session_id', 'search_history', ['session_id'], unique=False)
    op.create_index('ix_search_user_id', 'search_history', ['user_id'], unique=False)
    op.create_index('idx_search_query_gin', 'search_history', ['query'], unique=False, postgresql_using='gin', postgresql_ops={'query': 'gin_trgm_ops'})

    # Create export_jobs table
    op.create_table('export_jobs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dataset_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('export_type', sa.String(length=50), nullable=False),
        sa.Column('format_options', postgresql.JSONB(astext_type=sa.Text()), nullable=True, default=sa.text("'{}'::jsonb")),
        sa.Column('filters', postgresql.JSONB(astext_type=sa.Text()), nullable=True, default=sa.text("'{}'::jsonb")),
        sa.Column('status', sa.String(length=50), nullable=True, default='pending'),
        sa.Column('progress_percentage', sa.Integer(), nullable=True, default=0),
        sa.Column('file_path', sa.String(length=500), nullable=True),
        sa.Column('file_name', sa.String(length=255), nullable=True),
        sa.Column('file_size', sa.BigInteger(), nullable=True),
        sa.Column('download_url', sa.String(length=500), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_records', sa.Integer(), nullable=True),
        sa.Column('processed_records', sa.Integer(), nullable=True, default=0),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['dataset_id'], ['datasets.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("export_type IN ('csv', 'json', 'pdf', 'excel')", name='export_type_check'),
        sa.CheckConstraint("status IN ('pending', 'processing', 'completed', 'failed', 'cancelled')", name='status_check'),
        sa.CheckConstraint("progress_percentage >= 0 AND progress_percentage <= 100", name='progress_percentage_check')
    )
    op.create_index('ix_search_created_at', 'export_jobs', ['created_at'], unique=False)
    op.create_index('ix_export_created_at', 'export_jobs', ['created_at'], unique=False)
    op.create_index('ix_export_dataset_id', 'export_jobs', ['dataset_id'], unique=False)
    op.create_index('ix_export_expires_at', 'export_jobs', ['expires_at'], unique=False)
    op.create_index('ix_export_status', 'export_jobs', ['status'], unique=False)
    op.create_index('ix_export_user_id', 'export_jobs', ['user_id'], unique=False)

    # Create system_config table
    op.create_table('system_config',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=sa.text('uuid_generate_v4()')),
        sa.Column('key', sa.String(length=255), nullable=False),
        sa.Column('value', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True, default='general'),
        sa.Column('is_public', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key')
    )
    op.create_index('ix_system_config_category', 'system_config', ['category'], unique=False)
    op.create_index('ix_system_config_key', 'system_config', ['key'], unique=False)
    op.create_index('ix_system_config_public', 'system_config', ['is_public'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order of creation
    op.drop_table('system_config')
    op.drop_table('export_jobs')
    op.drop_table('search_history')
    op.drop_table('analysis_results')
    op.drop_table('tweets')
    op.drop_table('datasets')
    op.drop_table('users')