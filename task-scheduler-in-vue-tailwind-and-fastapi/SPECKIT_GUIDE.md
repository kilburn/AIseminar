# Spec Kit Guideline for Task Scheduler

## 1. Purpose

Spec Kit is being adopted to standardize requirements gathering, specification writing, and implementation tracking for this FastAPI + Vue.js + Tailwind CSS task scheduler application. We expect:

- Clear, testable specifications that prevent scope creep and misunderstandings
- Consistent documentation of API contracts and data models
- Improved cross-functional collaboration between frontend and backend teams
- Reduced technical debt through upfront design and validation
- Faster onboarding of new team members through standardized practices

## 2. Prerequisites (Repo-Specific)

- **Python**: 3.9+ (target: 3.10)
- **Node.js**: 18+ (target: 20)
- **Docker**: 20.10+ and Docker Compose 2.0+
- **PostgreSQL Client**: 15+ (for local development)

```bash
# Verify tool versions
python --version  # Should be 3.9+
node --version    # Should be 18+
docker --version  # Should be 20.10+
docker compose version  # Should be 2.0+

# Verify Docker can run containers
docker run hello-world
```

**AI Agent Configuration**: Configure your preferred AI agent in your environment or IDE settings. This team typically uses Claude Code for development assistance.

## 3. Quickstart (Copy-Paste)

```bash
# Safe bootstrap with clean state
git checkout -b speckit-bootstrap
git add -A && git commit -m "Pre-speckit setup checkpoint"

# Install Spec Kit CLI (choose one method)
# Method 1: UV (recommended)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# Method 2: Pip (fallback)
pip install specify-cli --find-links https://github.com/github/spec-kit.git

# Initialize Spec Kit in this repository
specify check
specify init --here   # Use --force ONLY after committing clean state

# Verify initialization
ls -la spec-kit/ constitution.md spec.md plan.md tasks.md
```

**Notes for this repo**:
- This is a **Docker-first** project - prefer `docker compose` commands for development
- The repository uses **dual package management** (Python requirements.txt + Node package.json)
- Frontend and backend are in separate directories (`client/` and `backend/`)
- Database migrations are managed via Alembic in the root directory

## 4. Our Constitution (Tailored)

### Coding Standards
- **Backend**: Python 3.10+, async/await FastAPI patterns, SQLAlchemy ORM, Alembic migrations
- **Frontend**: Vue 3 Composition API, ES6+, Tailwind CSS classes only (no custom CSS)
- **Database**: PostgreSQL 15, all schema changes via Alembic migrations
- **Code Style**: Black formatter for Python, Prettier for frontend (when configured)

### Testing Requirements
- **Backend**: All endpoints must have unit tests (pytest) and integration tests
- **Frontend**: Components must have Vitest unit tests; critical user flows need Playwright E2E tests
- **Coverage**: 80% minimum coverage across both frontend and backend
- **Contract Tests**: API endpoints must have integration tests validating request/response schemas

### Security & Privacy
- **Authentication**: JWT tokens with secure cookie handling (when implemented)
- **CORS**: Avoid via Nginx reverse proxy pattern - use relative URLs configured in `client/src/main.js`
- **Secrets**: Environment variables only in Docker Compose; never commit secrets
- **Dependencies**: Must pass Bandit (backend) and npm audit (frontend) scans
- **Data Validation**: Pydantic schemas for all API request/response models

### Performance & Reliability SLOs
- **API Response Time**: p95 < 200ms for simple CRUD operations
- **Database Queries**: All queries must be indexed and optimized
- **Frontend Bundle**: < 1MB total, < 100kb initial load
- **Error Rate**: < 1% for all endpoints
- **Uptime**: 99.9% availability target

### Observability Requirements
- **Logging**: Structured JSON logs for all API endpoints and database operations
- **Metrics**: Request/response times, error rates, database query performance
- **Health Checks**: `/health` endpoint for all services
- **Docker Logs**: All services must log to stdout/stderr for container orchestration

### UX Principles
- **Accessibility**: WCAG 2.1 AA compliance minimum
- **Design Tokens**: Tailwind CSS utility classes only
- **Responsive Design**: Mobile-first approach, support desktop layouts
- **Error Handling**: User-friendly error messages with appropriate HTTP status codes

### Never Do
- **Direct CORS configuration** - use Nginx reverse proxy pattern
- **Custom CSS files** - use Tailwind utility classes only
- **Manual database schema changes** - always use Alembic migrations
- **Commit secrets or API keys** - use environment variables
- **Skip tests for new endpoints or components**

## 5. How We Specify Changes

### When to Write a Spec
- **New Features**: Any new API endpoint, database table, or major UI component
- **Breaking Changes**: Any change to existing API contracts or database schema
- **Performance Changes**: Any optimization affecting user experience or system resources
- **Security Changes**: Authentication, authorization, or data handling modifications

