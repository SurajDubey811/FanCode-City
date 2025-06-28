import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils
import pytest


@pytest.mark.fancode
class TestFanCodeUtilities:
    """Test utility functions in FanCode context"""
    
    def test_is_email_valid(self):
        """Test email validation for FanCode users"""
        assert utils.is_email_valid("test@example.com")
        assert utils.is_email_valid("user@fancode.com")
        assert not utils.is_email_valid("invalid-email")
        assert not utils.is_email_valid("@fancode.com")

    def test_safe_get(self):
        """Test safe data extraction from API responses"""
        data = {"a": {"b": 2}}
        assert utils.safe_get(data, ["a", "b"]) == 2
        assert utils.safe_get(data, ["a", "c"]) is None
        assert utils.safe_get({}, ["a"]) is None

    def test_is_in_fancode_city(self):
        """Test FanCode city coordinate validation"""
        # Inside bounds
        assert utils.is_in_fancode_city(0, 10)
        assert utils.is_in_fancode_city(-40, 100)
        assert utils.is_in_fancode_city(5, 5)
        
        # Outside bounds  
        assert not utils.is_in_fancode_city(-41, 10)
        assert not utils.is_in_fancode_city(0, 4)
        assert not utils.is_in_fancode_city(6, 50)
        assert not utils.is_in_fancode_city(0, 101)

    def test_calculate_todo_completion(self):
        """Test todo completion calculation for FanCode users"""
        class Todo:
            def __init__(self, completed):
                self.completed = completed
        
        # Above FanCode threshold (>50%)
        todos = [Todo(True), Todo(False), Todo(True)]
        completion = utils.calculate_todo_completion(todos)
        assert completion == pytest.approx(66.666, rel=1e-2)
        assert completion > 50.0  # Passes FanCode criteria
        
        # Below FanCode threshold (≤50%)
        todos = [Todo(False), Todo(False)]
        completion = utils.calculate_todo_completion(todos)
        assert completion == 0.0
        assert completion <= 50.0  # Fails FanCode criteria
        
        # Perfect completion
        todos = [Todo(True)] * 4
        completion = utils.calculate_todo_completion(todos)
        assert completion == 100.0
        
        # Empty todos
        assert utils.calculate_todo_completion([]) == 0.0
