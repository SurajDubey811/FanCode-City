# Utility functions for FanCode SDET Assignment

import re

def is_email_valid(email: str) -> bool:
    """Simple email validation."""
    # More comprehensive email validation
    pattern = r"^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?$"
    return bool(re.match(pattern, email))

def safe_get(dct, keys):
    """Safely get a nested value from a dict."""
    for key in keys:
        if isinstance(dct, dict) and key in dct:
            dct = dct[key]
        else:
            return None
    return dct

def is_in_fancode_city(lat, lng, lat_min=-40, lat_max=5, lng_min=5, lng_max=100):
    """Check if coordinates are within FanCode City bounds."""
    return lat_min <= lat <= lat_max and lng_min <= lng <= lng_max

def calculate_todo_completion(todos):
    """Calculate completion percentage for a list of todos."""
    if not todos:
        return 0.0
    completed = sum(1 for todo in todos if getattr(todo, 'completed', False))
    return (completed / len(todos)) * 100
