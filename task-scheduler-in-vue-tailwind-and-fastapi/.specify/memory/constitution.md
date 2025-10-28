<!-- Sync Impact Report -->
<!-- Version change: 0.0.0 → 1.0.0 -->
<!-- Modified principles: All 5 principles instantiated for Task Scheduler project -->
<!-- Added sections: Technology Stack Constraints, Development Workflow Requirements -->
<!-- Updated templates: ✅ plan-template.md, ✅ spec-template.md, ✅ tasks-template.md -->
<!-- Follow-up TODOs: None -->

# Task Scheduler Constitution

## Core Principles

### I. Database-Aware Development
All code changes MUST be based on live database schema inspection. Database structure is the single source of truth - no hallucinated columns or tables. Use MCP server to read actual schema before any model changes. Database migrations MUST be written and tested before feature implementation.

### II. Docker-First Testing
All tests MUST execute in isolated Docker containers to ensure reproducible results across machines. No exceptions for local testing. Development environment mirrors production exactly via Docker Compose. Test commands use `docker compose exec backend python -m pytest` pattern.

### III. Test-Driven Development (NON-NEGOTIABLE)
TDD mandatory sequence: Write failing tests → Get user approval → Tests fail → Then implement → Refactor. Red-Green-Refactor cycle strictly enforced. Backend tests in `backend/tests/` using Pytest, frontend tests in `frontend/tests/` using Vitest/Playwright.

### IV. CORS-Free Architecture
Frontend-backend communication MUST use Nginx reverse proxy pattern. All API calls use relative URLs (e.g., `/api/tasks`) proxied to backend. No direct cross-origin requests allowed. This eliminates CORS issues and simplifies deployment.

### V. Full-Stack Consistency
Backend uses FastAPI async/await with SQLAlchemy ORM and Pydantic schemas. Frontend uses Vue 3 Composition API with Tailwind CSS (no custom CSS). All state managed through Pinia stores. API contracts must match exactly between frontend and backend.

## Technology Stack Constraints

### Backend Requirements
- FastAPI with Python 3.10+
- SQLAlchemy ORM with Alembic migrations
- PostgreSQL database (Docker container)
- Pydantic schemas for request/response validation
- Async/await pattern for all endpoints

### Frontend Requirements
- Vue.js 3 with Composition API
- Tailwind CSS for styling (FontAwesome icons allowed)
- Axios for HTTP requests with global base URL configuration
- Dayjs for date/calendar handling
- Nginx reverse proxy for CORS-free architecture

### Infrastructure Requirements
- Docker and Docker Compose mandatory
- Multi-stage builds (Node.js builder + Nginx runner)
- Database migrations run automatically on container start
- All services defined in docker-compose.yaml

## Development Workflow Requirements

### Feature Development Process
1. Schema inspection via MCP server
2. Write failing tests for new functionality
3. Implement backend models/services/endpoints
4. Implement frontend components/pages
5. Run full test suite in Docker
6. Create Git branch, commit, and PR via reviewer agent

### Code Quality Standards
- All backend endpoints async/await
- Use SQLAlchemy sessions via dependency injection
- Pydantic schemas for all API contracts
- Vue 3 Composition API preferred
- No custom CSS files - use Tailwind classes only
- Auto-generated OpenAPI docs at `/docs`

### Testing Requirements
- Backend tests: `docker compose exec backend python -m pytest`
- Frontend unit tests with Vitest
- E2E tests with Playwright
- All tests must pass in Docker environment
- Test coverage reporting required

## Governance

This constitution supersedes all other development practices and guidelines. All PRs and reviews must verify compliance with these principles. Amendments require documentation, approval, and migration plan. Use `CLAUDE.md` for runtime development guidance. Complexity beyond these principles must be explicitly justified in implementation plans.

**Version**: 1.0.0 | **Ratified**: 2025-01-28 | **Last Amended**: 2025-01-28