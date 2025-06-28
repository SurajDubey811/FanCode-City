"""
BDD Test Runner for FanCode Users Todo Completion
"""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import all step definitions
from features.step_definitions.common_steps import *
from features.step_definitions.fancode_steps import *
from features.step_definitions.api_client_steps import *
from features.step_definitions.data_model_steps import *
from features.step_definitions.utility_steps import *

# Load all scenarios from feature files
scenarios('../features/fancode_users_todo_completion.feature')
scenarios('../features/api_client.feature')
scenarios('../features/data_models.feature')
scenarios('../features/utility_functions.feature')

# This file serves as the main entry point for BDD tests
# All scenarios from the feature files will be automatically discovered and executed
