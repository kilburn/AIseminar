# Phase 1 Testing Documentation

**Version**: 1.0.0  
**Created**: 2025-10-28  
**Status**: Active  
**Feature Branch**: `001-tweeteval-nlp-platform`

## Overview

This document provides comprehensive testing guidance for Phase 1 of the TweetEval NLP Analysis Platform. All testing follows the project constitution requirement of **container-only development** - NO direct Python execution is allowed. All tests must run within Docker containers.

## Testing Architecture

### Container-Based Testing Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│          Testing Environment (docker-compose.test.yml)         │
├─────────────────────────────────────────────────────────────────┤
│  • Isolated Test Databases (PostgreSQL, Qdrant, Redis)         │
│  • Independent from Development Environment                    │
│  • Automatic Service Health Checks                             │
│  • Fresh Database State for Each Test Run                      │
│  • Integrated Coverage Reporting                               │
└─────────────────────────────────────────────────────────────────┘
```

### Key Testing Principles

1. **Isolation**: Tests run in isolated containers with fresh database state
2. **Repeatability**: Same test always produces same result regardless of environment
3. **Coverage**: Target minimum 70% code coverage (enforced in pytest.ini)
4. **Container-Only**: NO direct Python execution - all commands via Docker
5. **CI/CD Ready**: Scripts designed for automated integration

## Test Directories and Structure

```
backend/tests/
├── __init__.py                      # Test package initialization
├── conftest.py                      # Shared pytest fixtures and configuration
│
├── test_api/                        # API Endpoint Tests
│   ├── __init__.py
│   ├── test_auth.py                # Authentication endpoint tests
│   ├── test_datasets.py            # Dataset management endpoint tests
│   └── test_integration.py         # Full integration tests
│
├── test_models/                     # Database Model Tests
│   ├── __init__.py
│   ├── test_user.py                # User model unit tests
│   └── test_dataset.py             # Dataset model unit tests
│
└── test_schemas/                    # Pydantic Schema Tests
    ├── __init__.py
    ├── test_user_schemas.py        # User schema validation tests
    └── test_dataset_schemas.py     # Dataset schema validation tests
```

## Test Coverage - Phase 1

### Authentication System (Priority: P1)

**Test File**: `tests/test_api/test_auth.py`

| Scenario | Status | Coverage |
|----------|--------|----------|
| User registration with valid data | ✅ | 100% |
| Registration fails with duplicate email | ✅ | 100% |
| User login with correct credentials | ✅ | 100% |
| Login fails with invalid password | ✅ | 100% |
| Protected routes require JWT token | ✅ | 100% |
| Token refresh functionality | ⏳ | Phase 2 |
| Password reset flow | ⏳ | Phase 2 |

### Dataset Management (Priority: P1)

**Test Files**: 
- `tests/test_api/test_datasets.py` (API endpoints)
- `tests/test_models/test_dataset.py` (Database models)

| Scenario | Status | Coverage |
|----------|--------|----------|
| Create dataset | ✅ | 100% |
| List user's datasets | ✅ | 100% |
| Get dataset details | ✅ | 100% |
| Update dataset metadata | ✅ | 100% |
| Delete dataset | ✅ | 100% |
| Dataset visibility controls (public/private) | ✅ | 100% |
| Dataset status transitions | ✅ | 100% |
| Error handling during processing | ✅ | 100% |
| Unauthorized access prevention | ✅ | 100% |
| File integrity tracking | ✅ | 100% |

### User Management (Priority: P1)

**Test Files**:
- `tests/test_models/test_user.py` (Database models)
- `tests/test_schemas/test_user_schemas.py` (Schema validation)

| Scenario | Status | Coverage |
|----------|--------|----------|
| User creation with valid data | ✅ | 100% |
| Unique username/email constraints | ✅ | 100% |
| User timestamps tracking | ✅ | 100% |
| Active/inactive status | ✅ | 100% |
| Email verification status | ✅ | 100% |
| Last login tracking | ✅ | 100% |

### Schema Validation (Priority: P1)

**Test File**: `tests/test_schemas/test_dataset_schemas.py`

| Validation | Status | Coverage |
|-----------|--------|----------|
| Required field validation | ✅ | 100% |
| Data type validation | ✅ | 100% |
| Email format validation | ✅ | 100% |
| String length constraints | ✅ | 100% |
| Optional field handling | ✅ | 100% |
| Special characters handling | ✅ | 100% |

## Running Tests

### Prerequisites

1. **Docker and Docker Compose installed**
   ```bash
   docker --version
   docker compose --version
   ```

2. **Make script executable**
   ```bash
   chmod +x run-tests-phase1.sh
   ```

3. **Environment file configured**
   ```bash
   cp .env.example .env
   ```

### Test Execution Methods

#### Method 1: Using Test Script (Recommended)

```bash
# Run all tests with coverage
./run-tests-phase1.sh all

