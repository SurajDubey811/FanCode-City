import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from api_client import APIClient
from validator import FanCodeCityValidator


@pytest.mark.fancode
class TestFanCodeCityValidator:
    """Basic validator tests for FanCode city functionality"""
    
    @pytest.fixture(scope="class")
    def validator(self):
        client = APIClient()
        return FanCodeCityValidator(client)

    @pytest.mark.api
    def test_get_fancode_users(self, validator):
        """Test getting users from FanCode city coordinates"""
        users = validator.get_fancode_users()
        assert isinstance(users, list)
        
        # Verify all returned users are within FanCode city bounds
        for user in users:
            assert validator.LAT_MIN <= user.lat <= validator.LAT_MAX, \
                f"User {user.name} lat {user.lat} outside bounds"
            assert validator.LNG_MIN <= user.lng <= validator.LNG_MAX, \
                f"User {user.name} lng {user.lng} outside bounds"

    @pytest.mark.api
    def test_calculate_completion_percentage(self, validator):
        """Test todo completion percentage calculation"""
        users = validator.api_client.get_users()
        if users:
            todos = validator.api_client.get_user_todos(users[0].id)
            percent = validator.calculate_completion_percentage(todos)
            assert 0 <= percent <= 100, f"Invalid percentage: {percent}"
        else:
            pytest.skip("No users available to test completion percentage")

    @pytest.mark.fancode
    def test_validate_all_fancode_users(self, validator):
        """Test validation of all FanCode city users"""
        summary = validator.validate_all_fancode_users()
        
        # Verify result structure
        required_keys = ['overall_result', 'user_results', 'total_users', 'passed_users', 'failed_users']
        for key in required_keys:
            assert key in summary, f"Missing key: {key}"
        
        assert isinstance(summary['user_results'], list)
        assert isinstance(summary['overall_result'], bool)
        
        # Verify user results structure
        if summary['user_results']:
            user_result = summary['user_results'][0]
            user_keys = ['user_id', 'user_name', 'completion_percentage', 'passed']
            for key in user_keys:
                assert key in user_result, f"Missing user result key: {key}"
