# Allure Reporting Setup for FanCode SDET Assignment

## Overview

This project now uses Allure reporting instead of pytest-html for comprehensive test reporting. Allure provides rich visualizations, test history, and detailed test analytics.

## Prerequisites

### 1. Install Allure CLI

**Windows (using npm):**
```cmd
npm install -g allure-commandline
```

**Windows (using Chocolatey):**
```cmd
choco install allure
```

**Linux/macOS (using npm):**
```bash
npm install -g allure-commandline
```

**Linux (using apt):**
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

**macOS (using Homebrew):**
```bash
brew install allure
```

### 2. Python Dependencies

The required Python packages are automatically installed when running the test scripts:
- `allure-pytest==2.13.2`

## Running Tests with Allure

### Using Test Scripts

**Windows:**
```cmd
run_tests.bat
```

**Linux/macOS:**
```bash
./run_tests.sh
```

### Manual Execution

```bash
# Run tests and generate Allure results
pytest tests/ --alluredir=reports/allure-results

# Generate HTML report
allure generate reports/allure-results -o reports/allure-report --clean

# Serve report with built-in server
allure serve reports/allure-results
```

## Report Features

### Test Organization
- **Epics**: High-level test groupings (e.g., "FanCode SDET Assignment")
- **Features**: Test feature areas (e.g., "User Todo Completion Validation")
- **Stories**: Specific test scenarios (e.g., "API Connectivity", "Todo Completion Calculation")

### Test Metadata
- **Severity Levels**: BLOCKER, CRITICAL, NORMAL, MINOR
- **Tags**: Based on pytest markers (fancode, api, performance, etc.)
- **Steps**: Detailed test execution steps with attachments
- **Environment Info**: Test execution environment details

### Report Sections

1. **Overview**: Test execution summary with statistics
2. **Categories**: Failed tests grouped by failure types
3. **Suites**: Tests organized by test classes/files
4. **Graphs**: Visual representations of test results
5. **Timeline**: Test execution timeline
6. **Behaviors**: Tests organized by BDD features/stories
7. **Packages**: Test results by Python packages

## Viewing Reports

### Option 1: Open Static HTML Report
Navigate to `reports/allure-report/index.html` in your browser.

### Option 2: Use Allure Server
```bash
allure serve reports/allure-results
```
This starts a local server and opens the report in your browser automatically.

## Allure Annotations in Tests

The tests use various Allure decorators for better reporting:

```python
import allure

@allure.epic("FanCode SDET Assignment")
@allure.feature("User Todo Completion Validation")
class TestFanCodeUserTodoCompletion:
    
    @allure.story("API Connectivity")
    @allure.title("Verify API endpoints are accessible")
    @allure.description("Test API connectivity and data retrieval")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_api_connectivity(self):
        with allure.step("Fetch users from API"):
            users = api_client.get_users()
            allure.attach(f"Users count: {len(users)}", "API Response", allure.attachment_type.TEXT)
```

## Report Locations

- **Raw Results**: `reports/allure-results/` (JSON data files)
- **HTML Report**: `reports/allure-report/` (Generated HTML report)
- **Environment**: Auto-configured with test execution details

## Troubleshooting

### Allure CLI Not Found
If you see "Allure CLI not found" warnings:
1. Install Allure CLI using one of the methods above
2. Ensure `allure` command is available in your PATH
3. Restart your terminal/command prompt

### Empty Reports
If reports appear empty:
1. Ensure tests are running with `--alluredir` parameter
2. Check that `reports/allure-results/` contains JSON files
3. Verify Allure CLI installation

### Permission Issues
On Linux/macOS, you might need to make the script executable:
```bash
chmod +x run_tests.sh
```

## Migration from pytest-html

The following changes were made:
1. Replaced `pytest-html` with `allure-pytest` in requirements.txt
2. Updated `pytest.ini` to use `--alluredir` instead of `--html`
3. Modified test execution scripts to generate Allure reports
4. Added Allure decorators to test methods for enhanced reporting
5. Added environment configuration in `conftest.py`
