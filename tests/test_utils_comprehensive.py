import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import utils
from unittest.mock import Mock


class TestFanCodeUtilities:
    """Test utility functions specific to FanCode context"""
    
    def test_is_in_fancode_city_valid_coordinates(self):
        """Test FanCode city coordinate validation with valid coordinates"""
        # Test coordinates within FanCode city bounds
        valid_coordinates = [
            (-40, 5),      # Exact minimum bounds
            (-40, 100),    # Min lat, max lng
            (5, 5),        # Max lat, min lng  
            (5, 100),      # Exact maximum bounds
            (0, 50),       # Center coordinates
            (-20, 75),     # Random valid coordinates
        ]
        
        for lat, lng in valid_coordinates:
            assert utils.is_in_fancode_city(lat, lng) is True, \
                f"Coordinates ({lat}, {lng}) should be in FanCode city"
    
    def test_is_in_fancode_city_invalid_coordinates(self):
        """Test FanCode city coordinate validation with invalid coordinates"""
        # Test coordinates outside FanCode city bounds
        invalid_coordinates = [
            (-41, 50),     # Below min latitude
            (6, 50),       # Above max latitude
            (0, 4),        # Below min longitude
            (0, 101),      # Above max longitude
            (-50, 150),    # Both coordinates out of bounds
            (10, -10),     # Both coordinates out of bounds
        ]
        
        for lat, lng in invalid_coordinates:
            assert utils.is_in_fancode_city(lat, lng) is False, \
                f"Coordinates ({lat}, {lng}) should NOT be in FanCode city"
    
    def test_is_in_fancode_city_custom_bounds(self):
        """Test FanCode city validation with custom bounds"""
        # Test with custom coordinate bounds
        assert utils.is_in_fancode_city(10, 150, lat_min=0, lat_max=20, lng_min=100, lng_max=200) is True
        assert utils.is_in_fancode_city(10, 150, lat_min=20, lat_max=30, lng_min=100, lng_max=200) is False
    
    def test_calculate_todo_completion_various_scenarios(self):
        """Test todo completion calculation for various FanCode user scenarios"""
        class MockTodo:
            def __init__(self, completed):
                self.completed = completed
        
        # Scenario 1: Perfect completion (100%)
        perfect_todos = [MockTodo(True) for _ in range(5)]
        assert utils.calculate_todo_completion(perfect_todos) == 100.0
        
        # Scenario 2: No completion (0%)
        no_completion_todos = [MockTodo(False) for _ in range(5)]
        assert utils.calculate_todo_completion(no_completion_todos) == 0.0
        
        # Scenario 3: Exactly 50% completion
        half_completion_todos = [MockTodo(i < 5) for i in range(10)]
        assert utils.calculate_todo_completion(half_completion_todos) == 50.0
        
        # Scenario 4: Above 50% completion (meets FanCode criteria)
        above_threshold_todos = [MockTodo(i < 7) for i in range(10)]  # 70%
        completion_rate = utils.calculate_todo_completion(above_threshold_todos)
        assert completion_rate > 50.0
        assert completion_rate == 70.0
        
        # Scenario 5: Below 50% completion (fails FanCode criteria)
        below_threshold_todos = [MockTodo(i < 3) for i in range(10)]  # 30%
        completion_rate = utils.calculate_todo_completion(below_threshold_todos)
        assert completion_rate < 50.0
        assert completion_rate == 30.0
    
    def test_calculate_todo_completion_edge_cases(self):
        """Test todo completion calculation edge cases"""
        class MockTodo:
            def __init__(self, completed):
                self.completed = completed
        
        # Empty todo list
        assert utils.calculate_todo_completion([]) == 0.0
        
        # Single completed todo
        single_completed = [MockTodo(True)]
        assert utils.calculate_todo_completion(single_completed) == 100.0
        
        # Single incomplete todo
        single_incomplete = [MockTodo(False)]
        assert utils.calculate_todo_completion(single_incomplete) == 0.0
        
        # Large number of todos
        large_todos = [MockTodo(i % 3 == 0) for i in range(1000)]  # Every 3rd is completed
        expected_rate = (334 / 1000) * 100  # Approximately 33.4%
        actual_rate = utils.calculate_todo_completion(large_todos)
        assert abs(actual_rate - expected_rate) < 1.0  # Allow for small rounding differences


