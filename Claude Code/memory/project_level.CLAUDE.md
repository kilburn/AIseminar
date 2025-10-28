# Project Guidelines for Claude

## Project Overview

This repository implements a **full-stack task scheduler application** with modern web technologies and containerized deployment.

**Tech Stack:**
- **Frontend**: Vue.js 3 with Composition API, Tailwind CSS, Vite, and Nginx reverse proxy
- **Backend**: FastAPI (Python) with PostgreSQL and Alembic for schema management
- **DevOps**: Docker and Docker Compose for complete containerization
- **Language Composition**: Vue 78.9%, Python 15.2%, JavaScript 3.5%, Other 2.4%

## Repository Structure

```
├── client/                 # Vue.js 3 frontend application
│   ├── src/               # Vue components, stores, views
│   ├── public/            # Static assets
│   ├── nginx.conf         # Nginx reverse proxy configuration
│   ├── Dockerfile         # Frontend container image
│   └── package.json       # Node.js dependencies
├── backend/               # FastAPI REST API and business logic
│   ├── app/               # FastAPI application modules
│   ├── tests/             # pytest test suite
│   ├── Dockerfile         # Backend container image
│   └── requirements.txt    # Python dependencies
├── alembic/               # Database migration scripts (generic single-database setup)
│   ├── versions/          # Migration files
│   └── env.py             # Migration configuration
├── docs/                  # Comprehensive project documentation
│   ├── DOCUMENTATION.md   # Main project guide (START HERE)
│   ├── DOCKER.md          # Docker/containerization guide
│   ├── CORS.md            # API routing and CORS configuration
│   └── 307_REDIRECT_FIX.md # Troubleshooting common issues
├── screenshots/           # UI proof-of-concept assets
├── docker-compose.yml     # Service orchestration configuration
├── README.md              # Project overview and quick start
└── .env                   # Environment variables (DO NOT COMMIT)
```

## Coding & Architecture Conventions

### Frontend (Vue.js 3 + Tailwind CSS)
- **Location**: `client/src/`
- **Pattern**: Vue 3 Composition API with `<script setup>` syntax
- **Styling**: Tailwind CSS utility classes only (no inline styles)
- **Component Structure**: 
  - Place reusable components in `components/`
  - Keep page-level logic in `views/`
  - Use `composables/` for shared reactive logic
- **API Communication**: Use relative URLs (e.g., `/api/tasks`) which are proxied through Nginx
- **State Management**: Pinia for centralized state (if applicable)

### Backend (FastAPI + Python)
- **Location**: `backend/app/`
- **Architecture**:
  - Use FastAPI routers to organize endpoints by resource (e.g., `routers/tasks.py`)
  - Define request/response models with Pydantic for validation and documentation
  - Implement dependency injection for database sessions and authentication
  - Follow REST conventions for endpoint naming
- **Code Quality**:
  - Type hints on all functions and variables
  - Docstrings on endpoints using FastAPI's description parameter
  - Error handling with meaningful HTTP status codes
  - Logging for debugging and monitoring
- **Environment**: Load configuration from `.env` using `python-dotenv`

### Database & Migrations
- **Tool**: Alembic (generic single-database configuration)
- **Location**: `alembic/versions/`
- **Workflow**:
  1. Make schema changes in database or ORM models
  2. Auto-generate migration: `alembic revision --autogenerate -m "description"`
  3. Review and test the migration
  4. Migrations run automatically on container startup
  5. Manual trigger: `alembic upgrade head`
- **Critical**: Do NOT change the generic single-database setup without database expertise

### API & Reverse Proxy
- **Proxy**: Nginx eliminates CORS issues by routing `/api/*` to the FastAPI backend
- **Configuration**: See `client/nginx.conf` (do not modify without understanding implications)
- **URL Pattern**: Frontend calls `/api/tasks` → Nginx forwards to `backend:8000/tasks`
- **Trailing Slashes**: Some endpoints may require trailing slashes; see `docs/307_REDIRECT_FIX.md`

## Testing & Quality Standards

### Frontend Testing
- **Framework**: Vue Test Utils + Vitest
- **Location**: `client/tests/`
- **Coverage**: Aim for >80% on critical components
- **Run Tests**: `npm run test` (from `client/` directory)

### Backend Testing
- **Framework**: pytest
- **Location**: `backend/tests/`
- **Coverage**: Aim for >80% on API endpoints and business logic
- **Run Tests**: `pytest` (from `backend/` directory)
- **Database**: Use fixtures for test database isolation

### Code Quality & Linting

**Frontend:**
- ESLint with Vue 3 configuration
- Prettier for code formatting
- Tailwind CSS JIT class ordering enforcement
- Commands:
  ```bash
  npm run lint           # Run ESLint
  npm run format        # Format with Prettier
  npm run type-check    # Type checking (if using TypeScript)
  ```

**Backend:**
- flake8 for linting (PEP8 compliance)
- black for code formatting
- mypy for static type checking
- Commands:
  ```bash
  flake8 backend/       # Run linter
  black backend/        # Format code
  mypy backend/         # Type checking
  ```

### Continuous Integration
- **Trigger**: On push to `main` branch
- **Pipeline**:
  1. Run frontend linter and formatter checks
  2. Build frontend with Vite
  3. Run backend linter and type checks
  4. Execute backend test suite
  5. Bundle and create deployment artifact

## Development Workflow

### Getting Started
```bash
# Start the entire stack (frontend, backend, database)
docker-compose up --build

# Access the application
# Frontend: http://localhost:80
# API Docs: http://localhost/api/docs
# ReDoc: http://localhost/api/redoc
```

