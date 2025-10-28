-- Test database initialization script
-- Creates initial schema and test data for Phase 1 testing

-- Create test user for authentication tests
-- Note: In tests, these are typically created via API, this is for manual testing

-- Create system schema if needed
CREATE SCHEMA IF NOT EXISTS public;

-- Enable extensions for testing
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create initial tables (will be created by SQLAlchemy models in normal operation)
-- This script is for setup validation only

-- Verify PostgreSQL is accessible
SELECT version();

-- Check connection
SELECT current_database();

-- Display current user
SELECT current_user;

-- Verify extensions
SELECT extname FROM pg_extension ORDER BY extname;
