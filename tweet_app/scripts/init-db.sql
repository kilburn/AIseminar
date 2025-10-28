-- Initialize database extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create indexes for performance
-- These will also be created by Alembic, but we add them here for initial setup

-- Set up timezone
SET timezone = 'UTC';