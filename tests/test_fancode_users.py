import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import allure
import logging
from typing import Dict
from user import User
from todo import Todo
from api_client import APIClient
from validator import FanCodeCityValidator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@allure.epic("FanCode SDET Assignment")
@allure.feature("User Todo Completion Validation")
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
    
    @allure.story("API Connectivity")
    @allure.title("Verify API endpoints are accessible and return data")
    @allure.description("Test that the JSONPlaceholder API endpoints for users and todos are working correctly")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_api_connectivity(self, api_client):
        """Test API connectivity and basic functionality"""
        with allure.step("Fetch users from API"):
            users = api_client.get_users()
            allure.attach(f"Users count: {len(users)}", "Users Response", allure.attachment_type.TEXT)
        
        with allure.step("Fetch todos from API"):
            todos = api_client.get_todos()
            allure.attach(f"Todos count: {len(todos)}", "Todos Response", allure.attachment_type.TEXT)
        
        with allure.step("Validate API responses"):
            assert len(users) > 0, "No users found in API response"
            assert len(todos) > 0, "No todos found in API response"
        
        logger.info(f"API connectivity test passed: {len(users)} users, {len(todos)} todos")
    
    @allure.story("FanCode City Identification")
    @allure.title("Identify users within FanCode city coordinates")
    @allure.description("Test that the system correctly identifies users within the FanCode city coordinate range")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_fancode_city_identification(self, validator):
        """Test FanCode city user identification logic"""
        with allure.step("Get FanCode city users"):
            fancode_users = validator.get_fancode_users()
            allure.attach(f"FanCode users found: {len(fancode_users)}", "FanCode Users", allure.attachment_type.TEXT)
        
        with allure.step("Validate FanCode users exist"):
            assert len(fancode_users) > 0, "No users found in FanCode city"
        
        with allure.step("Verify coordinate boundaries for all users"):
            # Verify all identified users are within the coordinate range
            for user in fancode_users:
                assert validator.LAT_MIN <= user.lat <= validator.LAT_MAX, \
                    f"User {user.name} lat {user.lat} is outside FanCode city range"
                assert validator.LNG_MIN <= user.lng <= validator.LNG_MAX, \
                    f"User {user.name} lng {user.lng} is outside FanCode city range"
        
        logger.info(f"FanCode city identification test passed for {len(fancode_users)} users")
    
    @allure.story("Todo Completion Calculation")
    @allure.title("Calculate todo completion percentage for a user")
    @allure.description("Test the calculation of todo completion percentage for a user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_todo_completion_calculation(self, validator, api_client):
        """Test todo completion percentage calculation"""
        with allure.step("Get test user"):
            users = api_client.get_users()
            test_user = users[0]  # Use first user for testing
            allure.attach(f"Test user: {test_user.name} (ID: {test_user.id})", "Test User", allure.attachment_type.TEXT)
        
        with allure.step(f"Fetch todos for user {test_user.id}"):
            user_todos = api_client.get_user_todos(test_user.id)
            allure.attach(f"User todos count: {len(user_todos)}", "User Todos", allure.attachment_type.TEXT)
        
        with allure.step("Calculate completion percentage"):
            completion_percentage = validator.calculate_completion_percentage(user_todos)
            allure.attach(f"Completion percentage: {completion_percentage:.2f}%", "Completion Percentage", allure.attachment_type.TEXT)
        
        with allure.step("Validate completion percentage"):
            assert 0 <= completion_percentage <= 100, \
                f"Completion percentage {completion_percentage} is not within valid range"
            
            # Manual calculation verification
            completed_count = sum(1 for todo in user_todos if todo.completed)
            expected_percentage = (completed_count / len(user_todos)) * 100 if user_todos else 0
            
            assert abs(completion_percentage - expected_percentage) < 0.01, \
                f"Completion percentage calculation mismatch"
        
        logger.info(f"Todo completion calculation test passed")
    
    @allure.story("Main Validation Test")
    @allure.title("Validate that all FanCode city users have >50% todo completion")
    @allure.description("Main test to validate the todo completion rate for all users in FanCode city")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_fancode_users_todo_completion_rate(self, validator):
        """Main test: Validate that all FanCode city users have >50% todo completion"""
        with allure.step("Execute validation for all FanCode users"):
            result_summary = validator.validate_all_fancode_users()
        
        # Log detailed results
        logger.info("=" * 60)
        logger.info("FANCODE CITY USERS TODO COMPLETION REPORT")
        logger.info("=" * 60)
        
        with allure.step("Process individual user results"):
            for user_result in result_summary['user_results']:
                status = "✓ PASS" if user_result['passed'] else "✗ FAIL"
                logger.info(f"{status} | {user_result['user_name']} | "
                           f"{user_result['completed_todos']}/{user_result['total_todos']} "
                           f"({user_result['completion_percentage']:.1f}%)")
        
        logger.info("=" * 60)
        logger.info(f"SUMMARY: {result_summary['passed_users']}/{result_summary['total_users']} users passed")
        logger.info(f"OVERALL RESULT: {'PASS' if result_summary['overall_result'] else 'FAIL'}")
        logger.info("=" * 60)
        
        with allure.step("Validate overall result"):
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
