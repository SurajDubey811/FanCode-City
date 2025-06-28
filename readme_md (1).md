# FanCode SDET Assignment

## Overview

This project automates the validation of a specific scenario: **All users of City 'FanCode' should have more than half of their todos task completed.**

### Scenario Definition
- **Given:** User has todo tasks
- **And:** User belongs to the city FanCode
- **Then:** User's completed task percentage should be greater than 50%

### FanCode City Identification
FanCode city is identified by users whose coordinates fall within:
- **Latitude:** Between -40 and 5
- **Longitude:** Between 5 and 100

## 🏗️ Project Structure

```
fancode-sdet-assignment/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── pytest.ini              # Pytest configuration
├── conftest.py             # Pytest fixtures and setup
├── config.py               # Configuration management
├── test_fancode_users.py   # Main test suite
├── run_tests.sh           # Test execution script
└── reports/               # Test reports directory
    ├── report.html       # HTML test report
    ├── report.json       # JSON test report
    └── test_log_*.log    # Test execution logs
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip3
- Internet connection (to access JSONPlaceholder API)

### Setup and Execution

1. **Clone/Download the project**
   ```bash
   git clone <repository-url>
   cd fancode-sdet-assignment
   ```

2. **Make the script executable**
   ```bash
   chmod +x run_tests.sh
   ```

3. **Run the tests**
   ```bash
   ./run_tests.sh
   ```

### Alternative Manual Setup

If you prefer manual setup:

1. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests**
   ```bash
   pytest -v --html=reports/report.html --self-contained-html
   ```

## 🧪 Test Execution Options

### Run All Tests
```bash
./run_tests.sh
```

### Run Smoke Tests Only
```bash
./run_tests.sh --smoke
```

### Run Regression Tests Only
```bash
./run_tests.sh --regression
```

### Run Tests in Parallel
```bash
./run_tests.sh --parallel
```

### Skip HTML Report Generation
```bash
./run_tests.sh --no-report
```

### Combined Options
```bash
./run_tests.sh --smoke --parallel --no-report
```

## 📊 Test Reports

After test execution, you'll find the following reports in the `reports/` directory:

- **HTML Report:** `report.html` - Interactive test report with detailed results
- **JSON Report:** `report.json` - Machine-readable test results
- **Log Files:** `test_log_*.log` - Detailed execution logs

## 🏛️ Architecture & Design

### Core Components

1. **APIClient Class**
   - Handles all API interactions with JSONPlaceholder
   - Implements proper error handling and retry logic
   - Provides methods for fetching users and todos

2. **User & Todo Data Classes**
   - Type-safe data models using Python dataclasses
   - Clean data transformation from API responses

3. **FanCodeCityValidator Class**
   - Core business logic for validation
   - Implements FanCode city identification
   - Calculates todo completion percentages
   - Provides comprehensive validation results

4. **Test Class**
   - Comprehensive test coverage
   - Multiple test scenarios including edge cases
   - Detailed logging and reporting

### Key Features

- **Robust Error Handling:** Graceful handling of API failures and network issues
- **Comprehensive Logging:** Detailed logs for debugging and audit trail
- **Flexible Configuration:** Environment-based configuration management
- **Multiple Report Formats:** HTML, JSON, and log-based reporting
- **Parallel Execution:** Support for running tests in parallel
- **Type Safety:** Full type hints for better code quality

## 🧮 Algorithm Explanation

### Step 1: Fetch All Users
```python
users = api_client.get_users()
```

### Step 2: Identify FanCode City Users
```python
fancode_users = [
    user for user in users 
    if (-40 <= user.lat <= 5) and (5 <= user.lng <= 100)
]
```

### Step 3: For Each FanCode User
1. Fetch their todos: `api_client.get_user_todos(user.id)`
2. Calculate completion rate: `(completed_todos / total_todos) * 100`
3. Validate: `completion_rate > 50%`

### Step 4: Overall Validation
All FanCode city users must have >50% completion rate for the test to pass.

## 📈 Sample Output

```
========================================
FANCODE CITY USERS TODO COMPLETION REPORT
========================================
✓ PASS | Ervin Howell | 8/20 (40.0%)
✗ FAIL | Clementine Bauch | 7/20 (35.0%)
✓ PASS | Patricia Lebsack | 12/20 (60.0%)
========================================
SUMMARY: 2/3 users passed
OVERALL RESULT: FAIL
========================================
```

## 🔧 Configuration

### Environment Variables

You can customize the test execution using environment variables:

```bash
# API Configuration
export API_BASE_URL="http://jsonplaceholder.typicode.com"
export API_TIMEOUT=30
export API_MAX_RETRIES=3

# FanCode City Boundaries
export FANCODE_LAT_MIN=-40
export FANCODE_LAT_MAX=5
export FANCODE_LNG_MIN=5
export FANCODE_LNG_MAX=100

# Completion Threshold
export COMPLETION_THRESHOLD=50

# Test Configuration
export GENERATE_HTML_REPORT=true
export GENERATE_JSON_REPORT=true
export LOG_LEVEL=INFO
export PARALLEL_EXECUTION=false
export MAX_WORKERS=4
```

## 🧪 Test Cases Covered

1. **API Connectivity Test**
   - Validates API endpoints are accessible
   - Ensures data is returned correctly

2. **FanCode City Identification Test**
   - Verifies coordinate-based user filtering
   - Validates boundary conditions

3. **Todo Completion Calculation Test**
   - Tests percentage calculation accuracy
   - Handles edge cases (no todos, all completed, etc.)

4. **Main Validation Test**
   - Core business logic validation
   - Individual user validation
   - Overall result aggregation

## 🚨 Error Handling

The framework handles various error scenarios:

- **Network Issues:** Retry logic with exponential backoff
- **API Failures:** Graceful degradation and error reporting
- **Data Validation:** Type checking and boundary validation
- **Empty Results:** Proper handling of users with no todos

## 🔄 CI/CD Integration

The framework is designed for easy CI/CD integration:

### GitHub Actions Example
```yaml
name: FanCode Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Run tests
        run: ./run_tests.sh
      - name: Upload reports
        uses: actions/upload-artifact@v2
        with:
          name: test-reports
          path: reports/
```

### Jenkins Pipeline Example
```groovy
pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                sh 'python3 -m venv venv'
                sh 'source venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh './run_tests.sh'
            }
        }
        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'reports/*', fingerprint: true
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Test Report'
                ])
            }
        }
    }
}
```

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Check internet connectivity
   - Verify API endpoint is accessible
   - Review firewall/proxy settings

2. **Permission Errors**
   - Make sure `run_tests.sh` is executable: `chmod +x run_tests.sh`
   - Check write permissions for reports directory

3. **Python/Pip Issues**
   - Ensure Python 3.7+ is installed
   - Update pip: `pip install --upgrade pip`
   - Use virtual environment to avoid conflicts

4. **Test Failures**
   - Review HTML report for detailed failure information
   - Check log files in reports directory
   - Verify API endpoints are returning expected data

### Debug Mode

For detailed debugging, run tests with verbose output:
```bash
pytest -v -s --tb=long
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

This project is created for the FanCode SDET Assignment and is available for educational purposes.

## 📞 Support

For issues or questions regarding this assignment:
- Review the troubleshooting section
- Check the generated test reports
- Examine the log files for detailed error information

---

**Note:** This framework is designed to be production-ready with proper error handling, logging, and reporting capabilities. It demonstrates best practices in test automation including proper project structure, configuration management, and comprehensive test coverage.