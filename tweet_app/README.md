# TweetEval NLP Analysis Platform

A comprehensive FastAPI + Vue.js platform for tweet dataset analysis using TweetEval models, backed by PostgreSQL and Qdrant vector databases, providing semantic search and interactive visualizations.

## Features

- **Dataset Upload & Processing**: CSV/JSON file ingestion with TweetEval analysis
- **Semantic Search**: Natural language search with embeddings powered by Qdrant
- **Interactive Visualizations**: Charts, timelines, and analytics dashboard
- **Real-time Processing**: Background task processing with live status updates
- **Multi-format Export**: CSV, JSON, and PDF report generation
- **Advanced Analytics**: Correlation analysis and custom modeling capabilities

## Technology Stack

### Backend
- **FastAPI**: High-performance async web framework
- **PostgreSQL**: Primary database for structured data
- **Qdrant**: Vector database for semantic search (custom Dockerfile with curl for healthchecks)
- **SQLAlchemy**: ORM with Alembic migrations
- **Celery**: Background task processing
- **Redis**: Caching and message broker
- **TweetEval**: State-of-the-art NLP models
- **Sentence Transformers**: Text embeddings

### Frontend
- **Vue 3**: Progressive JavaScript framework
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Pinia**: State management
- **Chart.js/D3.js**: Data visualization

## Quick Start

### Prerequisites
- Docker and Docker Compose (required for all development)
- Git
- **Note**: Direct Python/npm execution is not supported. All development must be done within Docker containers.

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tweet_app
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**
   ```bash
   docker compose -f docker-compose.dev.yml up -d
   ```

4. **Initialize the database**
   ```bash
   # Run database migrations
   docker compose-f docker-compose.dev.yml exec backend alembic upgrade head

   # Create initial user (optional)
   docker compose-f docker-compose.dev.yml exec backend python -m app.scripts.create_admin
   ```

5. **Access the applications**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Qdrant Dashboard: http://localhost:6333/dashboard

## Development

### Backend Development

```bash
# Enter backend container
docker compose-f docker-compose.dev.yml exec backend bash

# Install new dependencies
pip install package-name

# Run tests
pytest

# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

**IMPORTANT**: All backend development MUST be done within the Docker container. Direct Python execution is not allowed.

### Frontend Development

```bash
# Enter frontend container
docker compose-f docker-compose.dev.yml exec frontend bash

# Install new dependencies
npm install package-name

# Run tests
npm run test

# Build for production
npm run build
```

**IMPORTANT**: All frontend development MUST be done within the Docker container. Direct npm/node execution is not allowed.

## Project Structure

```
tweet_app/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── workers/        # Celery tasks
│   ├── alembic/            # Database migrations
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── frontend/               # Vue.js application
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/          # Page views
│   │   ├── stores/         # Pinia stores
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   ├── public/             # Static assets
│   ├── tests/              # Frontend tests
│   └── package.json        # Node.js dependencies
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── uploads/                # User uploaded files
├── exports/                # Generated export files
├── qdrant.Dockerfile       # Custom Qdrant Dockerfile with curl for healthchecks
└── docker-compose.dev.yml  # Development environment
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

### Key Endpoints

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/datasets` - Upload dataset
- `GET /api/v1/datasets` - List datasets
- `POST /api/v1/search/semantic` - Semantic search
- `GET /api/v1/analytics/dashboard` - Analytics data

## Database Schema

The application uses PostgreSQL for structured data and Qdrant for vector embeddings:

### PostgreSQL Tables
- `users` - User accounts and authentication
- `datasets` - Dataset metadata and processing status
- `tweets` - Individual tweet data
- `analysis_results` - NLP analysis from TweetEval models
- `search_history` - Search query tracking
- `export_jobs` - Export job management

### Qdrant Collections
- `tweets` - Vector embeddings for semantic search

See the `docs/database/` directory for detailed schema documentation.

## Testing

### Backend Tests
```bash
# Run all tests
docker compose-f docker-compose.dev.yml exec backend pytest

# Run with coverage
docker compose-f docker-compose.dev.yml exec backend pytest --cov=app

# Run specific test file
docker compose-f docker-compose.dev.yml exec backend pytest tests/test_auth.py
```

### Frontend Tests
```bash
# Run unit tests
docker compose-f docker-compose.dev.yml exec frontend npm run test

# Run end-to-end tests
docker compose-f docker-compose.dev.yml exec frontend npm run test:e2e
```

## Deployment

For production deployment, use the production Docker Compose configuration:

```bash
docker compose-f docker-compose.prod.yml up -d
```

See `docs/deployment/` for detailed deployment instructions.

## Monitoring

- **Application Logs**: Available via Docker logs
- **Database Metrics**: PostgreSQL monitoring
- **Vector Database**: Qdrant metrics at http://localhost:6333/metrics
- **Task Queue**: Celery monitoring with Flower (when enabled)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation in `docs/`
- Review the API documentation at `/docs`

## Acknowledgments

- **TweetEval**: Benchmark for tweet classification tasks
- **Hugging Face**: Pre-trained NLP models
- **Qdrant**: Vector similarity search engine
- **FastAPI**: Modern web framework for building APIs