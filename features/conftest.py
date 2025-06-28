"""
BDD Test Configuration and Shared Fixtures
"""
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api_client import APIClient
from validator import FanCodeCityValidator

# Shared context fixture for BDD tests
@pytest.fixture
def context():
    """Shared context for storing test data across BDD steps"""
    return {}

# API client fixture for BDD tests  
@pytest.fixture(scope="session")
def api_client():
    """Session-scoped API client fixture for BDD tests"""
    return APIClient()

# Validator fixture for BDD tests
@pytest.fixture(scope="session") 
def validator(api_client):
    """Session-scoped validator fixture for BDD tests"""
    return FanCodeCityValidator(api_client)

# Hook to add BDD markers automatically
def pytest_collection_modifyitems(config, items):
    """Add bdd marker to all BDD test items"""
    for item in items:
        if "test_bdd_" in item.nodeid:
            item.add_marker(pytest.mark.bdd)

# Configure BDD test reporting
def pytest_configure(config):
    """Configure BDD-specific settings"""
    # Register BDD marker
    config.addinivalue_line(
        "markers", "bdd: Behavior-driven development tests"
    )
