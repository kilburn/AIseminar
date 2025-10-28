# Phase 1 Testing Quick Reference

## ⚡ Quick Commands

```bash
# Run all tests (recommended)
./run-tests-phase1.sh all

# Run unit tests only
./run-tests-phase1.sh unit

# Run integration tests only
./run-tests-phase1.sh integration

# Generate coverage report
./run-tests-phase1.sh coverage

# Verbose output
./run-tests-phase1.sh all --verbose
```

## 📂 Test Files Location

```
backend/tests/
├── test_api/
│   ├── test_auth.py              # Authentication tests
│   ├── test_datasets.py          # Dataset endpoints
│   └── test_integration.py       # Integration scenarios
├── test_models/
│   ├── test_user.py              # User model tests
│   └── test_dataset.py           # Dataset model tests
└── test_schemas/
    ├── test_user_schemas.py      # User validation
    └── test_dataset_schemas.py   # Dataset validation
```

## 🐳 Docker Commands (Manual)

```bash
# Start test environment
docker compose -f docker-compose.test.yml up -d

# Run migrations
docker compose -f docker-compose.test.yml exec backend-test alembic upgrade head

# Run tests
docker compose -f docker-compose.test.yml exec backend-test pytest

# Run specific test
docker compose -f docker-compose.test.yml exec backend-test pytest tests/test_models/test_user.py

# View logs
docker compose -f docker-compose.test.yml logs backend-test

# Stop services
docker compose -f docker-compose.test.yml down
```

## 📊 Coverage Report

After running tests:
- **Terminal Output**: Shows in console with missing lines
- **HTML Report**: `backend-coverage-report/index.html`
- **Coverage Threshold**: 70% minimum (enforced)

## 🔍 Test Database Access

```bash
# Connect to PostgreSQL test database
psql -h localhost -p 25432 -U test_user -d tweeteval_test

# Connect to Qdrant API
curl http://localhost:26333/docs

# Connect to Redis test cache
redis-cli -h localhost -p 26379
```

## ✅ What's Tested (Phase 1)

**Authentication**
- ✅ User registration
- ✅ User login
- ✅ JWT token validation
- ✅ Protected routes

**Dataset Management**
- ✅ Create/Read/Update/Delete
- ✅ Access control
- ✅ Status tracking
- ✅ File integrity

**User Management**
- ✅ User creation
- ✅ Unique constraints
- ✅ Status tracking
- ✅ Email verification

**Schema Validation**
- ✅ Required fields
- ✅ Data types
- ✅ Formats
- ✅ Edge cases

## 🚨 Troubleshooting

**Port in use**
```bash
docker ps | grep tweeteval
docker stop <container_id>
```

**Services not healthy**
```bash
docker compose -f docker-compose.test.yml ps
docker compose -f docker-compose.test.yml logs postgres-test
```

**Tests fail to connect**
```bash
# Wait longer for services
sleep 10
docker compose -f docker-compose.test.yml exec backend-test pytest
```

## 📋 File Checklist

- ✅ `docker-compose.test.yml` - Test environment
- ✅ `run-tests-phase1.sh` - Test runner script
- ✅ `backend/pytest.ini` - Pytest configuration
- ✅ `backend/requirements-test.txt` - Test dependencies
- ✅ `backend/tests/conftest.py` - Test fixtures
- ✅ `docs/development/phase-1-testing.md` - Full documentation

## 🎯 Key Statistics

| Metric | Value |
|--------|-------|
| Test Files | 6 files |
| Test Cases | 30+ cases |
| Target Coverage | 70%+ |
| Execution Time | ~1 minute |
| Docker Services | 4 services |
| Isolation Level | Complete |

## 🔄 CI/CD Ready

Tests are ready for integration with:
- GitHub Actions
- GitLab CI
- Jenkins
- Docker CI/CD pipelines

Simply call: `./run-tests-phase1.sh all`

## 📝 Notes

- ⚠️ NO direct Python execution - all tests run in Docker
- ⚠️ Fresh database state per test run
- ⚠️ Automatic cleanup after tests
- ✅ Fully container-based
- ✅ Reproducible results

## 🎓 Learn More

See full documentation at:
`docs/development/phase-1-testing.md`

---

**Last Updated**: 2025-10-28  
**Status**: ✅ Ready for Use
