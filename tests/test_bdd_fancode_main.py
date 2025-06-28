"""
BDD Tests for FanCode Users Todo Completion Validation
Main business logic tests following BDD principles
"""
import pytest
from pytest_bdd import scenarios
import sys
import os
from pytest_bdd import scenarios, given, parsers, when, then

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import step definitions
from features.step_definitions.common_steps import *
from features.step_definitions.fancode_steps import *

# Load scenarios from the main FanCode feature file
scenarios('../features/fancode_users_todo_completion.feature')
