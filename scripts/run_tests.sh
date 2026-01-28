#!/bin/bash
# Test runner script for OpenAspen

set -e

echo "🧪 Running OpenAspen test suite..."

# Run tests with coverage
poetry run pytest \
    --cov=openaspen \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-report=xml \
    -v \
    "$@"

echo ""
echo "✅ Tests completed!"
echo "📊 Coverage report: htmlcov/index.html"