class TestUtilityFunctions:
    """Test general utility functions"""
    
    def test_is_email_valid_fancode_emails(self):
        """Test email validation with FanCode-style emails"""
        valid_fancode_emails = [
            "user@fancode.com",
            "test.user@fancode.co.in",
            "admin@fancode.sports",
            "support@fancode.io"
        ]
        
        for email in valid_fancode_emails:
            assert utils.is_email_valid(email) is True, f"{email} should be valid"
    
    def test_is_email_valid_invalid_emails(self):
        """Test email validation with invalid emails"""
        invalid_emails = [
            "notanemail",
            "@fancode.com",
            "user@",
            "user..double.dot@fancode.com",
            "",
            "user@fancode",
            "user name@fancode.com"  # Space in email
        ]
        
        for email in invalid_emails:
            assert utils.is_email_valid(email) is False, f"{email} should be invalid"
    
    def test_safe_get_nested_data(self):
        """Test safe data extraction from nested API responses"""
        # Mock API response structure similar to JSONPlaceholder
        api_response = {
            "user": {
                "id": 1,
                "profile": {
                    "location": {
                        "coordinates": {
                            "lat": -37.3159,
                            "lng": 81.1496
                        }
                    }
                }
            },
            "todos": {
                "completed": 5,
                "total": 10
            }
        }
        
        # Test successful nested access
        assert utils.safe_get(api_response, ["user", "id"]) == 1
        assert utils.safe_get(api_response, ["user", "profile", "location", "coordinates", "lat"]) == -37.3159
        assert utils.safe_get(api_response, ["todos", "completed"]) == 5
        
        # Test failed access (returns None)
        assert utils.safe_get(api_response, ["user", "nonexistent"]) is None
        assert utils.safe_get(api_response, ["user", "profile", "location", "country"]) is None
        assert utils.safe_get(api_response, ["missing", "key"]) is None
        
        # Test with empty dict
        assert utils.safe_get({}, ["any", "key"]) is None
        
        # Test with None input
        assert utils.safe_get(None, ["any"]) is None


class TestUtilityIntegration:
    """Test utility functions with integrated scenarios"""
    
    def test_fancode_user_validation_workflow(self):
        """Test complete workflow using utilities for FanCode user validation"""
        # Mock user data similar to JSONPlaceholder format
        mock_user_data = {
            "id": 1,
            "name": "Test User",
            "email": "test.user@fancode.com",
            "address": {
                "geo": {
                    "lat": "-10.5",
                    "lng": "75.2"
                }
            }
        }
        
        # Extract coordinates using safe_get
        lat = float(utils.safe_get(mock_user_data, ["address", "geo", "lat"]))
        lng = float(utils.safe_get(mock_user_data, ["address", "geo", "lng"]))
        
        # Validate email
        email = utils.safe_get(mock_user_data, ["email"])
        is_valid_email = utils.is_email_valid(email)
        
        # Check if user is in FanCode city
        is_fancode_user = utils.is_in_fancode_city(lat, lng)
        
        # Assertions
        assert lat == -10.5
        assert lng == 75.2
        assert is_valid_email is True
        assert is_fancode_user is True
    
    def test_todo_completion_analysis(self):
        """Test todo completion analysis using utilities"""
        # Mock todos for a FanCode user
        class MockTodo:
            def __init__(self, completed):
                self.completed = completed
        
        # User with good completion rate (should pass FanCode criteria)
        good_todos = [MockTodo(i < 8) for i in range(10)]  # 80% completion
        good_completion = utils.calculate_todo_completion(good_todos)
        
        # User with poor completion rate (should fail FanCode criteria)
        poor_todos = [MockTodo(i < 2) for i in range(10)]  # 20% completion
        poor_completion = utils.calculate_todo_completion(poor_todos)
        
        # FanCode business rule: >50% completion required
        fancode_threshold = 50.0
        
        assert good_completion > fancode_threshold  # Should pass
        assert poor_completion < fancode_threshold  # Should fail
        
        # Log results (similar to actual validator)
        good_status = "PASS" if good_completion > fancode_threshold else "FAIL"
        poor_status = "PASS" if poor_completion > fancode_threshold else "FAIL"
        
        assert good_status == "PASS"
        assert poor_status == "FAIL"


@pytest.mark.parametrize("lat,lng,expected", [
    # Test boundary conditions systematically
    (-40, 5, True),      # Southwest corner
    (-40, 100, True),    # Southeast corner  
    (5, 5, True),        # Northwest corner
    (5, 100, True),      # Northeast corner
    (-40.1, 50, False),  # Just south of boundary
    (5.1, 50, False),    # Just north of boundary
    (0, 4.9, False),     # Just west of boundary
    (0, 100.1, False),   # Just east of boundary
])
def test_fancode_boundary_conditions(lat, lng, expected):
    """Parametrized test for FanCode city boundary conditions"""
    assert utils.is_in_fancode_city(lat, lng) == expected


@pytest.mark.parametrize("completed,total,expected", [
    (0, 10, 0.0),        # No completion
    (5, 10, 50.0),       # Exactly 50%
    (6, 10, 60.0),       # Above threshold
    (10, 10, 100.0),     # Perfect completion
    (1, 3, 33.333),      # Fractional percentage
])
def test_completion_percentage_calculations(completed, total, expected):
    """Parametrized test for completion percentage calculations"""
    class MockTodo:
        def __init__(self, completed):
            self.completed = completed
    
    todos = [MockTodo(i < completed) for i in range(total)]
    result = utils.calculate_todo_completion(todos)
    assert abs(result - expected) < 0.01  # Allow for floating point precision
