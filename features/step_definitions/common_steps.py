"""
Common step definitions for FanCode BDD tests
"""
import pytest
from pytest_bdd import given, when, then, parsers
import sys
import os
import time
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from api_client import APIClient
from validator import FanCodeCityValidator
from user import User
from todo import Todo
import utils

logger = logging.getLogger(__name__)

# Shared fixtures and context
@pytest.fixture
def context():
    """Shared context for storing test data across steps"""
    return {}

@pytest.fixture
def api_client():
    """API client fixture"""
    return APIClient()

@pytest.fixture
def validator(api_client):
    """Validator fixture"""
    return FanCodeCityValidator(api_client)

# Background steps
@given("the JSONPlaceholder API is accessible")
def api_is_accessible(api_client):
    """Verify API is accessible"""
    try:
        users = api_client.get_users()
        assert len(users) > 0, "API should return users"
    except Exception as e:
        pytest.fail(f"API is not accessible: {e}")

@given(parsers.parse('the JSONPlaceholder API is available at "{url}"'))
def api_is_available_at_url(url):
    """Verify API is available at specific URL"""
    assert url == "http://jsonplaceholder.typicode.com"

@given("the FanCode city coordinates are defined as latitude between -40 and 5 and longitude between 5 and 100")
def fancode_coordinates_defined():
    """Define FanCode city coordinates"""
    # This is just for documentation - the actual bounds are defined in the validator
    pass

# API-related steps
@given("I have an API client instance")
def have_api_client(api_client, context):
    """Store API client in context"""
    context['api_client'] = api_client

@given("I have access to the user and todo data from the API")
def have_access_to_api_data(api_client, context):
    """Fetch and store API data"""
    context['api_client'] = api_client
    context['all_users'] = api_client.get_users()
    context['all_todos'] = api_client.get_todos()

@given("I have access to the user data from the API")
def have_access_to_user_data(api_client, context):
    """Fetch and store user data"""
    context['api_client'] = api_client
    context['all_users'] = api_client.get_users()

@given("I know a valid user ID")
def know_valid_user_id(context):
    """Get a valid user ID from existing users"""
    if 'all_users' not in context:
        context['all_users'] = context['api_client'].get_users()
    context['valid_user_id'] = context['all_users'][0].id if context['all_users'] else 1

# Data creation steps
@given("I have user data from the JSONPlaceholder API")
def have_user_data_from_api(context):
    """Create sample user data matching API format"""
    context['user_api_data'] = {
        'id': 1,
        'name': 'John Doe',
        'username': 'johndoe',
        'email': 'john@example.com',
        'address': {
            'street': 'Test Street',
            'suite': 'Apt 1',
            'city': 'TestCity',
            'zipcode': '12345',
            'geo': {
                'lat': '0.0',
                'lng': '50.0'
            }
        }
    }

@given("I have todo data from the JSONPlaceholder API")
def have_todo_data_from_api(context):
    """Create sample todo data matching API format"""
    context['todo_api_data'] = {
        'userId': 1,
        'id': 1,
        'title': 'Sample todo',
        'completed': True
    }

# Error handling steps
@given("the API is temporarily unavailable")
def api_temporarily_unavailable(context, monkeypatch):
    """Mock API to simulate unavailability"""
    import requests
    
    def mock_get(*args, **kwargs):
        raise requests.RequestException("API temporarily unavailable")
    
    monkeypatch.setattr(requests.Session, 'get', mock_get)
    context['api_unavailable'] = True

# Time measurement helper
def measure_time(func, *args, **kwargs):
    """Measure execution time of a function"""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time