# Run only unit tests
./run-tests-phase1.sh unit

# Run only integration tests
./run-tests-phase1.sh integration

# Run with coverage report
./run-tests-phase1.sh coverage

# Run with verbose output
./run-tests-phase1.sh all --verbose

# Run with no output capture (see print statements)
./run-tests-phase1.sh all --no-capture
```

#### Method 2: Direct Docker Compose

```bash
# Start test environment
docker compose -f docker-compose.test.yml up -d

# Run migrations
docker compose -f docker-compose.test.yml exec backend-test alembic upgrade head

# Run all tests
docker compose -f docker-compose.test.yml exec backend-test pytest

# Run specific test file
docker compose -f docker-compose.test.yml exec backend-test pytest tests/test_models/test_user.py

# Run specific test
docker compose -f docker-compose.test.yml exec backend-test pytest tests/test_models/test_user.py::TestUserModel::test_user_creation

# Run with coverage
docker compose -f docker-compose.test.yml exec backend-test pytest --cov=app --cov-report=html

# Stop services
docker compose -f docker-compose.test.yml down
```

#### Method 3: Interactive Debugging

```bash
# Start test environment
docker compose -f docker-compose.test.yml up -d

# Enter backend test container shell
docker compose -f docker-compose.test.yml exec backend-test bash

# Inside container:
# Run pytest with debugging
pytest tests/test_models/test_user.py -v --pdb

# Run single test
pytest tests/test_models/test_user.py::TestUserModel::test_user_creation -v

# Exit shell
exit
```

### Test Configuration

**File**: `backend/pytest.ini`

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v                              # Verbose output
    --tb=short                      # Short traceback format
    --strict-markers                # Strict marker checking
    --disable-warnings              # Disable warnings
    --cov=app                       # Coverage for app module
    --cov-report=term-missing       # Terminal coverage report
    --cov-report=html               # HTML coverage report
    --cov-fail-under=70             # Fail if coverage < 70%
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    auth: marks tests related to authentication
    datasets: marks tests related to dataset management
    nlp: marks tests related to NLP processing
    search: marks tests related to search functionality
asyncio_mode = auto
```

## Test Dependencies

**File**: `backend/requirements-test.txt`

```
pytest>=7.4.0              # Test framework
pytest-asyncio>=0.21.0    # Async test support
httpx>=0.24.0             # HTTP client for API testing
pytest-cov>=4.1.0         # Coverage measurement
factory-boy>=3.3.0        # Test data factories
faker>=19.0.0             # Fake data generation
```

## Coverage Requirements

### Phase 1 Target Coverage: 70%+

Coverage is enforced through pytest configuration and will fail tests if not met.

### Coverage Report

After running tests, coverage reports are generated:

```bash
# Terminal report
# Shown in console output with missing lines highlighted

# HTML report
# Generated in: backend-coverage-report/index.html
# Open in browser: file:///path/to/backend-coverage-report/index.html

# JSON report (available in coverage.json)
# Can be integrated with CI/CD systems
```

### Improving Coverage

1. **Identify uncovered code**: Check HTML coverage report
2. **Add edge case tests**: Test boundary conditions
3. **Add integration tests**: Test service interactions
4. **Mock external services**: Isolate functionality

Example of adding coverage:

```python
# Identify missing coverage in code
# Add test case for missing scenario
def test_edge_case_scenario(self, client, sample_data):
    """Test specific edge case that wasn't covered."""
    response = await client.post(
        "/api/v1/endpoint",
        json=sample_data
    )
    assert response.status_code == expected_status
```

## Test Database Configuration

### PostgreSQL Test Database

- **Container**: `postgres-test`
- **Database**: `tweeteval_test`
- **User**: `test_user`
- **Password**: `test_pass` (from `.env`)
- **Port**: `25432` (mapped from internal 5432)

### Qdrant Test Vector Database

- **Container**: `qdrant-test`
- **Port**: `26333` (mapped from internal 6333)
- **Storage**: `qdrant_test_data` volume
- **Initialization**: Empty, populated during tests

### Redis Test Cache

- **Container**: `redis-test`
- **Port**: `26379` (mapped from internal 6379)
- **Memory Limit**: 256MB
- **Eviction Policy**: `allkeys-lru`

### Fresh State Between Tests

Each test run:
1. Creates fresh test database with all tables
2. Initializes empty Qdrant collections
3. Clears Redis cache
4. Runs migrations automatically
5. Cleans up after test completion

