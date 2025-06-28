"""
Data Models step definitions
"""
import pytest
from pytest_bdd import given, when, then, parsers
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from user import User
from todo import Todo

# User model steps
@when("I create a User object from the API data")
def create_user_from_api_data(context):
    """Create User object from API data"""
    context['user_object'] = User.from_dict(context['user_api_data'])

@when("I create a Todo object from the API data")
def create_todo_from_api_data(context):
    """Create Todo object from API data"""
    context['todo_object'] = Todo.from_dict(context['todo_api_data'])

@then("the User object should have all required fields")
def verify_user_required_fields(context):
    """Verify User object has all required fields"""
    user = context['user_object']
    required_fields = ['id', 'name', 'username', 'email', 'address', 'lat', 'lng']
    
    for field in required_fields:
        assert hasattr(user, field), f"User object missing field: {field}"
        assert getattr(user, field) is not None, f"User field {field} should not be None"

@then("the Todo object should have all required fields")
def verify_todo_required_fields(context):
    """Verify Todo object has all required fields"""
    todo = context['todo_object']
    required_fields = ['id', 'user_id', 'title', 'completed']
    
    for field in required_fields:
        assert hasattr(todo, field), f"Todo object missing field: {field}"
        assert getattr(todo, field) is not None, f"Todo field {field} should not be None"

@then("the coordinates should be properly extracted from the address")
def verify_coordinates_extraction(context):
    """Verify coordinates are properly extracted"""
    user = context['user_object']
    expected_lat = float(context['user_api_data']['address']['geo']['lat'])
    expected_lng = float(context['user_api_data']['address']['geo']['lng'])
    
    assert user.lat == expected_lat, f"Expected lat {expected_lat}, got {user.lat}"
    assert user.lng == expected_lng, f"Expected lng {expected_lng}, got {user.lng}"

@then("the completion status should be a boolean value")
def verify_completion_boolean(context):
    """Verify completion status is boolean"""
    todo = context['todo_object']
    assert isinstance(todo.completed, bool), f"Completion should be boolean, got {type(todo.completed)}"

# Coordinate variation steps
@given(parsers.parse("I have user data with latitude {lat:f} and longitude {lng:f}"))
def have_user_data_with_coordinates(lat, lng, context):
    """Create user data with specific coordinates"""
    context['user_api_data'] = {
        'id': 1,
        'name': 'Test User',
        'username': 'testuser',
        'email': 'test@example.com',
        'address': {
            'street': 'Test Street',
            'suite': 'Apt 1',
            'city': 'TestCity',
            'zipcode': '12345',
            'geo': {
                'lat': str(lat),
                'lng': str(lng)
            }
        }
    }

@when("I create a User object from this data")
def create_user_from_coordinate_data(context):
    """Create User object from coordinate data"""
    context['user_object'] = User.from_dict(context['user_api_data'])

@then(parsers.parse("the User object should have latitude {lat:f}"))
def verify_user_latitude(lat, context):
    """Verify User object has correct latitude"""
    user = context['user_object']
    assert user.lat == lat, f"Expected latitude {lat}, got {user.lat}"

@then(parsers.parse("the User object should have longitude {lng:f}"))
def verify_user_longitude(lng, context):
    """Verify User object has correct longitude"""
    user = context['user_object']
    assert user.lng == lng, f"Expected longitude {lng}, got {user.lng}"

# String representation steps
@given(parsers.parse("I have a User object with name \"{name}\""))
def have_user_with_name(name, context):
    """Create User object with specific name"""
    context['user_object'] = User(
        id=1,
        name=name,
        username='testuser',
        email='test@example.com',
        address={'geo': {'lat': '0.0', 'lng': '0.0'}},
        lat=0.0,
        lng=0.0
    )

@given(parsers.parse("I have a Todo object with title \"{title}\""))
def have_todo_with_title(title, context):
    """Create Todo object with specific title"""
    context['todo_object'] = Todo(
        id=1,
        user_id=1,
        title=title,
        completed=True
    )

@when("I convert the User to string")
def convert_user_to_string(context):
    """Convert User object to string"""
    context['user_string'] = str(context['user_object'])

@when("I convert the Todo to string")
def convert_todo_to_string(context):
    """Convert Todo object to string"""
    context['todo_string'] = str(context['todo_object'])

@then("the string should contain the user's name")
def verify_string_contains_user_name(context):
    """Verify string representation contains user name"""
    user_string = context['user_string']
    user_name = context['user_object'].name
    assert user_name in user_string, f"User string '{user_string}' should contain name '{user_name}'"

@then("the string should contain the todo's title")
def verify_string_contains_todo_title(context):
    """Verify string representation contains todo title"""
    todo_string = context['todo_string']
    todo_title = context['todo_object'].title
    assert todo_title in todo_string, f"Todo string '{todo_string}' should contain title '{todo_title}'"

@then("the string should be human-readable")
def verify_string_human_readable(context):
    """Verify string representation is human-readable"""
    user_string = context['user_string']
    # Basic checks for human readability
    assert len(user_string) > 0, "String should not be empty"
    assert not user_string.startswith('<'), "String should not be a raw object representation"

@then("the string should indicate completion status")
def verify_string_indicates_completion(context):
    """Verify string representation indicates completion status"""
    todo_string = context['todo_string']
    completion_status = context['todo_object'].completed
    
    # Check that completion status is somehow indicated in the string
    if completion_status:
        # Should indicate completion (True, completed, done, etc.)
        completion_indicators = ['true', 'completed', 'done', 'finished']
    else:
        # Should indicate incompletion (False, not completed, pending, etc.)
        completion_indicators = ['false', 'not completed', 'pending', 'incomplete']
    
    string_lower = todo_string.lower()
    has_indicator = any(indicator in string_lower for indicator in completion_indicators)
    assert has_indicator, f"Todo string '{todo_string}' should indicate completion status {completion_status}"
