# Support: a user has coordinates latitude {lat} and longitude {lng}
from pytest_bdd import given, parsers
import pytest
pytestmark = pytest.mark.bdd


def user_has_coordinates_any(lat, lng, context):
    """Store coordinates for user (alternate wording, for boundary tests)"""
    from user import User
    context['lat'] = float(lat)
    context['lng'] = float(lng)
    # Also create a test_user for compatibility with FanCode steps
    context['test_user'] = User(
        id=999, name="Test User", username="testuser",
        email="test@fancode.com", address={}, lat=float(lat), lng=float(lng)
    )
# Flexible step for all coordinate scenarios (accepts int, float, str)
from pytest_bdd import given, parsers

@given(parsers.parse("I have coordinates latitude {lat} and longitude {lng}"))
def have_coordinates_flexible_any(lat, lng, context):
    """Store coordinates with flexible parsing (catch-all)"""
    context['lat'] = float(lat)
    context['lng'] = float(lng)
"""
Utility Functions step definitions
"""
import pytest
from pytest_bdd import given, when, then, parsers
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import utils
from todo import Todo

# Email validation steps
@given(parsers.parse("I have an email address \"{email}\""))
def have_email_address(email, context):
    """Store email address for validation"""
    context['email'] = email

@when("I validate the email format")
def validate_email_format(context):
    """Validate email format using utility function"""
    context['email_valid'] = utils.is_email_valid(context['email'])

@then(parsers.parse("the validation result should be {expected}"))
def verify_email_validation_result(expected, context):
    """Verify email validation result"""
    expected_bool = expected.lower() == 'true'
    actual = context['email_valid']
    assert actual == expected_bool, f"Expected {expected_bool}, got {actual} for email '{context['email']}'"

# Coordinate validation steps
@given(parsers.parse("I have coordinates latitude {lat:f} and longitude {lng:f}"))
def have_coordinates(lat, lng, context):
    """Store coordinates for validation"""
    context['lat'] = lat
    context['lng'] = lng

@when("I check if the coordinates are within FanCode city bounds")
def check_fancode_bounds(context):
    """Check if coordinates are within FanCode city bounds"""
    context['in_fancode_city'] = utils.is_in_fancode_city(context['lat'], context['lng'])

@then(parsers.parse("the result should be {expected}"))
def verify_coordinate_result(expected, context):
    """Verify coordinate validation result"""
    expected_bool = expected.lower() == 'true'
    actual = context['in_fancode_city']
    assert actual == expected_bool, \
           f"Expected {expected_bool}, got {actual} for coordinates ({context['lat']}, {context['lng']})"


# Todo completion calculation steps
@given(parsers.parse("I have a list of todos with {total:d} items"))
def have_todos_list(total, context):
    """Create a list of todos with specified count"""
    context['test_todos'] = [
        Todo(id=i, user_id=1, title=f"Todo {i}", completed=False)
        for i in range(1, total + 1)
    ]
    # Set default coordinates for robustness
    context['lat'] = 0.0
    context['lng'] = 0.0

@given(parsers.parse("{completed:d} of them are marked as completed"))
def mark_todos_as_completed(completed, context):
    """Mark specified number of todos as completed"""
    for i in range(min(completed, len(context['test_todos']))):
        context['test_todos'][i].completed = True

@given("I have an empty list of todos")
def have_empty_todos_list(context):
    """Create an empty list of todos and set default coordinates for robustness"""
    context['test_todos'] = []
    context['lat'] = 0.0
    context['lng'] = 0.0

@when("I calculate the completion percentage")
def calculate_completion_percentage_util(context):
    """Calculate completion percentage using utility function"""
    context['completion_percentage'] = utils.calculate_todo_completion(context['test_todos'])
    # For robustness, always set these keys so result steps never KeyError
    context['in_fancode_city'] = None
    context['in_custom_bounds'] = None

@then(parsers.parse("the result should be {expected_percentage:f}"))
def verify_completion_percentage_result(expected_percentage, context):
    """Verify completion percentage result"""
    actual = context['completion_percentage']
    # Allow for small floating point differences
    assert abs(actual - expected_percentage) < 0.01, \
           f"Expected {expected_percentage}%, got {actual}%"

@then("the result should be 0.0")
def verify_zero_result(context):
    """Verify result is exactly 0.0"""
    actual = context['completion_percentage']
    assert actual == 0.0, f"Expected 0.0, got {actual}"

# Custom bounds steps
@given(parsers.parse("I define custom coordinate bounds with lat_min {lat_min:d}, lat_max {lat_max:d}, lng_min {lng_min:d}, lng_max {lng_max:d}"))
def define_custom_bounds(lat_min, lat_max, lng_min, lng_max, context):
    """Define custom coordinate bounds"""
    context['custom_bounds'] = {
        'lat_min': lat_min,
        'lat_max': lat_max,
        'lng_min': lng_min,
        'lng_max': lng_max
    }

@when("I check if the coordinates are within the custom bounds")
def check_custom_bounds(context):
    """Check if coordinates are within custom bounds"""
    bounds = context['custom_bounds']
    context['in_custom_bounds'] = utils.is_in_fancode_city(
        context['lat'], 
        context['lng'],
        lat_min=bounds['lat_min'],
        lat_max=bounds['lat_max'],
        lng_min=bounds['lng_min'],
        lng_max=bounds['lng_max']
    )

@then("the result should be true")
def verify_true_result(context):
    """Verify result is true"""
    actual = context.get('in_custom_bounds', context.get('in_fancode_city', None))
    assert actual is True, f"Expected True, got {actual}"

@then("the result should be false")
def verify_false_result(context):
    """Verify result is false"""
    actual = context.get('in_custom_bounds', context.get('in_fancode_city', None))
    assert actual is False, f"Expected False, got {actual}"
# Ensure that when checking bounds, the context is always set for both keys for robustness
@when("I check if the coordinates are within FanCode city bounds")
def check_fancode_bounds(context):
    """Check if coordinates are within FanCode city bounds"""
    result = utils.is_in_fancode_city(context['lat'], context['lng'])
    context['in_fancode_city'] = result
    context['in_custom_bounds'] = result
# Ensure that when checking custom bounds, the context is always set for both keys for robustness
@when("I check if the coordinates are within the custom bounds")
def check_custom_bounds(context):
    """Check if coordinates are within custom bounds"""
    bounds = context['custom_bounds']
    result = utils.is_in_fancode_city(
        context['lat'], 
        context['lng'],
        lat_min=bounds['lat_min'],
        lat_max=bounds['lat_max'],
        lng_min=bounds['lng_min'],
        lng_max=bounds['lng_max']
    )
    context['in_custom_bounds'] = result
    context['in_fancode_city'] = result

# Additional missing step definitions
@given(parsers.parse("I have coordinates latitude {lat:f} and longitude {lng:f}"))
def have_coordinates_alt(lat, lng, context):
    """Alternative coordinates step (duplicate for compatibility)"""
    context['lat'] = lat
    context['lng'] = lng

@given(parsers.parse("I have coordinates latitude {lat:d} and longitude {lng:d}"))
def have_coordinates_int(lat, lng, context):
    """Store integer coordinates for validation"""
    context['lat'] = float(lat)
    context['lng'] = float(lng)

# Handle decimal coordinates specifically
@given(parsers.parse("I have coordinates latitude {lat} and longitude {lng}"))
def have_coordinates_flexible(lat, lng, context):
    """Store coordinates with flexible parsing"""
    context['lat'] = float(lat)
    context['lng'] = float(lng)
