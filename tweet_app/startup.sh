#!/bin/bash

# TweetEval NLP Platform Startup Script
# This script starts the development environment

set -e

echo "🚀 Starting TweetEval NLP Platform..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Copy environment files if they don't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Please edit .env file with your configuration before running again."
    exit 0
fi

if [ ! -f frontend/.env ]; then
    echo "📝 Creating frontend .env file from template..."
    cp frontend/.env.example frontend/.env
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads exports

# Start services with Docker Compose
echo "🐳 Starting Docker services..."
docker compose-f docker-compose.dev.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo "🔍 Checking service health..."

# Check PostgreSQL
if docker compose-f docker-compose.dev.yml exec -T postgres pg_isready -U tweeteval_user -d tweeteval > /dev/null 2>&1; then
    echo "✅ PostgreSQL is ready"
else
    echo "❌ PostgreSQL is not ready"
fi

# Check Qdrant
if curl -f http://localhost:6333/health > /dev/null 2>&1; then
    echo "✅ Qdrant is ready"
else
    echo "❌ Qdrant is not ready"
fi

# Check Redis
if docker compose-f docker-compose.dev.yml exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is ready"
else
    echo "❌ Redis is not ready"
fi

# Run database migrations
echo "🗄️ Running database migrations..."
docker compose-f docker-compose.dev.yml exec backend alembic upgrade head

# Show service URLs
echo ""
echo "🎉 TweetEval NLP Platform is starting up!"
echo ""
echo "📊 Services will be available at:"
echo "   Frontend:     http://localhost:13000"
echo "   Backend API:  http://localhost:18000"
echo "   API Docs:     http://localhost:18000/api/v1/docs"
echo "   Qdrant:       http://localhost:16333"
echo ""
echo "📋 Useful commands:"
echo "   View logs:    docker compose-f docker-compose.dev.yml logs -f [service]"
echo "   Stop all:     docker compose-f docker-compose.dev.yml down"
echo "   Restart:      docker compose-f docker-compose.dev.yml restart [service]"
echo "   Backend dev:  docker compose-f docker-compose.dev.yml exec backend bash"
echo "   Frontend dev: docker compose-f docker-compose.dev.yml exec frontend bash"
echo ""
echo "🔧 To create an admin user, run:"
echo "   docker compose-f docker-compose.dev.yml exec backend python -m app.scripts.create_admin"
echo ""
echo "⚠️  IMPORTANT: All development must be done within Docker containers."
echo "   Direct Python/npm execution is not supported in this environment."
echo ""

# Follow logs
echo "📝 Following logs (Ctrl+C to stop):"
docker compose-f docker-compose.dev.yml logs -f