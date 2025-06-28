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
./run_tests.