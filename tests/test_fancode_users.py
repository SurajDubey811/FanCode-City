import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import logging
from typing import Dict
from user import User
from todo import Todo
from api_client import APIClient
from validator import FanCodeCityValidator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TestFanCodeUserTodoCompletion:
    """Test class for FanCode user todo completion validation"""
    
    @pytest.fixture(scope="class")
    def api_client(self):
        """Fixture to provide API client"""
        return APIClient()
    
    @pytest.fixture(scope="class")
    def validator(self, api_client):
        """Fixture to provide validator instance"""
        return FanCodeCityValidator(api_client)
    
    def test_api_connectivity(self, api_client):
        """Test API connectivity and basic functionality"""
        users = api_client.get_users()
        todos = api_client.get_todos()
        
        assert len(users) > 0, "No users found in API response"
        assert len(todos) > 0, "No todos found in API response"
        
        logger.info(f"API connectivity test passed: {len(users)} users, {len(todos)} todos")
    
    def test_fancode_city_identification(self, validator):
        """Test FanCode city user identification logic"""
        fancode_users = validator.get_fancode_users()
        
        assert len(fancode_users) > 0, "No users found in FanCode city"
        
        # Verify all identified users are within the coordinate range
        for user in fancode_users:
            assert validator.LAT_MIN <= user.lat <= validator.LAT_MAX, \
                f"User {user.name} lat {user.lat} is outside FanCode city range"
            assert validator.LNG_MIN <= user.lng <= validator.LNG_MAX, \
                f"User {user.name} lng {user.lng} is outside FanCode city range"
        
        logger.info(f"FanCode city identification test passed for {len(fancode_users)} users")
    
    def test_todo_completion_calculation(self, validator, api_client):
        """Test todo completion percentage calculation"""
        users = api_client.get_users()
        test_user = users[0]  # Use first user for testing
        
        user_todos = api_client.get_user_todos(test_user.id)
        completion_percentage = validator.calculate_completion_percentage(user_todos)
        
        assert 0 <= completion_percentage <= 100, \
            f"Completion percentage {completion_percentage} is not within valid range"
        
        # Manual calculation verification
        completed_count = sum(1 for todo in user_todos if todo.completed)
        expected_percentage = (completed_count / len(user_todos)) * 100 if user_todos else 0
        
        assert abs(completion_percentage - expected_percentage) < 0.01, \
            f"Completion percentage calculation mismatch"
        
        logger.info(f"Todo completion calculation test passed")
    
    def test_fancode_users_todo_completion_rate(self, validator):
        """Main test: Validate that all FanCode city users have >50% todo completion"""
        result_summary = validator.validate_all_fancode_users()
        
        # Log detailed results
        logger.info("=" * 60)
        logger.info("FANCODE CITY USERS TODO COMPLETION REPORT")
        logger.info("=" * 60)
        
        for user_result in result_summary['user_results']:
            status = "✓ PASS" if user_result['passed'] else "✗ FAIL"
            logger.info(f"{status} | {user_result['user_name']} | "
                       f"{user_result['completed_todos']}/{user_result['total_todos']} "
                       f"({user_result['completion_percentage']:.1f}%)")
        
        logger.info("=" * 60)
        logger.info(f"SUMMARY: {result_summary['passed_users']}/{result_summary['total_users']} users passed")
        logger.info(f"OVERALL RESULT: {'PASS' if result_summary['overall_result'] else 'FAIL'}")
        logger.info("=" * 60)
        
        # Assertion for the main requirement
        assert result_summary['total_users'] > 0, "No FanCode city users found"
        
        # Check each user individually
        failed_users = []
        for user_result in result_summary['user_results']:
            if not user_result['passed']:
                failed_users.append(f"{user_result['user_name']} ({user_result['completion_percentage']:.1f}%)")
        
        assert result_summary['overall_result'], \
            f"The following FanCode city users have ≤50% todo completion rate: {', '.join(failed_users)}"
        
        logger.info("🎉 All FanCode city users have more than 50% of their todos completed!")


if __name__ == "__main__":
    # Direct execution for quick testing
    client = APIClient()
    validator = FanCodeCityValidator(client)
    result = validator.validate_all_fancode_users()
    
    print("\n" + "="*60)
    print("QUICK VALIDATION RESULTS")
    print("="*60)
    print(f"Total FanCode users: {result['total_users']}")
    print(f"Users with >50% completion: {result['passed_users']}")
    print(f"Users with ≤50% completion: {result['failed_users']}")
    print(f"Overall result: {'PASS' if result['overall_result'] else 'FAIL'}")
    print("="*60)
