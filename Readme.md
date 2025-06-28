
# FanCode SDET Assignment

Enhanced with **Behavior-Driven Development (BDD)** capabilities using pytest-bdd!

---

## 📚 Table of Contents

- [Overview](#overview)
- [🎯 BDD Framework](#-bdd-framework)
- [Test Suite Execution](#test-suite-execution)
- [Project Structure](#️project-structure)
- [Quick Start](#quick-start)
- [Test Execution Options](#test-execution-options)
- [Test Reports](#test-reports)
- [Architecture & Design](#architecture--design)
- [Algorithm](#algorithm)
- [Configuration](#configuration)
- [Test Cases](#test-cases)
- [Error Handling](#error-handling)
- [CI/CD Integration](#cicd-integration)
- [Running with Docker](#running-with-docker)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Overview

Automated validation to ensure **all users of City 'FanCode' have more than half of their todos completed**.

### Scenario
- **Given:** User has todo tasks
- **And:** User belongs to the city FanCode (lat: -40 to 5, lng: 5 to 100)
- **Then:** User's completed task percentage should be greater than 50%

## 🎯 BDD Framework

This project now supports **Behavior-Driven Development (BDD)** with:
- ✅ **Gherkin syntax** for readable test scenarios
- ✅ **Business-focused** test descriptions
- ✅ **Stakeholder collaboration** through natural language
- ✅ **Comprehensive coverage** of business requirements

**🚀 Quick BDD Start:**
```bat
run_tests_bdd.bat --bdd
```

📖 **For detailed BDD documentation, see [BDD_README.md](BDD_README.md)**

---

## 🚀 Quick Start & Test Suite Execution

### Prerequisites
- Python 3.7+ and pip (in PATH)
- Internet connection (for JSONPlaceholder API)
- All dependencies in `requirements.txt` will be installed automatically.

### 1. Clone/Download
```bash
git clone <repository-url>
cd "FanCode City"
```

### 2. Install dependencies and run tests

**Linux/Mac:**
```sh
chmod +x run_tests.sh
./run_tests.sh [options]
```

**Windows:**
```bat
run_tests.bat [options]
```

**Options:**
- `--smoke`       Run only smoke tests
- `--regression`  Run only regression tests
- `--no-report`   Skip HTML report generation
- `--parallel`    Run tests in parallel
- `--help`        Show help message

**Example:**
```bat
run_tests.bat --regression --parallel
```
This will run only regression tests in parallel and generate an HTML report in the `reports` directory.

---
## 🏗️ Project Structure

```
FanCode City/
├── README.md
├── requirements.txt
├── pytest.ini
├── conftest.py
├── config.py
├── api_client.py
├── user.py
├── todo.py
├── validator.py
├── utils.py
├── run_tests.sh
├── run_tests.bat
├── docker-compose.yml
├── Dockerfile
├── .github/
│   └── workflows/
│       └── main.yml
├── reports/
│   ├── report.html
│   ├── report.json
│   └── test_log_*.log
└── tests/
    ├── __init__.py
    ├── test_fancode_users.py
    ├── test_api_client.py
    ├── test_validator.py
    ├── test_user_model.py
    ├── test_todo_model.py
    ├── test_utils.py
    ├── test_api_client_comprehensive.py
    ├── test_validator_comprehensive.py
    ├── test_models_comprehensive.py
    ├── test_utils_comprehensive.py
    └── test_performance_integration.py
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7+ and pip (in PATH)
- Internet connection (for JSONPlaceholder API)

### Setup & Execution

#### 1. Clone/Download
```bash
git clone <repository-url>
cd FanCode-City
```

#### 2. Install dependencies and run tests

**Linux/Mac:**
```sh
chmod +x run_tests.sh
./run_tests.sh
```

**Windows:**
```bat
run_tests.bat
```

#### 3. Script Options

- `--smoke`       Run only smoke tests
- `--regression`  Run only regression tests
- `--no-report`   Skip HTML report generation
- `--parallel`    Run tests in parallel
- `--help`        Show help message

**Example:**
```bat
run_tests.bat --regression --parallel
```

---

## 🧪 Test Execution Options

| Option         | Description                         |
|----------------|-------------------------------------|
| `--smoke`      | Run only smoke tests                |
| `--regression` | Run only regression tests           |
| `--no-report`  | Skip HTML report generation         |
| `--parallel`   | Run tests in parallel               |
| `--help`       | Show help message                   |

---

## 📊 Test Reports

After execution, reports are in `reports/`:
- **HTML:** `report.html`
- **JSON:** `report.json`
- **Logs:** `test_log_*.log`

---

## 🏛️ Architecture & Design

### Components

- **APIClient:** Handles JSONPlaceholder API interactions with comprehensive error handling and retry logic.
- **User & Todo Data Classes:** Typed models for API data with validation and from_dict factory methods.
- **FanCodeCityValidator:** Core business logic for city identification and todo completion validation.
- **Utilities:** FanCode-specific helper functions for coordinate validation and completion calculations.
- **Comprehensive Test Suite:** Multi-layered testing approach covering unit, integration, performance, and business logic.

### Design Patterns

- **Factory Pattern:** Used in User.from_dict() and Todo.from_dict() for API response parsing
- **Strategy Pattern:** Flexible validation logic in FanCodeCityValidator
- **Repository Pattern:** APIClient abstracts data access from business logic
- **Test Patterns:** Fixtures, Mocking, Parametrized testing, Test categories with markers

---

## 🧮 Algorithm

1. Fetch all users.
2. Identify FanCode city users (lat/lng bounds).
3. For each, fetch todos, calculate completion rate, validate >50%.
4. All must pass for overall success.

---

## 🔧 Configuration

Environment variables can override defaults (API URL, city bounds, thresholds, etc).

---

## 🧪 Test Suite

### Test Categories

The test suite is organized into multiple categories covering all testing concepts:

#### **Core Tests:**
- `test_fancode_users.py` - Main integration tests for FanCode user validation
- `test_api_client.py` - API client integration tests
- `test_validator.py` - Validator logic tests with FanCode-specific markers
- `test_user_model.py` - User data model tests
- `test_todo_model.py` - Todo data model tests
- `test_utils.py` - Utility function tests

#### **Comprehensive Test Suites:**
- `test_api_client_comprehensive.py` - **Integration, Error Handling, Mocking, Performance**
- `test_validator_comprehensive.py` - **Unit, Boundary, Integration, Business Logic**
- `test_models_comprehensive.py` - **Data Models, Edge Cases, FanCode Scenarios**
- `test_utils_comprehensive.py` - **FanCode Utilities, Parametrized Tests**
- `test_performance_integration.py` - **Performance, Load, Stress, E2E Testing**

#### **Test Markers:**
```bash
@pytest.mark.fancode      # FanCode-specific business logic tests
@pytest.mark.api          # API integration tests
@pytest.mark.performance  # Performance and load tests
@pytest.mark.business_logic # Business rule validation
@pytest.mark.load         # Load testing scenarios
@pytest.mark.stress       # Stress testing scenarios
@pytest.mark.reliability  # Reliability and error recovery tests
```

#### **Running Specific Test Categories:**
```bash
# Run all tests
pytest tests/ -v

# Run FanCode-specific tests
pytest -m fancode -v

# Run API integration tests
pytest -m api -v

# Run performance tests
pytest -m performance -v

# Run comprehensive test suites
pytest tests/test_*_comprehensive.py -v

# Run with parallel execution
pytest tests/ -n auto
```

### Test Coverage

The test suite covers:
- **Functional Testing:** Unit, Integration, End-to-End
- **Non-Functional Testing:** Performance, Load, Stress, Reliability
- **Test Design Techniques:** Boundary Value Analysis, Equivalence Partitioning, Parametrized Testing
- **FanCode Business Logic:** City coordinate validation, Todo completion thresholds, API integration
- **Error Scenarios:** Network failures, Invalid data, Edge cases

---

## 🚨 Error Handling

- Network/API errors
- Data validation
- Empty results

---

## 🔄 CI/CD Integration

**GitHub Actions:**
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

**Jenkins:**
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

---

## 🐳 Running with Docker

To build and run tests in Docker:

```bash
docker build -t fancode-sdet .
```

**On Windows (cmd):**
```bat
REM Recommended: Use absolute path and quotes if your path has spaces
docker run --rm -v "C:/Users/91704/Downloads/FanCode SDET Assignment/FanCode City/reports:/app/reports" fancode-sdet
```
(Make sure your image name is all lowercase, e.g., `fancode-sdet`)

If you see `invalid reference format`, ensure you build the image with a lowercase name:
```bat
docker build -t fancode-sdet .
```

Then run:
```bat
docker run --rm -v "C:/Users/91704/Downloads/FanCode SDET Assignment/FanCode City/reports:/app/reports" fancode-sdet
```


**On Linux/macOS:**
```sh
docker run --rm -v "$(pwd)/reports:/app/reports" fancode-sdet
```

---

## 🐛 Troubleshooting

- Check connectivity, permissions, Python/pip versions.
- Review HTML report and logs in `reports/`.

---

## 🤝 Contributing

1. Fork, branch, add tests, PR.

---

## 📝 License

Educational use for FanCode SDET Assignment.

---

## 📞 Support

- See troubleshooting, reports, and logs for help.

---

**Note:** This framework is designed to be production-ready with robust error handling, logging, and reporting. It demonstrates best practices in test automation, including clear project structure, configuration management, and comprehensive test coverage.