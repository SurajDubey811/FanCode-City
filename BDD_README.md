# FanCode SDET Assignment - BDD Framework

## 🎯 Overview

This project has been enhanced with **Behavior-Driven Development (BDD)** capabilities using **pytest-bdd**. The BDD framework allows writing tests in natural language (Gherkin syntax) that can be easily understood by both technical and non-technical stakeholders.

## 🏗️ BDD Framework Structure

```
FanCode City/
├── features/                          # BDD Feature files (Gherkin)
│   ├── fancode_users_todo_completion.feature
│   ├── api_client.feature
│   ├── data_models.feature
│   ├── utility_functions.feature
│   ├── conftest.py                    # BDD fixtures and configuration
│   └── step_definitions/              # Step definitions (Python)
│       ├── common_steps.py
│       ├── fancode_steps.py
│       ├── api_client_steps.py
│       ├── data_model_steps.py
│       └── utility_steps.py
├── tests/
│   ├── test_bdd_fancode_main.py       # Main BDD test runner
│   ├── test_bdd_api_client.py         # API client BDD tests
│   ├── test_bdd_data_models.py        # Data model BDD tests
│   ├── test_bdd_utilities.py          # Utility BDD tests
│   └── ... (traditional tests)
├── run_tests_bdd.bat                  # Enhanced test runner with BDD support
└── ...
```

## 🚀 Running BDD Tests

### Prerequisites
- Python 3.7+
- All dependencies from `requirements.txt` (automatically installed)

### Quick Start

**Run all tests (BDD + Traditional):**
```bat
run_tests_bdd.bat
```

**Run only BDD tests:**
```bat
run_tests_bdd.bat --bdd
```

**Run only traditional tests:**
```bat
run_tests_bdd.bat --traditional
```

**Run BDD tests with specific markers:**
```bat
run_tests_bdd.bat --bdd --smoke
run_tests_bdd.bat --bdd --regression
```

**Run tests in parallel:**
```bat
run_tests_bdd.bat --parallel
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--bdd` | Run only BDD tests |
| `--traditional` | Run only traditional pytest tests |
| `--smoke` | Run only smoke tests |
| `--regression` | Run only regression tests |
| `--parallel` | Run tests in parallel |
| `--no-report` | Skip HTML report generation |
| `--help` | Show help message |

## 📝 BDD Features Overview

### 1. FanCode Users Todo Completion (`fancode_users_todo_completion.feature`)

**Main Scenario:**
```gherkin
Scenario: All FanCode city users should have more than 50% todo completion rate
  Given I have access to the user and todo data from the API
  When I identify all users belonging to FanCode city
  And I calculate the todo completion percentage for each FanCode user
  Then all FanCode city users should have more than 50% of their todos completed
```

**Key Test Cases:**
- ✅ Main business logic validation
- ✅ FanCode city user identification
- ✅ Todo completion calculation accuracy
- ✅ Boundary conditions testing
- ✅ Edge cases (users with no todos)
- ✅ Performance validation
- ✅ Error handling

### 2. API Client Functionality (`api_client.feature`)

**Key Test Cases:**
- ✅ Fetch users and todos from API
- ✅ Validate response structure
- ✅ Handle invalid requests
- ✅ Performance testing
- ✅ Error handling

### 3. Data Models (`data_models.feature`)

**Key Test Cases:**
- ✅ User and Todo model creation
- ✅ Field validation
- ✅ Coordinate extraction
- ✅ String representations

### 4. Utility Functions (`utility_functions.feature`)

**Key Test Cases:**
- ✅ Email validation
- ✅ Coordinate validation
- ✅ Todo completion calculations
- ✅ Custom bounds testing

## 🎨 BDD Test Examples

### Example 1: Parameterized Business Logic Testing
```gherkin
Scenario Outline: FanCode user todo completion validation with different completion rates
  Given a FanCode city user has <total_todos> todos
  And <completed_todos> of them are completed
  When I calculate the completion percentage
  Then the completion percentage should be <expected_percentage>
  And the user should <result> the FanCode completion criteria

  Examples:
    | total_todos | completed_todos | expected_percentage | result |
    | 10          | 6              | 60.0               | pass   |
    | 10          | 5              | 50.0               | fail   |
    | 20          | 11             | 55.0               | pass   |
```

### Example 2: Boundary Conditions Testing
```gherkin
Scenario Outline: Validate FanCode city boundary conditions
  Given a user has coordinates latitude <lat> and longitude <lng>
  When I check if the user belongs to FanCode city
  Then the user should be <result> as a FanCode city user

  Examples:
    | lat  | lng | result     |
    | -40  | 5   | identified |
    | -40.1| 50  | not identified |
    | 5.1  | 50  | not identified |
```

## 🔧 BDD Framework Components

### Step Definitions

**Common Steps (`common_steps.py`):**
- API connectivity verification
- Background setup
- Shared fixtures

**FanCode Steps (`fancode_steps.py`):**
- FanCode user identification
- Todo completion calculations
- Business logic validation

**API Client Steps (`api_client_steps.py`):**
- API response validation
- Performance testing
- Error handling

**Data Model Steps (`data_model_steps.py`):**
- Model creation and validation
- Field verification

**Utility Steps (`utility_steps.py`):**
- Utility function testing
- Calculation verification

### Features

Each `.feature` file contains scenarios written in Gherkin syntax that describe the expected behavior of the system from a business perspective.

## 📊 Reporting

