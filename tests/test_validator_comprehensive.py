import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import Mock, patch
from validator import FanCodeCityValidator
from api_client import APIClient
from user import User
from todo import Todo


class TestFanCodeValidatorUnit:
    """Unit tests for FanCode city validator"""
    
    @pytest.fixture
    def mock_api_client(self):
        return Mock(spec=APIClient)
    
    @pytest.fixture
    def validator(self, mock_api_client):
        return FanCodeCityValidator(mock_api_client)
    
    def test_is_fancode_city_user_within_bounds(self, validator):
        """Test user within FanCode city bounds"""
        # Create test users
        fancode_user = User(
            id=1, name="FanCode User", username="fancode", 
            email="test@fancode.com", address={}, lat=0.0, lng=50.0
        )
        outside_user = User(
            id=2, name="Outside User", username="outside", 
            email="test@outside.com", address={}, lat=50.0, lng=150.0
        )
        
        assert validator.is_fancode_city_user(fancode_user) is True
        assert validator.is_fancode_city_user(outside_user) is False
    
    def test_calculate_completion_percentage_edge_cases(self, validator):
        """Test completion percentage calculation edge cases"""
        # Empty todos
        assert validator.calculate_completion_percentage([]) == 0.0
        
        # All completed
        all_completed = [
            Todo(1, 1, "Task 1", True),
            Todo(2, 1, "Task 2", True)
        ]
        assert validator.calculate_completion_percentage(all_completed) == 100.0
        
        # None completed
        none_completed = [
            Todo(1, 1, "Task 1", False),
            Todo(2, 1, "Task 2", False)
        ]
        assert validator.calculate_completion_percentage(none_completed) == 0.0
        
        # Mixed completion
        mixed = [
            Todo(1, 1, "Task 1", True),
            Todo(2, 1, "Task 2", False),
            Todo(3, 1, "Task 3", True)
        ]
        expected = (2/3) * 100  # 66.67%
        assert abs(validator.calculate_completion_percentage(mixed) - expected) < 0.01


class TestFanCodeValidatorBoundaryConditions:
    """Test boundary conditions for FanCode city validation"""
    
    @pytest.fixture
    def validator(self):
        return FanCodeCityValidator(Mock(spec=APIClient))
    
    @pytest.mark.parametrize("lat,lng,expected", [
        # Exact boundaries
        (-40, 5, True),      # Min lat, min lng
        (-40, 100, True),    # Min lat, max lng
        (5, 5, True),        # Max lat, min lng
        (5, 100, True),      # Max lat, max lng
        
        # Just outside boundaries
        (-40.1, 50, False),  # Below min lat
        (5.1, 50, False),    # Above max lat
        (0, 4.9, False),     # Below min lng
        (0, 100.1, False),   # Above max lng
        
        # Well within boundaries
        (0, 50, True),
        (-20, 75, True)
    ])
    def test_boundary_coordinates(self, validator, lat, lng, expected):
        """Test coordinate boundary conditions"""
        user = User(
            id=1, name="Test User", username="test", 
            email="test@test.com", address={}, lat=lat, lng=lng
        )
        assert validator.is_fancode_city_user(user) == expected


class TestFanCodeValidatorIntegration:
    """Integration tests with real API data"""
    
    @pytest.fixture(scope="class")
    def validator(self):
        return FanCodeCityValidator(APIClient())
    
    def test_get_fancode_users_integration(self, validator):
        """Test getting FanCode users from real API"""
        fancode_users = validator.get_fancode_users()
        
        assert isinstance(fancode_users, list)
        # Verify all returned users are within bounds
        for user in fancode_users:
            assert validator.LAT_MIN <= user.lat <= validator.LAT_MAX
            assert validator.LNG_MIN <= user.lng <= validator.LNG_MAX
    
    def test_validate_user_completion_rate_integration(self, validator):
        """Test user validation with real API data"""
        # Get a FanCode user
        fancode_users = validator.get_fancode_users()
        if fancode_users:
            user = fancode_users[0]
            is_valid, percentage, completed, total = validator.validate_user_completion_rate(user)
            
            assert isinstance(is_valid, bool)
            assert 0 <= percentage <= 100
            assert completed >= 0
            assert total >= 0
            assert completed <= total
    
    def test_validate_all_fancode_users_structure(self, validator):
        """Test the structure of validation results"""
        result = validator.validate_all_fancode_users()
        
        # Check result structure
        required_keys = ['total_users', 'passed_users', 'failed_users', 'overall_result', 'user_results']
        for key in required_keys:
            assert key in result
        
        # Check data types
        assert isinstance(result['total_users'], int)
        assert isinstance(result['passed_users'], int)
        assert isinstance(result['failed_users'], int)
        assert isinstance(result['overall_result'], bool)
        assert isinstance(result['user_results'], list)
        
        # Check user result structure
        if result['user_results']:
            user_result = result['user_results'][0]
            user_required_keys = [
                'user_id', 'user_name', 'username', 'coordinates',
                'total_todos', 'completed_todos', 'completion_percentage', 'passed'
            ]
            for key in user_required_keys:
                assert key in user_result


