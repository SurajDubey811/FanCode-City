#!/bin/bash

# FanCode SDET Assignment - Test Execution Script
# This script sets up the environment and runs the test suite

set -e  # Exit on any error

echo "=========================================="
echo "FanCode SDET Assignment - Test Execution"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python3 is not installed. Please install Python3 to continue."
    exit 1
fi

print_status "Python3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3 to continue."
    exit 1
fi

print_status "pip3 found: $(pip3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt
print_success "Dependencies installed successfully"

# Create reports directory
mkdir -p reports

# Set environment variables (optional)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Parse command line arguments
RUN_MODE="all"
GENERATE_REPORT="true"
PARALLEL="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        --smoke)
            RUN_MODE="smoke"
            shift
            ;;
        --regression)
            RUN_MODE="regression"
            shift
            ;;
        --no-report)
            GENERATE_REPORT="false"
            shift
            ;;
        --parallel)
            PARALLEL="true"
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --smoke       Run only smoke tests"
            echo "  --regression  Run only regression tests"
            echo "  --no-report   Skip HTML report generation"
            echo "  --parallel    Run tests in parallel"
            echo "  --help        Show this help message"
            exit 0
            ;;
        *)
            print_warning "Unknown option: $1"
            shift
            ;;
    esac
done

# Build pytest command
PYTEST_CMD="pytest -v"

# Add markers based on run mode
case $RUN_MODE in
    "smoke")
        PYTEST_CMD="$PYTEST_CMD -m smoke"
        print_status "Running smoke tests only"
        ;;
    "regression")
        PYTEST_CMD="$PYTEST_CMD -m regression"
        print_status "Running regression tests only"
        ;;
    *)
        print_status "Running all tests"
        ;;
esac

# Add parallel execution if requested
if [ "$PARALLEL" = "true" ]; then
    PYTEST_CMD="$PYTEST_CMD -n auto"
    print_status "Parallel execution enabled"
fi

# Add report generation
if [ "$GENERATE_REPORT" = "true" ]; then
    PYTEST_CMD="$PYTEST_CMD --html=reports/report.html --self-contained-html"
    print_status "HTML report generation enabled"
fi

# Run the tests
print_status "Starting test execution..."
echo "Command: $PYTEST_CMD"
echo "=========================================="

if $PYTEST_CMD; then
    print_success "All tests completed successfully!"
    
    # Show report location
    if [ "$GENERATE_REPORT" = "true" ]; then
        print_status "HTML report generated: $(pwd)/reports/report.html"
        print_status "JSON report generated: $(pwd)/reports/report.json"
    fi
    
    # Show log files
    if ls reports/test_log_*.log 1> /dev/null 2>&1; then
        print_status "Log files available in reports/ directory"
    fi
    
    echo "=========================================="
    print_success "Test execution completed successfully!"
    
else
    print_error "Some tests failed. Check the reports for details."
    echo "=========================================="
    exit 1
fi

# Deactivate virtual environment
deactivate