BDD tests generate enhanced reports that include:
- ✅ Scenario execution results
- ✅ Step-by-step execution details
- ✅ Gherkin-style readable output
- ✅ Traditional pytest HTML reports
- ✅ JSON reports for CI/CD integration

## 🏷️ BDD Markers

BDD tests use the same marker system as traditional tests:

```bash
@smoke      # Quick validation tests
@regression # Full test suite
@api        # API-specific tests  
@fancode    # FanCode business logic
@performance # Performance tests
@boundary   # Boundary condition tests
@edge_cases # Edge case scenarios
@bdd        # All BDD tests (auto-applied)
```

## 🎯 Benefits of BDD Approach

### For Stakeholders:
- **Readable**: Tests written in plain English
- **Collaborative**: Business analysts can understand and contribute
- **Documentation**: Features serve as living documentation
- **Traceability**: Clear mapping from requirements to tests

### For Developers:
- **Reusable**: Step definitions can be reused across scenarios
- **Maintainable**: Separation of test logic and test data
- **Comprehensive**: Covers business scenarios, edge cases, and technical aspects
- **CI/CD Ready**: Integrates seamlessly with existing pytest infrastructure

## 🚦 Test Execution Examples

### Basic Execution
```bat
# Run all BDD tests
run_tests_bdd.bat --bdd

# Run only smoke BDD tests
run_tests_bdd.bat --bdd --smoke

# Run with parallel execution
run_tests_bdd.bat --bdd --parallel
```

### Specific Feature Testing
```bat
# Run specific BDD test file
python -m pytest tests/test_bdd_fancode_main.py -v

# Run all BDD tests using marker
python -m pytest -m bdd -v

# Run all BDD tests by pattern (Windows-compatible)
python -m pytest tests/ -k "test_bdd" -v

# Run with multiple markers
python -m pytest -m "fancode and smoke" -v

# Run specific BDD test files explicitly
python -m pytest tests/test_bdd_fancode_main.py tests/test_bdd_api_client.py -v
```

## 🔄 Migration from Traditional Tests

The BDD framework **complements** the existing traditional tests:

- **Traditional tests** remain for unit testing and detailed technical validation
- **BDD tests** focus on business scenarios and user behavior
- **Both approaches** can be run together or separately
- **Shared utilities** and fixtures are used by both test types

## 🐛 BDD Troubleshooting

### Common Issues and Solutions

#### Issue: `ERROR: file or directory not found: tests/test_bdd_*.py`
**Solution**: Use alternative commands for Windows compatibility:
```bat
# Instead of wildcards, use:
python -m pytest tests/ -k "test_bdd" -v
# Or run with BDD marker:
python -m pytest -m bdd -v
# Or list files explicitly:
python -m pytest tests/test_bdd_fancode_main.py tests/test_bdd_api_client.py -v
```

#### Issue: `StepDefinitionNotFoundError`
**Solution**: Ensure step definitions are properly imported:
1. Check that step definition files exist in `features/step_definitions/`
2. Verify imports in test files include all needed step modules
3. Run only working BDD tests first:
   ```bat
   python -m pytest tests/test_bdd_fancode_main.py::test_all_fancode_city_users_should_have_more_than_50_todo_completion_rate -v
   ```

#### Issue: Collection errors
**Solution**: Run tests individually to isolate issues:
```bat
# Test each BDD file separately
python -m pytest tests/test_bdd_fancode_main.py -v
python -m pytest tests/test_bdd_api_client.py -v
python -m pytest tests/test_bdd_data_models.py -v
```

### Working BDD Commands (Verified)

```bat
# ✅ Main business logic test (WORKS)
python -m pytest tests/test_bdd_fancode_main.py::test_all_fancode_city_users_should_have_more_than_50_todo_completion_rate -v

# ✅ User identification test (WORKS)
python -m pytest tests/test_bdd_fancode_main.py::test_validate_fancode_city_user_identification -v

# ✅ Parameterized completion tests (WORKS)
python -m pytest tests/test_bdd_fancode_main.py -k "completion_validation_with_different_completion_rates" -v

# ✅ All fancode BDD tests (WORKS)
python -m pytest tests/test_bdd_fancode_main.py -v
```

## 🎉 Getting Started with BDD

1. **Run the enhanced test suite:**
   ```bat
   run_tests_bdd.bat
   ```

2. **Quick BDD examples (Windows-compatible):**
   ```bat
   # Use the helper script for common scenarios
   run_bdd_examples.bat main      # Main business logic test
   run_bdd_examples.bat working   # Verified working tests
   run_bdd_examples.bat param     # Parameterized tests
   run_bdd_examples.bat all       # All BDD tests
   ```

3. **Explore the feature files** in the `features/` directory to understand the business scenarios

4. **Check the generated reports** in the `reports/` directory

5. **Modify scenarios** in `.feature` files to add new test cases

6. **Add step definitions** in the `step_definitions/` directory for new functionality

### ✅ Verified Working Commands

```bat
# ✅ Main business test (100% working)
python -m pytest tests/test_bdd_fancode_main.py::test_all_fancode_city_users_should_have_more_than_50_todo_completion_rate -v

# ✅ User identification (100% working)  
python -m pytest tests/test_bdd_fancode_main.py::test_validate_fancode_city_user_identification -v

# ✅ Parameterized tests (5 scenarios, 100% working)
python -m pytest tests/test_bdd_fancode_main.py -k "completion_validation_with_different_completion_rates" -v
```

This BDD framework ensures comprehensive validation of the FanCode business requirements while maintaining readability and collaboration between technical and business teams.
