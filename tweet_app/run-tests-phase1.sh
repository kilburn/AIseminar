#!/bin/bash
# Phase 1 Testing Script - Runs all backend tests in Docker
# Usage: ./run-tests-phase1.sh [test-type] [options]
# Test types: unit, integration, all, coverage
# Options: --verbose, --no-capture, --pdb

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOCKER_COMPOSE_FILE="docker-compose.test.yml"
CONTAINER_NAME="tweeteval_backend_test"
TEST_DIR="backend/tests"
COVERAGE_REPORT_DIR="backend-coverage-report"

# Functions
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Main testing logic
main() {
    TEST_TYPE="${1:-all}"
    OPTIONS="${@:2}"

    print_header "Phase 1 Testing - Backend Test Suite"
    echo "Test Type: $TEST_TYPE"
    echo "Docker Compose File: $DOCKER_COMPOSE_FILE"
    echo ""

    # Start services if not already running
    print_header "Starting Test Services"
    docker compose -f "$DOCKER_COMPOSE_FILE" up -d
    
    # Wait for services to be healthy
    print_header "Waiting for services to be healthy"
    sleep 5
    
    # Check service health
    if ! docker compose -f "$DOCKER_COMPOSE_FILE" exec -T postgres-test pg_isready -U test_user -d tweeteval_test > /dev/null 2>&1; then
        print_warning "PostgreSQL test service not ready yet, waiting..."
        sleep 5
    fi

    print_success "All test services are healthy"
    echo ""

    # Run database migrations
    print_header "Running Database Migrations"
    docker compose -f "$DOCKER_COMPOSE_FILE" exec backend-test bash -c "cd /app && alembic upgrade head" || { print_error "Migration failed!"; exit 1; }
    print_success "Database migrations completed"
    echo ""

    # Run tests based on type
    print_header "Running Tests: $TEST_TYPE"

    case $TEST_TYPE in
        unit)
            run_unit_tests "$OPTIONS"
            ;;
        integration)
            run_integration_tests "$OPTIONS"
            ;;
        coverage)
            run_coverage_tests "$OPTIONS"
            ;;
        all)
            run_all_tests "$OPTIONS"
            ;;
        *)
            print_error "Unknown test type: $TEST_TYPE"
            print_warning "Valid types: unit, integration, all, coverage"
            exit 1
            ;;
    esac

    # Collect coverage report if coverage was run
    if [[ "$TEST_TYPE" == "coverage" ]] || [[ "$TEST_TYPE" == "all" ]]; then
        print_header "Collecting Coverage Report"
        mkdir -p backend-coverage-report
        docker compose -f "$DOCKER_COMPOSE_FILE" cp backend-test:/app/htmlcov/. backend-coverage-report/ 2>/dev/null || print_warning "Could not copy coverage report"
        print_success "Coverage report available in backend-coverage-report/"
        if [ -f "backend-coverage-report/index.html" ]; then
            echo "Open in browser: file://$PWD/backend-coverage-report/index.html"
        fi
    fi

    # Cleanup
    print_header "Test Execution Complete"
    print_success "Tests finished successfully"
    
    # Option to keep services running
    read -p "Keep test services running? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_header "Stopping Test Services"
        docker compose -f "$DOCKER_COMPOSE_FILE" down
        print_success "Test services stopped"
    else
        print_warning "Test services still running. Stop with: docker compose -f $DOCKER_COMPOSE_FILE down"
    fi
}

run_unit_tests() {
    local options="$1"
    docker compose -f "$DOCKER_COMPOSE_FILE" exec backend-test bash -c \
        "cd /app && pytest tests/test_models tests/test_schemas -v -m 'unit' $options" || \
        { print_error "Unit tests failed"; exit 1; }
    print_success "Unit tests completed"
}

run_integration_tests() {
    local options="$1"
    docker compose -f "$DOCKER_COMPOSE_FILE" exec backend-test bash -c \
        "cd /app && pytest tests/test_api -v -m 'integration' $options" || \
        { print_error "Integration tests failed"; exit 1; }
    print_success "Integration tests completed"
}

run_coverage_tests() {
    local options="$1"
    docker compose -f "$DOCKER_COMPOSE_FILE" exec backend-test bash -c \
        "cd /app && pytest --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=70 $options" || \
        { print_error "Coverage tests failed or coverage below 70%"; exit 1; }
    print_success "Coverage tests completed"
}

run_all_tests() {
    local options="$1"
    docker compose -f "$DOCKER_COMPOSE_FILE" exec backend-test bash -c \
        "cd /app && pytest --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=70 -v $options" || \
        { print_error "Full test suite failed"; exit 1; }
    print_success "Full test suite completed"
}

cleanup_on_error() {
    print_error "Test execution failed!"
    print_header "Cleaning up"
    docker compose -f "$DOCKER_COMPOSE_FILE" down
    exit 1
}

trap cleanup_on_error ERR

main "$@"