### Making Changes

**For Frontend Features:**
1. Create Vue component or modify existing one in `client/src/`
2. Use Tailwind classes for styling
3. Make API calls using relative URLs (e.g., `fetch('/api/tasks')`)
4. Write tests in `client/tests/`
5. Run linter: `npm run lint`

**For Backend Features:**
1. Create/modify FastAPI routers in `backend/app/routers/`
2. Define Pydantic models in `backend/app/models/`
3. Update database schema if needed
4. Generate migration: `alembic revision --autogenerate -m "description"`
5. Write tests in `backend/tests/`
6. Run linter and tests: `flake8 backend/ && pytest`

**For Database Schema Changes:**
1. Update ORM models or create migration manually
2. Generate migration: `alembic revision --autogenerate -m "clear description"`
3. Review the generated SQL in `alembic/versions/`
4. Test locally: `docker-compose up --build`
5. Migrations auto-run on container startup

### Documentation Updates
- Update `docs/DOCUMENTATION.md` for major features
- Update `docs/DOCKER.md` if deployment changes
- Update `docs/CORS.md` if API routing changes
- Keep this `CLAUDE.md` file in sync with project conventions

## Architecture Principles

### Separation of Concerns
- **Frontend** (`client/`): UI/UX, user interactions, form validation, state management
- **Backend** (`backend/`): Business logic, data validation, database operations, authentication
- **Database** (`alembic/`): Schema definition and versioned migrations

### Key Design Patterns
1. **REST API**: Stateless, resource-based endpoints
2. **Component-Based UI**: Reusable Vue components with single responsibility
3. **Dependency Injection**: FastAPI dependencies for database and auth
4. **Type Safety**: Python type hints and Pydantic validation
5. **Containerization**: Each service (frontend, backend, database) runs in isolated container

## Documentation & Resources

| Document | Purpose |
|----------|---------|
| `docs/DOCUMENTATION.md` | **START HERE** - Complete project overview and navigation |
| `docs/DOCKER.md` | Docker/Docker Compose setup, architecture, deployment |
| `docs/CORS.md` | Nginx reverse proxy configuration and API routing |
| `docs/307_REDIRECT_FIX.md` | Common issues and troubleshooting solutions |
| `README.md` | Project overview, screenshots, and quick start commands |

## What NOT to Change (Critical Constraints)

### Do NOT
- ❌ Remove or rename `screenshots/` folder without updating README references
- ❌ Commit secrets, `.env` files, `node_modules/`, or build artifacts to git
- ❌ Mix inline styles with Tailwind utilities; maintain utility-only styling
- ❌ Modify `client/nginx.conf` without understanding CORS/routing implications
- ❌ Change the Alembic configuration from "generic single-database setup" without expertise
- ❌ Remove or modify `docs/` folder; it's critical project guidance
- ❌ Add backend logic to frontend components or vice versa
- ❌ Commit un-formatted or un-linted code; enforce CI standards locally first

### Ensure Updated
- ✅ `.gitignore` excludes all local build artifacts and secrets
- ✅ `requirements.txt` updated when backend dependencies change
- ✅ `package.json` and `package-lock.json` synchronized when frontend dependencies change
- ✅ Documentation reflects major architectural changes
- ✅ Type hints added to all new Python functions
- ✅ Tailwind classes used instead of custom CSS

## Common Tasks Reference

### Add a New API Endpoint
1. Create/modify router in `backend/app/routers/`
2. Define Pydantic models for request/response
3. Implement endpoint with FastAPI decorator
4. Add type hints and docstrings
5. Write tests in `backend/tests/`
6. Call from frontend using `fetch('/api/...')`

### Add a New Database Table
1. Define SQLAlchemy model in `backend/app/models/`
2. Generate migration: `alembic revision --autogenerate -m "add_new_table"`
3. Review SQL in `alembic/versions/`
4. Test with `docker-compose up --build`
5. Update API routers to use new table

### Add a New Vue Component
1. Create `.vue` file in `client/src/components/` or `client/src/views/`
2. Use `<script setup>` syntax and Composition API
3. Style with Tailwind CSS classes only
4. Import and use in parent component
5. Write tests if critical to app flow
6. Ensure ESLint passes: `npm run lint`

### Debug API Issues
1. Check Nginx proxy logs: `docker-compose logs nginx`
2. Check backend logs: `docker-compose logs backend`
3. Review API documentation: `http://localhost/api/docs`
4. Verify trailing slashes (see `docs/307_REDIRECT_FIX.md`)
5. Check CORS configuration (see `docs/CORS.md`)

## Quick Reference: Running Commands

```bash
# Frontend
cd client && npm install        # Install dependencies
npm run dev                     # Dev server (hot reload)
npm run build                   # Production build
npm run lint                    # ESLint
npm run format                  # Prettier format
npm run test                    # Run tests

# Backend
cd backend && pip install -r requirements.txt  # Install dependencies
uvicorn app.main:app --reload                # Dev server
pytest                                        # Run tests
flake8 .                                     # Lint
black .                                      # Format
mypy .                                       # Type check

# Database
alembic revision --autogenerate -m "message"  # Generate migration
alembic upgrade head                          # Apply migrations
alembic downgrade -1                          # Rollback one migration

# Docker
docker-compose up --build                     # Start all services
docker-compose down                           # Stop all services
docker-compose logs -f backend               # View backend logs
docker-compose exec backend bash              # Enter backend container
```

---

**Last Updated**: 2025-10-26  
**Project**: Task Scheduler (Vue.js + FastAPI + PostgreSQL)  
**Maintained By**: Development Team
