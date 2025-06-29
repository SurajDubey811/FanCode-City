@echo off
REM Enhanced test runner for FanCode SDET Assignment with BDD support
REM Usage: run_tests_bdd.bat [options]

setlocal EnableDelayedExpansion

echo ================================================================
echo                FanCode SDET Assignment - BDD Test Runner
echo ================================================================

REM Parse command line arguments
set "RUN_SMOKE=0"
set "RUN_REGRESSION=0"
set "RUN_BDD=0"
set "RUN_TRADITIONAL=0"
set "SKIP_REPORT=0"
set "PARALLEL=0"
set "SHOW_HELP=0"

:parse_args
if "%~1"=="" goto :args_parsed
if "%~1"=="--smoke" (
    set "RUN_SMOKE=1"
    shift
    goto :parse_args
)
if "%~1"=="--regression" (
    set "RUN_REGRESSION=1"
    shift
    goto :parse_args
)
if "%~1"=="--bdd" (
    set "RUN_BDD=1"
    shift
    goto :parse_args
)
if "%~1"=="--traditional" (
    set "RUN_TRADITIONAL=1"
    shift
    goto :parse_args
)
if "%~1"=="--no-report" (
    set "SKIP_REPORT=1"
    shift
    goto :parse_args
)
if "%~1"=="--parallel" (
    set "PARALLEL=1"
    shift
    goto :parse_args
)
if "%~1"=="--help" (
    set "SHOW_HELP=1"
    shift
    goto :parse_args
)
echo Unknown argument: %~1
shift
goto :parse_args

:args_parsed

if "%SHOW_HELP%"=="1" (
    echo Usage: run_tests_bdd.bat [options]
    echo.
    echo Options:
    echo   --smoke         Run only smoke tests
    echo   --regression    Run only regression tests  
    echo   --bdd           Run only BDD tests
    echo   --traditional   Run only traditional pytest tests
    echo   --no-report     Skip HTML report generation
    echo   --parallel      Run tests in parallel
    echo   --help          Show this help message
    echo.
    echo Examples:
    echo   run_tests_bdd.bat --bdd --smoke
    echo   run_tests_bdd.bat --traditional --regression
    echo   run_tests_bdd.bat --parallel
    echo.
    goto :end
)

REM If no specific test type is selected, run both
if "%RUN_BDD%"=="0" if "%RUN_TRADITIONAL%"=="0" (
    set "RUN_BDD=1"
    set "RUN_TRADITIONAL=1"
)

echo Current directory: %CD%
echo.

REM Install/upgrade dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo Dependencies installed successfully.
echo.

REM Create reports directory
if not exist "reports" mkdir reports

REM Build test command
set "TEST_CMD=python -m pytest"

REM Add parallel option
if "%PARALLEL%"=="1" (
    set "TEST_CMD=!TEST_CMD! -n auto"
)

REM Add marker filters
set "MARKERS="
if "%RUN_SMOKE%"=="1" (
    if "!MARKERS!"=="" (
        set "MARKERS=smoke"
    ) else (
        set "MARKERS=!MARKERS! or smoke"
    )
)
if "%RUN_REGRESSION%"=="1" (
    if "!MARKERS!"=="" (
        set "MARKERS=regression"
    ) else (
        set "MARKERS=!MARKERS! or regression"
    )
)

if not "!MARKERS!"=="" (
    set "TEST_CMD=!TEST_CMD! -m \"!MARKERS!\""
)

REM Add report options
if "%SKIP_REPORT%"=="0" (
    set "TEST_CMD=!TEST_CMD! --html=reports/bdd_report.html --self-contained-html"
)

REM Run BDD tests
if "%RUN_BDD%"=="1" (
    echo ================================================================
    echo                     Running BDD Tests
    echo ================================================================
    
    set "BDD_CMD=!TEST_CMD! -m bdd tests/"
    echo Command: !BDD_CMD!
    echo.
    
    !BDD_CMD!
    set "BDD_EXIT_CODE=!errorlevel!"
    
    if !BDD_EXIT_CODE! equ 0 (
        echo.
        echo ✓ BDD tests completed successfully
    ) else (
        echo.
        echo ✗ BDD tests failed with exit code !BDD_EXIT_CODE!
    )
    echo.
)

REM Run traditional tests
if "%RUN_TRADITIONAL%"=="1" (
    echo ================================================================
    echo                   Running Traditional Tests
    echo ================================================================
    
    set "TRADITIONAL_CMD=!TEST_CMD! -m not\ bdd tests"
    echo Command: !TRADITIONAL_CMD!
    echo.
    
    !TRADITIONAL_CMD!
    set "TRADITIONAL_EXIT_CODE=!errorlevel!"
    
    if !TRADITIONAL_EXIT_CODE! equ 0 (
        echo.
        echo ✓ Traditional tests completed successfully
    ) else (
        echo.
        echo ✗ Traditional tests failed with exit code !TRADITIONAL_EXIT_CODE!
    )
    echo.
)

REM Summary
echo ================================================================
echo                         Test Summary
echo ================================================================

if "%RUN_BDD%"=="1" (
    if defined BDD_EXIT_CODE (
        if !BDD_EXIT_CODE! equ 0 (
            echo BDD Tests: PASSED
        ) else (
            echo BDD Tests: FAILED
        )
    )
)

if "%RUN_TRADITIONAL%"=="1" (
    if defined TRADITIONAL_EXIT_CODE (
        if !TRADITIONAL_EXIT_CODE! equ 0 (
            echo Traditional Tests: PASSED
        ) else (
            echo Traditional Tests: FAILED
        )
    )
)

if "%SKIP_REPORT%"=="0" (
    echo.
    echo Reports generated in the 'reports' directory:
    if exist "reports\bdd_report.html" echo   - BDD Test Report: reports\bdd_report.html
    if exist "reports\report.html" echo   - Traditional Test Report: reports\report.html
)

echo ================================================================

REM Determine overall exit code
set "OVERALL_EXIT_CODE=0"
if defined BDD_EXIT_CODE if !BDD_EXIT_CODE! neq 0 set "OVERALL_EXIT_CODE=!BDD_EXIT_CODE!"
if defined TRADITIONAL_EXIT_CODE if !TRADITIONAL_EXIT_CODE! neq 0 set "OVERALL_EXIT_CODE=!TRADITIONAL_EXIT_CODE!"

:end
exit /b !OVERALL_EXIT_CODE!
