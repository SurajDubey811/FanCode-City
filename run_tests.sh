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
    PYTEST_CMD="$PYTEST_CMD --alluredir=reports/allure-results --clean-alluredir"
    print_status "Allure report generation enabled"
fi

# Run the tests
print_status "Starting test execution..."
echo "Command: $PYTEST_CMD"
echo "=========================================="

if $PYTEST_CMD; then
    print_success "All tests completed successfully!"
    
    # Generate Allure report
    if [ "$GENERATE_REPORT" = "true" ]; then
        print_status "Generating Allure report..."
        if command -v allure &> /dev/null; then
            allure generate reports/allure-results -o reports/allure-report --clean
            if [ $? -eq 0 ]; then
                print_status "Allure report generated: $(pwd)/reports/allure-report/index.html"
                print_status "To view the report, open: $(pwd)/reports/allure-report/index.html"
                print_status "To serve the report, run: allure serve reports/allure-results"
            else
                print_warning "Failed to generate Allure report"
                print_status "Raw test results available in: $(pwd)/reports/allure-results"
            fi
        else
            print_warning "Allure CLI not found. Install it with: npm install -g allure-commandline"
            print_status "Raw test results available in: $(pwd)/reports/allure-results"
        fi
    fi
    
    # Show log files
    if ls reports/test_log_*.log 1> /dev/null 2>&1; then
        print_status "Log files available in reports/ directory"
    fi
    
    echo "=========================================="
    print_success "Test execution completed successfully!"
    
else
    print_error "Some tests failed. Check the reports for details."
    
    # Generate Allure report even on failure
    if [ "$GENERATE_REPORT" = "true" ]; then
        print_status "Generating Allure report..."
        if command -v allure &> /dev/null; then
            allure generate reports/allure-results -o reports/allure-report --clean
            if [ $? -eq 0 ]; then
                print_status "Allure report generated: $(pwd)/reports/allure-report/index.html"
                print_status "To serve the report, run: allure serve reports/allure-results"
            else
                print_warning "Failed to generate Allure report"
                print_status "Raw test results available in: $(pwd)/reports/allure-results"
            fi
        else
            print_warning "Allure CLI not found. Install it with: npm install -g allure-commandline"
            print_status "Raw test results available in: $(pwd)/reports/allure-results"
        fi
    fi
    echo "=========================================="
    exit 1
fi

# Deactivate virtual environment
deactivate