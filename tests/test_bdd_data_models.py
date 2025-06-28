"""
BDD Tests for Data Models
"""
import pytest
from pytest_bdd import scenarios
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import step definitions
from features.step_definitions.common_steps import *
from features.step_definitions.data_model_steps import *

# Load scenarios from the data models feature file
scenarios('../features/data_models.feature')