### Specification Template (FastAPI + Vue Stack)

```markdown
## Feature: [Feature Name]

### Overview
Brief description of what this feature accomplishes and why it's needed.

### API Contract (Backend)
- **Endpoint**: `GET|POST|PUT|DELETE /api/resource/{id}`
- **Request**: Pydantic schema with field definitions and validation rules
- **Response**: JSON schema with success and error response formats
- **Authentication**: Required roles and permissions
- **Rate Limiting**: Any limits or quotas

### Data Model Changes
- **Database Schema**: New tables, columns, or indices
- **Alembic Migration**: Migration script details
- **Relationships**: Foreign keys and join conditions

### Frontend Implementation
- **Vue Components**: New or modified components with props and emits
- **Routes**: Router configuration changes
- **State Management**: Pinia store modifications (if applicable)
- **API Integration**: Axios service layer changes

### Acceptance Criteria (Gherkin Style)
```gherkin
Feature: Task Management
  As a user
  I want to create, read, update, and delete tasks
  So that I can manage my work effectively

  Scenario: Create a new task
    Given I am on the task creation page
    When I fill in the task title and description
    And I select a due date
    And I click "Create Task"
    Then I should see the task in my task list
    And the task should be saved in the database
```

### Testing Requirements
- **Unit Tests**: Backend service and schema validation tests
- **Integration Tests**: API endpoint tests with database
- **Frontend Tests**: Component unit tests and user interaction tests
- **E2E Tests**: Critical user journey automation

### Performance Requirements
- **Response Time**: Maximum acceptable response time
- **Database Queries**: Query optimization requirements
- **Frontend Bundle**: Bundle size impact assessment
```

## 6. Planning Against This Codebase

### Module Boundaries
- **Backend Modules**: Separate concerns by feature (tasks, users, auth, etc.)
- **Frontend Modules**: Group by page/component hierarchy
- **Database**: One table per entity, proper foreign key relationships
- **API**: RESTful design with consistent URL patterns

### Data Contracts & Validation
- **HTTP**: JSON payloads with Content-Type: application/json
- **Validation**: Pydantic schemas for all request/response models
- **Database**: SQLAlchemy models with proper constraints and indexes
- **Frontend**: Type-safe prop validation in Vue components

### Migration & Feature Flag Approach
- **Database**: Alembic migrations with rollback scripts
- **API**: Version endpoints when breaking changes are required
- **Frontend**: Feature flags using environment variables
- **Rollback Triggers**: Monitor error rates and performance metrics post-deployment

## 7. Tasks & Execution

### Task Decomposition (≤1 Day Tasks)
- **Backend Tasks**: API endpoints, database models, service layer logic
- **Frontend Tasks**: Component development, route configuration, API integration
- **Testing Tasks**: Unit tests, integration tests, E2E test scenarios
- **Infrastructure Tasks**: Docker configuration, CI/CD pipeline updates

### Branching Model
- **Main Branch**: `main` for production deployments
- **Development Branch**: `develop` for integration testing
- **Feature Branches**: `feature/task-123-task-management` from develop
- **Bugfix Branches**: `bugfix/fix-task-creation-validation` from main

### Required Checks
- **All PRs**: Must pass CI/CD pipeline including matrix testing
- **Backend**: Unit tests, integration tests, security scans (Bandit, Safety)
- **Frontend**: Unit tests, E2E tests, security audit (npm audit)
- **Performance**: Bundle size analysis and API performance benchmarks

### Commit/PR Conventions
```
feat(tasks): add task creation endpoint with validation
fix(auth): resolve JWT token expiration handling issue
docs(api): update OpenAPI documentation for task endpoints
test(frontend): add unit tests for task list component
perf(database): add index to task.created_date for query optimization
```

## 8. Implementation Workflow (Commands)

### Development Environment Setup
```bash
# Start Docker development environment
docker compose -f docker/docker-compose.yaml up --build

# View logs for specific services
docker compose -f docker/docker-compose.yaml logs -f backend
docker compose -f docker/docker-compose.yaml logs -f frontend

# Execute commands in containers
docker compose -f docker/docker-compose.yaml exec backend python -m pytest
docker compose -f docker/docker-compose.yaml exec backend alembic upgrade head
```

### Local Development Commands
```bash
# Backend development
pip install -r src/requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Frontend development
cd client
npm install
npm run dev  # Development server on port 3000
npm run build  # Production build

# Testing
pytest tests/ -v --cov=backend  # Backend tests
cd client && npm run test:coverage  # Frontend tests
npm run test:e2e  # E2E tests
```

### Spec Kit Commands
```bash
/speckit.constitution    # Review our coding standards
/speckit.specify        # Write detailed specifications
/speckit.plan          # Create implementation plan
/speckit.tasks         # Decompose into actionable tasks
/speckit.analyze       # Analyze impact and dependencies
/speckit.implement     # Generate implementation code
```

