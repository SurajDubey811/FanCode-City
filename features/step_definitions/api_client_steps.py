"""
API Client step definitions
"""
import pytest
from pytest_bdd import given, when, then, parsers
import time
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from api_client import APIClient

# API fetch steps
@when("I fetch all users from the API")
def fetch_all_users(context):
    """Fetch all users from API"""
    start_time = time.time()
    context['users'] = context['api_client'].get_users()
    context['users_fetch_time'] = time.time() - start_time

@when("I fetch all todos from the API")
def fetch_all_todos(context):
    """Fetch all todos from API"""
    start_time = time.time()
    context['todos'] = context['api_client'].get_todos()
    context['todos_fetch_time'] = time.time() - start_time

@when("I fetch todos for that specific user")
def fetch_user_todos(context):
    """Fetch todos for specific user"""
    user_id = context['valid_user_id']
    context['user_todos'] = context['api_client'].get_user_todos(user_id)

@when("I fetch todos for a non-existent user ID")
def fetch_nonexistent_user_todos(context):
    """Fetch todos for non-existent user"""
    non_existent_id = 99999
    context['nonexistent_user_todos'] = context['api_client'].get_user_todos(non_existent_id)

# Response validation steps
@then("I should receive a list of users")
def verify_users_list(context):
    """Verify users response is a list"""
    assert isinstance(context['users'], list), "Users response should be a list"

@then("I should receive a list of todos")
def verify_todos_list(context):
    """Verify todos response is a list"""
    assert isinstance(context['todos'], list), "Todos response should be a list"

@then(parsers.parse("the list should contain exactly {count:d} users"))
def verify_users_count(count, context):
    """Verify exact number of users"""
    actual_count = len(context['users'])
    assert actual_count == count, f"Expected {count} users, got {actual_count}"

@then(parsers.parse("the list should contain exactly {count:d} todos"))
def verify_todos_count(count, context):
    """Verify exact number of todos"""
    actual_count = len(context['todos'])
    assert actual_count == count, f"Expected {count} todos, got {actual_count}"

@then("each user should have required fields for FanCode validation")
def verify_user_fields(context):
    """Verify users have required fields"""
    if not context['users']:
        pytest.skip("No users to validate")
    
    user = context['users'][0]
    required_fields = ['id', 'name', 'email', 'lat', 'lng']
    
    for field in required_fields:
        assert hasattr(user, field), f"User missing required field: {field}"
    
    # Verify coordinate types
    assert isinstance(user.lat, (int, float)), "Latitude should be numeric"
    assert isinstance(user.lng, (int, float)), "Longitude should be numeric"

@then("each todo should have required fields for completion calculation")
def verify_todo_fields(context):
    """Verify todos have required fields"""
    if not context['todos']:
        pytest.skip("No todos to validate")
    
    todo = context['todos'][0]
    required_fields = ['id', 'user_id', 'completed']
    
    for field in required_fields:
        assert hasattr(todo, field), f"Todo missing required field: {field}"
    
    # Verify completion type
    assert isinstance(todo.completed, bool), "Completed field should be boolean"

@then("I should receive only todos belonging to that user")
def verify_user_todos_ownership(context):
    """Verify todos belong to correct user"""
    user_id = context['valid_user_id']
    for todo in context['user_todos']:
        assert todo.user_id == user_id, f"Todo {todo.id} belongs to user {todo.user_id}, expected {user_id}"

@then("all returned todos should have the correct user ID")
def verify_correct_user_id(context):
    """Verify all todos have correct user ID"""
    user_id = context['valid_user_id']
    for todo in context['user_todos']:
        assert todo.user_id == user_id, f"Todo has user_id {todo.user_id}, expected {user_id}"

@then("I should receive an empty list")
def verify_empty_list(context):
    """Verify response is empty list"""
    assert context['nonexistent_user_todos'] == [], "Should receive empty list for non-existent user"

@then("no errors should be thrown")
def verify_no_errors(context):
    """Verify no errors were thrown"""
    # If we reach this step, no errors were thrown during the API call
    assert True

# Performance validation steps
@when("I measure the response time for fetching users")
def measure_users_response_time(context):
    """Measure users API response time"""
    start_time = time.time()
    context['users'] = context['api_client'].get_users()
    context['users_response_time'] = time.time() - start_time

@when("I measure the response time for fetching todos")
def measure_todos_response_time(context):
    """Measure todos API response time"""
    start_time = time.time()
    context['todos'] = context['api_client'].get_todos()
    context['todos_response_time'] = time.time() - start_time

@then(parsers.parse("the response time should be less than {max_seconds:d} seconds"))
def verify_response_time(max_seconds, context):
    """Verify response time is within limit"""
    # Check the most recent response time measurement
    if 'users_response_time' in context:
        actual_time = context['users_response_time']
        assert actual_time < max_seconds, f"Users API response time {actual_time:.2f}s exceeds {max_seconds}s limit"
    elif 'todos_response_time' in context:
        actual_time = context['todos_response_time']
        assert actual_time < max_seconds, f"Todos API response time {actual_time:.2f}s exceeds {max_seconds}s limit"
    else:
        pytest.fail("No response time measurement found")

@then(parsers.parse("the API calls should complete within {max_seconds:d} seconds each"))
def verify_api_call_times(max_seconds, context):
    """Verify all API calls complete within time limit"""
    if 'users_fetch_time' in context:
        assert context['users_fetch_time'] < max_seconds, \
               f"Users fetch took {context['users_fetch_time']:.2f}s, should be < {max_seconds}s"
    
    if 'todos_fetch_time' in context:
        assert context['todos_fetch_time'] < max_seconds, \
               f"Todos fetch took {context['todos_fetch_time']:.2f}s, should be < {max_seconds}s"