## Continuous Integration (CI/CD) Integration

### GitHub Actions Example

```yaml
name: Phase 1 Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: docker/setup-buildx-action@v2
      
      - name: Run tests
        run: ./run-tests-phase1.sh all
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./backend-coverage-report/coverage.xml
          flags: unittests
```

### Local Pre-commit Testing

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "Running Phase 1 tests before commit..."
./run-tests-phase1.sh all --no-capture
if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi
```

## Common Issues and Solutions

### Issue: Services Not Healthy

```bash
# Problem: Services taking too long to start
# Solution: Increase wait time or check logs

docker compose -f docker-compose.test.yml logs postgres-test
docker compose -f docker-compose.test.yml logs qdrant-test
```

### Issue: Database Migrations Failing

```bash
# Problem: Migration errors during test setup
# Solution: Verify alembic configuration

docker compose -f docker-compose.test.yml exec backend-test \
    alembic current

docker compose -f docker-compose.test.yml exec backend-test \
    alembic history
```

### Issue: Flaky Tests (Intermittent Failures)

```bash
# Problem: Tests pass sometimes, fail others
# Solution: Run tests multiple times

for i in {1..5}; do
    echo "Run $i:"
    ./run-tests-phase1.sh all
done
```

### Issue: Port Already in Use

```bash
# Problem: Port 25432 or 26333 already in use
# Solution: Stop conflicting containers

docker ps | grep tweeteval
docker stop <container_id>

# Or: Change ports in docker-compose.test.yml
```

### Issue: Out of Memory

```bash
# Problem: Docker container running out of memory
# Solution: Increase memory limit or reduce concurrency

# In docker-compose.test.yml, add memory limit:
memswap_limit: 2g
mem_limit: 1g
```

## Best Practices

### 1. Test Organization

- **One assertion focus**: Each test tests one behavior
- **Clear naming**: Test names describe what is tested
- **Arrange-Act-Assert**: Organize tests logically
- **Fixtures for setup**: Use pytest fixtures for test data

### 2. Test Data Management

```python
@pytest.fixture
def sample_user_data():
    """Provides consistent test data."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
```

### 3. Async Test Handling

```python
@pytest.mark.asyncio
async def test_async_operation(self, db_session):
    """Test async database operations."""
    result = await db_session.execute(query)
    assert result is not None
```

### 4. Mocking External Services

```python
@patch('app.services.external_service.call')
def test_with_mock(self, mock_service):
    """Mock external service calls."""
    mock_service.return_value = {"status": "success"}
    result = my_function()
    assert result["status"] == "success"
```

### 5. Error Condition Testing

```python
def test_error_handling(self, client):
    """Test error responses."""
    response = client.post("/api/v1/endpoint", json={})
    assert response.status_code == 400
    assert "error" in response.json()
```

## Monitoring and Metrics

### Test Metrics to Track

- **Test Duration**: How long tests take to run
- **Coverage Trends**: Coverage percentage over time
- **Failure Rate**: Percentage of failing tests
- **Test Count**: Growth of test suite

### Performance Benchmarks

| Metric | Target | Current |
|--------|--------|---------|
| Full test suite duration | <2 min | TBD |
| Unit tests duration | <30 sec | TBD |
| Integration tests duration | <90 sec | TBD |
| Coverage percentage | ≥70% | TBD |

## Next Steps (Phase 2)

Phase 2 testing will add:

1. **NLP Processing Tests**
   - TweetEval model output validation
   - Embedding generation tests
   - Batch processing tests

2. **Search Functionality Tests**
   - Semantic similarity tests
   - Qdrant integration tests
   - Search performance tests

3. **Background Task Tests**
   - Celery task testing
   - Long-running process tests
   - Error recovery tests

4. **End-to-End Tests**
   - Complete workflow tests
   - User journey tests
   - Performance tests

## Support and Troubleshooting

### Getting Help

1. **Check test output**: Review error messages carefully
2. **Review logs**: `docker compose -f docker-compose.test.yml logs`
3. **Interactive debugging**: Use `--pdb` flag for debugging
4. **Test documentation**: Review this document for solutions

### Reporting Issues

When reporting test issues, include:

1. Command run: `./run-tests-phase1.sh all`
2. Error output: Full error message from console
3. Environment: OS, Docker version, Python version
4. Reproducibility: Can issue be reproduced consistently?

## Conclusion

Phase 1 testing provides comprehensive coverage of core functionality with a container-based approach ensuring consistency and reproducibility. All tests follow the project constitution requirement of container-only development with NO direct Python execution.

For updates or questions about Phase 1 testing, refer to the implementation plan and feature specification documents.
