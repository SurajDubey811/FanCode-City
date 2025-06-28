@echo off
REM FanCode SDET Assignment - Test Execution Script (Windows)
REM This script sets up the environment and runs the test suite

echo ==========================================
echo FanCode SDET Assignment - Test Execution
echo ==========================================

REM Check for Python
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python to continue.
    exit /b 1
)
python --version

REM Check for pip
where pip >nul 2>nul
if errorlevel 1 (
    echo [ERROR] pip is not installed. Please install pip to continue.
    exit /b 1
)
pip --version

REM Upgrade pip
echo [INFO] Upgrading pip...
pip install --upgrade pip

REM Install dependencies
echo [INFO] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    exit /b 1
)
echo [SUCCESS] Dependencies installed successfully

REM Create reports directory
if not exist reports (
    mkdir reports
)

REM Set environment variable for PYTHONPATH
set PYTHONPATH=%CD%;%PYTHONPATH%

REM Parse command line arguments
set RUN_MODE=all
set GENERATE_REPORT=true
set PARALLEL=false

:parse_args
if "%1"=="" goto after_args
if "%1"=="--smoke" (
    set RUN_MODE=smoke
    shift
    goto parse_args
)
if "%1"=="--regression" (
    set RUN_MODE=regression
    shift
    goto parse_args
)
if "%1"=="--no-report" (
    set GENERATE_REPORT=false
    shift
    goto parse_args
)
if "%1"=="--parallel" (
    set PARALLEL=true
    shift
    goto parse_args
)
if "%1"=="--help" (
    echo Usage: %0 [OPTIONS]
    echo Options:
    echo   --smoke       Run only smoke tests
    echo   --regression  Run only regression tests
    echo   --no-report   Skip HTML report generation
    echo   --parallel    Run tests in parallel
    echo   --help        Show this help message
    exit /b 0
)
echo [WARNING] Unknown option: %1
shift
goto parse_args

:after_args

REM Build pytest command
set PYTEST_CMD=pytest -v

REM Add markers based on run mode
if "%RUN_MODE%"=="smoke" (
    set PYTEST_CMD=%PYTEST_CMD% -m smoke
    echo [INFO] Running smoke tests only
) else if "%RUN_MODE%"=="regression" (
    set PYTEST_CMD=%PYTEST_CMD% -m regression
    echo [INFO] Running regression tests only
) else (
    echo [INFO] Running all tests
)

REM Add parallel execution if requested
if "%PARALLEL%"=="true" (
    set PYTEST_CMD=%PYTEST_CMD% -n auto
    echo [INFO] Parallel execution enabled
)

REM Add report generation
if "%GENERATE_REPORT%"=="true" (
    set PYTEST_CMD=%PYTEST_CMD% --alluredir=reports/allure-results --clean-alluredir
    echo [INFO] Allure report generation enabled
)

REM Run the tests
echo [INFO] Starting test execution...
echo Command: %PYTEST_CMD%
echo ==========================================

%PYTEST_CMD%
if errorlevel 1 (
    echo [ERROR] Some tests failed. Check the reports for details.
    if "%GENERATE_REPORT%"=="true" (
        echo [INFO] Generating Allure report...
        allure generate reports/allure-results -o reports/allure-report --clean
        if not errorlevel 1 (
            echo [INFO] Allure report generated: %CD%\reports\allure-report\index.html
            echo [INFO] To serve the report, run: allure serve reports/allure-results
        ) else (
            echo [WARNING] Failed to generate Allure report. Make sure Allure CLI is installed.
            echo [INFO] Raw test results available in: %CD%\reports\allure-results
        )
    )
    exit /b 1
) else (
    echo [SUCCESS] All tests completed successfully!
    if "%GENERATE_REPORT%"=="true" (
        echo [INFO] Generating Allure report...
        allure generate reports/allure-results -o reports/allure-report --clean
        if not errorlevel 1 (
            echo [INFO] Allure report generated: %CD%\reports\allure-report\index.html
            echo [INFO] To view the report, open: %CD%\reports\allure-report\index.html
            echo [INFO] To serve the report, run: allure serve reports/allure-results
        ) else (
            echo [WARNING] Failed to generate Allure report. Make sure Allure CLI is installed.
            echo [INFO] Raw test results available in: %CD%\reports\allure-results
        )
    )
    for %%f in (reports\test_log_*.log) do (
        if exist "%%f" (
            echo [INFO] Log files available in reports\ directory
            goto breaklog
        )
    )
    :breaklog
    echo ==========================================
    echo [SUCCESS] Test execution completed successfully!
)

REM Deactivate virtual environment
deactivate
