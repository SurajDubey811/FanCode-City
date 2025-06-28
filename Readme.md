
# FanCode SDET Assignment

---

## 📚 Table of Contents

- [Overview](#overview)
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
├── reports/
│   ├── report.html
│   ├── report.json
│   └── test_log_*.log
└── tests/
    └── test_fancode_users.py
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

- **APIClient:** Handles API interactions and error handling.
- **User & Todo Data Classes:** Typed models for API data.
- **FanCodeCityValidator:** Core business logic and validation.
- **Test Class:** Comprehensive test coverage and reporting.

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

## 🧪 Test Cases

- API connectivity
- FanCode city identification
- Todo completion calculation
- Main validation (per-user and overall)

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