### Environment Variables
```bash
# Database configuration
DATABASE_USERNAME=scheduler
DATABASE_PASSWORD=scheduler
DATABASE_HOST=db  # In Docker
DATABASE_NAME=scheduler

# Frontend build configuration
VITE_BASE_URL=http://127.0.0.1:8080/  # Base URL for API calls
```

## 9. Testing Strategy (Repo-Tuned)

### Test Locations
- **Backend Unit Tests**: `tests/unit/` - Test service layer logic and Pydantic schemas
- **Backend Integration Tests**: `tests/integration/` - Test API endpoints with database
- **Frontend Unit Tests**: `client/tests/unit/` - Test Vue components and utilities
- **E2E Tests**: `client/tests/e2e/` - Test complete user workflows

### Test Execution
```bash
# Run all tests
docker compose -f docker/docker-compose.yaml exec backend python -m pytest
cd client && npm run test:run

# Run specific test suites
pytest tests/unit/test_services.py -v
npm run test:unit
npm run test:e2e -- --project=chromium

# Coverage reports
pytest --cov=backend --cov-report=html
npm run test:coverage
```

### Minimal Smoke Tests for New Modules
- **Backend Module**: Test database CRUD operations and API endpoint responses
- **Frontend Component**: Test component rendering, props, and user interactions
- **Integration**: Test data flow from frontend UI to backend database

### Performance & Regression Tests
- **Load Testing**: Artillery configuration in `tests/performance/`
- **Bundle Analysis**: Webpack Bundle Analyzer for frontend
- **Database Performance**: Query timing and indexing validation

## 10. Security & Compliance

### Dependency Scanning
- **Backend**: Bandit for code analysis, Safety for dependency vulnerabilities
- **Frontend**: npm audit for package vulnerabilities
- **Frequency**: Automated scanning on all PRs and daily security updates

### AuthN/Z Patterns
- **Authentication**: JWT tokens with secure HttpOnly cookies
- **Authorization**: Role-based access control (RBAC) when implemented
- **Session Management**: Secure token storage and refresh mechanisms

### Data Handling
- **PII/GDPR**: No personal data stored without explicit consent
- **Encryption**: Database connections and sensitive data at rest
- **Audit Logging**: Track all data modifications and access attempts

### Security Configuration
```bash
# Run security scans
bandit -r backend/ -f json -o security-report.json
safety check --json --output dependency-report.json
npm audit --audit-level=moderate --json > frontend-security.json
```

## 11. Observability Playbook

### Logging Requirements
- **Backend**: Structured JSON logs with request ID tracing
- **Frontend**: Error logging and user interaction tracking
- **Database**: Query performance logging and connection monitoring

### Metrics Collection
- **API Metrics**: Request/response times, error rates, endpoint usage
- **Database Metrics**: Query performance, connection pool usage
- **Frontend Metrics**: Bundle size, page load times, user interactions

### Dashboards & Alerts
- **Performance Dashboard**: API response times and error rates
- **Database Dashboard**: Query performance and connection health
- **Frontend Dashboard**: Bundle analysis and user experience metrics

### SLI/SLOs
- **API Response Time**: p95 < 200ms, p99 < 500ms
- **Error Rate**: < 1% for all endpoints
- **Database Query Time**: p95 < 100ms for complex queries
- **Frontend Load Time**: < 3 seconds for initial page load

## 12. Release & Rollout

### Versioning Strategy
- **Semantic Versioning**: Follow SemVer for all releases
- **Database Migrations**: Version-controlled with Alembic
- **API Versioning**: URL-based versioning when breaking changes required

### Changelog Management
- **Automatic Changelog**: Generate from Git commit messages
- **Release Notes**: Include new features, bug fixes, and breaking changes
- **Migration Notes**: Document database changes and manual steps required

### Release Process
```bash
# Create release branch
git checkout -b release/v1.2.0 develop

# Run full test suite
docker compose -f docker/docker-compose.yaml up --build
pytest tests/ -v
cd client && npm run test:run

# Tag and release
git tag v1.2.0
git push origin v1.2.0
```

### Post-Release Monitoring
- **Error Monitoring**: Watch for increased error rates
- **Performance Monitoring**: Validate response times remain within SLOs
- **User Feedback**: Monitor for user-reported issues
- **Rollback Criteria**: Define thresholds for automatic rollback

## 13. Checklists

### Author PR Checklist
- [ ] Code follows project coding standards (Black/Prettier where configured)
- [ ] All new code has appropriate unit tests
- [ ] Integration tests validate API contracts
- [ ] Frontend components have accessible markup (ARIA labels, semantic HTML)
- [ ] Database changes include Alembic migration
- [ ] Security scans pass (Bandit, Safety, npm audit)
- [ ] Performance impact assessed and documented
- [ ] Documentation updated (API docs, README, etc.)
- [ ] PR description references specification clause

