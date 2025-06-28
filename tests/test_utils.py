import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils
import pytest


@pytest.mark.fancode
class TestFanCodeUtilities:
    """Smoke test for FanCode utility functions (comprehensive tests in test_utils_comprehensive.py)"""
    
    def test_utils_smoke(self):
        """Smoke test: utility function import and call"""
        assert utils.is_email_valid("test@example.com")
        # Minimal check for calculate_todo_completion (no dependency on undefined Todo class)
        class DummyTodo:
            def __init__(self, completed):
                self.completed = completed
        # Below FanCode threshold (≤50%)
        todos = [DummyTodo(False), DummyTodo(False)]
        completion = utils.calculate_todo_completion(todos)
        assert completion == 0.0
        assert completion <= 50.0  # Fails FanCode criteria
        # Perfect completion
        todos = [DummyTodo(True)] * 4
        completion = utils.calculate_todo_completion(todos)
        assert completion == 100.0
        # Empty todos
        assert utils.calculate_todo_completion([]) == 0.0
