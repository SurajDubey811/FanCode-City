import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from api_client import APIClient
from validator import FanCodeCityValidator


@pytest.mark.fancode
class TestFanCodeCityValidator:
    """Smoke test for FanCode city validator (comprehensive tests in test_validator_comprehensive.py)"""
    
    @pytest.fixture(scope="class")
    def validator(self):
        client = APIClient()
        return FanCodeCityValidator(client)

    def test_validator_smoke(self, validator):
        """Smoke test: validator instantiation and basic method call"""
        users = validator.get_fancode_users()
        assert isinstance(users, list)
