#!/bin/bash

# Test runner script for TweetEval NLP Platform
# This script runs both backend and frontend tests

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Running TweetEval Platform Tests${NC}"
echo "======================================"

# Function to print status
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Check if services are running
print_status "Checking if services are running..."
if ! docker compose -f docker-compose.dev.yml ps | grep -q "Up (healthy)"; then
    print_warning "Some services are not healthy. Starting services..."
    docker compose -f docker-compose.dev.yml up -d

    # Wait for services to be healthy
    print_status "Waiting for services to be healthy..."
    for i in {1..30}; do
        if docker compose -f docker-compose.dev.yml ps | grep -q "Up (healthy)"; then
            print_status "Services are healthy!"
            break
        fi
        if [ $i -eq 30 ]; then
            print_error "Services did not become healthy in time."
            docker compose -f docker-compose.dev.yml logs --tail=50
            exit 1
        fi
        sleep 2
    done
fi

# Run backend tests
print_status "Running backend tests..."
if docker compose -f docker-compose.dev.yml exec -T backend python -m pytest --version > /dev/null 2>&1; then
    print_status "Installing test dependencies..."
    docker compose -f docker-compose.dev.yml exec -T backend pip install -r requirements-test.txt

    print_status "Running pytest..."
    docker compose -f docker-compose.dev.yml exec -T backend python -m pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=70

    BACKEND_EXIT_CODE=$?
    if [ $BACKEND_EXIT_CODE -eq 0 ]; then
        print_status "✅ Backend tests passed!"
    else
        print_error "❌ Backend tests failed!"
        exit $BACKEND_EXIT_CODE
    fi
else
    print_warning "Pytest not available in backend container. Installing..."
    docker compose -f docker-compose.dev.yml exec -T backend pip install pytest pytest-asyncio pytest-cov httpx
    print_status "Running backend tests..."
    docker compose -f docker-compose.dev.yml exec -T backend python -m pytest tests/ -v
fi

# Run frontend tests
print_status "Running frontend tests..."
if docker compose -f docker-compose.dev.yml exec -T frontend npm run test -- --version > /dev/null 2>&1; then
    print_status "Running Vitest..."
    docker compose -f docker-compose.dev.yml exec -T frontend npm run test -- --run --coverage

    FRONTEND_EXIT_CODE=$?
    if [ $FRONTEND_EXIT_CODE -eq 0 ]; then
        print_status "✅ Frontend tests passed!"
    else
        print_error "❌ Frontend tests failed!"
        exit $FRONTEND_EXIT_CODE
    fi
else
    print_warning "Vitest not available. Installing..."
    docker compose -f docker-compose.dev.yml exec -T frontend npm install
    print_status "Running frontend tests..."
    docker compose -f docker-compose.dev.yml exec -T frontend npm run test -- --run
fi

# Run integration tests if available
print_status "Running integration tests..."
if [ -f "tests/integration/run-integration.sh" ]; then
    bash tests/integration/run-integration.sh
    INTEGRATION_EXIT_CODE=$?
    if [ $INTEGRATION_EXIT_CODE -eq 0 ]; then
        print_status "✅ Integration tests passed!"
    else
        print_error "❌ Integration tests failed!"
        exit $INTEGRATION_EXIT_CODE
    fi
else
    print_warning "No integration tests found. Skipping."
fi

# Generate test summary
print_status "Generating test summary..."
echo ""
echo "======================================"
echo "🎉 All tests completed successfully!"
echo "======================================"
echo ""
echo "📊 Test Results Summary:"
echo "  ✅ Backend: Unit tests with $(docker compose -f docker-compose.dev.yml exec -T backend python -c "import os; print('coverage enabled' if os.path.exists('htmlcov') else 'coverage disabled')" 2>/dev/null || echo "coverage disabled")"
echo "  ✅ Frontend: Unit tests with coverage"
echo "  ✅ Services: All containers running and healthy"
echo ""
echo "📁 Generated Reports:"
echo "  - Backend coverage: backend/htmlcov/index.html"
echo "  - Frontend coverage: frontend/coverage/index.html"
echo ""
echo "🔗 Next Steps:"
echo "  1. Review test coverage reports"
echo "  2. Check any failing tests"
echo "  3. Run integration tests if needed"
echo "  4. Deploy to staging environment"
echo ""

# Show service status
print_status "Final service status:"
docker compose -f docker-compose.dev.yml ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

echo ""
print_status "✅ Test run completed successfully!"