class TestFanCodeValidatorMocked:
    """Test validator with mocked dependencies"""
    
    @pytest.fixture
    def mock_api_client(self):
        mock_client = Mock(spec=APIClient)
        
        # Mock users data
        mock_users = [
            User(1, "FanCode User 1", "fc1", "fc1@test.com", {}, lat=0.0, lng=50.0),
            User(2, "FanCode User 2", "fc2", "fc2@test.com", {}, lat=-10.0, lng=75.0),
            User(3, "Outside User", "out", "out@test.com", {}, lat=50.0, lng=150.0)
        ]
        mock_client.get_users.return_value = mock_users
        
        # Mock todos for users
        def mock_get_user_todos(user_id):
            if user_id == 1:  # 75% completion (3/4)
                return [
                    Todo(1, 1, "Task 1", True),
                    Todo(2, 1, "Task 2", True),
                    Todo(3, 1, "Task 3", True),
                    Todo(4, 1, "Task 4", False)
                ]
            elif user_id == 2:  # 25% completion (1/4)
                return [
                    Todo(5, 2, "Task 5", True),
                    Todo(6, 2, "Task 6", False),
                    Todo(7, 2, "Task 7", False),
                    Todo(8, 2, "Task 8", False)
                ]
            return []
        
        mock_client.get_user_todos.side_effect = mock_get_user_todos
        return mock_client
    
    @pytest.fixture
    def validator(self, mock_api_client):
        return FanCodeCityValidator(mock_api_client)
    
    def test_get_fancode_users_mocked(self, validator):
        """Test getting FanCode users with mocked data"""
        fancode_users = validator.get_fancode_users()
        
        assert len(fancode_users) == 2  # Only 2 users are in FanCode city
        assert fancode_users[0].name == "FanCode User 1"
        assert fancode_users[1].name == "FanCode User 2"
    
    def test_validate_all_fancode_users_mocked(self, validator):
        """Test validation with known outcomes"""
        result = validator.validate_all_fancode_users()
        
        assert result['total_users'] == 2
        assert result['passed_users'] == 1  # Only user 1 has >50% completion
        assert result['failed_users'] == 1  # User 2 has <50% completion
        assert result['overall_result'] is False  # Not all users passed
        
        # Check individual results
        user_results = result['user_results']
        assert len(user_results) == 2
        
        # User 1 should pass (75% completion)
        user1_result = next(r for r in user_results if r['user_id'] == 1)
        assert user1_result['passed'] is True
        assert user1_result['completion_percentage'] == 75.0
        
        # User 2 should fail (25% completion)
        user2_result = next(r for r in user_results if r['user_id'] == 2)
        assert user2_result['passed'] is False
        assert user2_result['completion_percentage'] == 25.0


@pytest.mark.business_logic
class TestFanCodeBusinessRules:
    """Test FanCode-specific business logic"""
    
    def test_fancode_city_coordinates_constants(self):
        """Test that FanCode city coordinates are correctly defined"""
        validator = FanCodeCityValidator(Mock())
        
        assert validator.LAT_MIN == -40
        assert validator.LAT_MAX == 5
        assert validator.LNG_MIN == 5
        assert validator.LNG_MAX == 100
        assert validator.COMPLETION_THRESHOLD == 50.0
    
    def test_50_percent_threshold_rule(self):
        """Test the 50% completion threshold rule"""
        validator = FanCodeCityValidator(Mock())
        
        # Exactly 50% should fail (business rule is >50%)
        todos_50_percent = [Todo(i, 1, f"Task {i}", i < 5) for i in range(10)]  # 5/10 = 50%
        percentage = validator.calculate_completion_percentage(todos_50_percent)
        assert percentage == 50.0
        
        # Mock user for validation
        mock_user = User(1, "Test", "test", "test@test.com", {}, 0, 50)
        validator.api_client = Mock()
        validator.api_client.get_user_todos.return_value = todos_50_percent
        
        is_valid, _, _, _ = validator.validate_user_completion_rate(mock_user)
        assert is_valid is False  # Exactly 50% should not pass
