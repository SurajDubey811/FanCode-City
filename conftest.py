"""
Pytest configuration and shared fixtures for FanCode SDET Assignment
"""

import pytest
import allure
import os
from datetime import datetime


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Configure Allure environment"""
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    # Set environment information for Allure
    allure_results_dir = config.getoption('--alluredir')
    if allure_results_dir:
        environment_properties = {
            'Test.Environment': 'FanCode SDET Assignment',
            'Test.Execution.Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'API.Base.URL': 'https://jsonplaceholder.typicode.com',
            'Python.Version': f"{pytest.__version__}",
        }
        
        env_file_path = os.path.join(allure_results_dir, 'environment.properties')
        os.makedirs(allure_results_dir, exist_ok=True)
        
        with open(env_file_path, 'w') as env_file:
            for key, value in environment_properties.items():
                env_file.write(f"{key}={value}\n")


@pytest.fixture(autouse=True)
def test_setup(request):
    """Auto-setup for all tests with Allure metadata"""
    test_name = request.node.name
    test_class = request.node.cls.__name__ if request.node.cls else "N/A"
    
    # Add test metadata to Allure
    allure.dynamic.title(test_name)
    if hasattr(request.node, 'function'):
        docstring = request.node.function.__doc__
        if docstring:
            allure.dynamic.description(docstring.strip())
    
    # Auto-tag based on markers
    markers = [mark.name for mark in request.node.iter_markers()]
    for marker in markers:
        if marker in ['fancode', 'api', 'performance', 'smoke', 'regression']:
            allure.dynamic.tag(marker)
    
    # Set severity based on markers
    if 'smoke' in markers:
        allure.dynamic.severity(allure.severity_level.BLOCKER)
    elif 'regression' in markers:
        allure.dynamic.severity(allure.severity_level.CRITICAL)
    elif 'api' in markers:
        allure.dynamic.severity(allure.severity_level.NORMAL)
    else:
        allure.dynamic.severity(allure.severity_level.MINOR)


# Place any custom fixtures or hooks here as needed.