### Reviewer Checklist
- [ ] Code implements requirements from specification
- [ ] Tests provide adequate coverage and edge case handling
- [ ] Security implications reviewed and addressed
- [ ] Performance impact acceptable
- [ ] API contracts follow RESTful principles
- [ ] Database schema is properly normalized and indexed
- [ ] Error handling is comprehensive and user-friendly
- [ ] Frontend follows accessibility guidelines

### Pre-Merge CI Checklist
- [ ] All CI/CD jobs pass (matrix testing across Python/Node versions)
- [ ] Security scans complete with no high-severity issues
- [ ] Code coverage meets minimum thresholds (80%)
- [ ] Performance benchmarks within acceptable ranges
- [ ] Integration tests validate end-to-end workflows
- [ ] Documentation builds successfully

### Release Checklist
- [ ] All required approvals obtained
- [ ] Release notes prepared and reviewed
- [ ] Database migrations tested in staging environment
- [ ] Rollback plan documented and tested
- [ ] Monitoring dashboards updated for new features
- [ ] Support team notified of changes
- [ ] Post-release monitoring plan in place

## 14. Slash-Command Cookbook (For Our Stack)

### Common Development Flows

```bash
# Start new feature development
/speckit.specify    # Write specification for new task management feature
/speckit.plan      # Create implementation plan
/speckit.tasks     # Generate actionable tasks

# Implement new API endpoint
/speckit.implement --focus backend-endpoint --model Task --endpoint POST /api/tasks

# Create frontend component
/speckit.implement --focus vue-component --name TaskForm --props "task:Task, mode:edit|create"

# Add database migration
/speckit.implement --focus alembic-migration --description "add priority column to task table"

# Write tests for existing code
/speckit.implement --focus backend-tests --module tasks.services
/speckit.implement --focus frontend-tests --component TaskList

# Performance optimization
/speckit.analyze --focus performance --target "task listing endpoint"
/speckit.implement --focus database-index --table task --columns "status, created_date"
```

### Quick Validation Commands

```bash
# Validate current implementation against constitution
/speckit.constitution --check

# Analyze impact of proposed changes
/speckit.analyze --impact security,performance

# Generate documentation
/speckit.implement --focus api-docs --module tasks
```

## 15. Appendix

### Repo Snapshot

**Stack & Tooling:**
- Backend: Python 3.10, FastAPI 0.88.0, SQLAlchemy 1.4.45, PostgreSQL 15
- Frontend: Vue.js 3.5.13, Vite 6.2.2, Tailwind CSS 4.0.15, Node.js 20
- Testing: Pytest 7.4.3, Vitest 2.1.8, Playwright 1.50.0
- Infrastructure: Docker, Docker Compose, Nginx

**Architecture:**
- Three-tier: Frontend (Nginx/Vue) → Backend (FastAPI) → Database (PostgreSQL)
- CORS-free design via Nginx reverse proxy
- Modular structure with clear separation of concerns
- Database migrations managed via Alembic

**Data Model:**
- Primary entity: Task (id, title, description, status, createdDate, dueDate)
- Relationships: Simple flat structure (expandable for user assignments, categories)
- Validation: Pydantic schemas for all API contracts

**CI/CD:**
- Matrix testing across multiple Python and Node.js versions
- Comprehensive security scanning (Bandit, Safety, npm audit)
- Performance benchmarking and bundle analysis
- Automated test reporting and coverage tracking

### File Map (Post-Initialization)

Once Spec Kit is initialized, you'll find these key files:

```
spec-kit/
├── constitution.md        # Our team's coding standards and rules
├── spec.md               # Detailed feature specifications
├── plan.md               # Implementation plans and architecture
├── tasks.md              # Decomposed actionable tasks
└── generated/            # Auto-generated implementation files
    ├── backend/          # FastAPI endpoints, models, services
    ├── frontend/         # Vue components, routes, utilities
    ├── tests/            # Test files for backend and frontend
    └── migrations/       # Alembic migration scripts
```

### Open Questions

**Performance SLOs:** Team needs to define specific response time targets and error budget policies.

**AI Agent Configuration:** Team should document preferred AI assistant settings and integration points.

**Coverage Floors:** Currently set at 80% globally - consider if different modules need different thresholds.

**Feature Flag System:** Need to decide on feature flag implementation approach (environment variables vs external service).

**Secret Management:** Currently using environment variables - evaluate if external secret management (HashiCorp Vault, AWS Secrets Manager) is needed.

**Monitoring Stack:** Define preferred monitoring and observability tools (Prometheus/Grafana, DataDog, New Relic, etc.).

**Release Cadence:** Establish regular release schedule (weekly, bi-weekly, monthly) and deployment windows.