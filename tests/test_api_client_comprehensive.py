import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from api_client import APIClient
from user import User
from todo import Todo


class TestAPIClientIntegration:
    """Integration tests for API client with real API calls"""
    
    @pytest.fixture(scope="class")
    def api_client(self):
        return APIClient()
    
    def test_get_users_real_api(self, api_client):
        """Test fetching users from real JSONPlaceholder API"""
        users = api_client.get_users()
        
        assert isinstance(users, list)
        assert len(users) > 0, "API should return users"
        assert len(users) == 10, "JSONPlaceholder should return exactly 10 users"
        
        # Validate user structure
        user = users[0]
        assert hasattr(user, 'id')
        assert hasattr(user, 'name')
        assert hasattr(user, 'email')
        assert hasattr(user, 'lat')
        assert hasattr(user, 'lng')
    
    def test_get_todos_real_api(self, api_client):
        """Test fetching todos from real JSONPlaceholder API"""
        todos = api_client.get_todos()
        
        assert isinstance(todos, list)
        assert len(todos) > 0, "API should return todos"
        assert len(todos) == 200, "JSONPlaceholder should return exactly 200 todos"
        
        # Validate todo structure
        todo = todos[0]
        assert hasattr(todo, 'id')
        assert hasattr(todo, 'user_id')
        assert hasattr(todo, 'title')
        assert hasattr(todo, 'completed')
    
    def test_get_user_todos_real_api(self, api_client):
        """Test fetching todos for specific user from real API"""
        user_id = 1
        todos = api_client.get_user_todos(user_id)
        
        assert isinstance(todos, list)
        assert len(todos) > 0, f"User {user_id} should have todos"
        
        # All todos should belong to the requested user
        for todo in todos:
            assert todo.user_id == user_id
    
    def test_fancode_city_users_exist(self, api_client):
        """Test that FanCode city users exist in the API data"""
        users = api_client.get_users()
        fancode_users = []
        
        for user in users:
            if -40 <= user.lat <= 5 and 5 <= user.lng <= 100:
                fancode_users.append(user)
        
        assert len(fancode_users) > 0, "There should be users in FanCode city coordinates"


class TestAPIClientErrorHandling:
    """Test API client error handling and edge cases"""
    
    @patch('requests.Session.get')
    def test_network_error_handling(self, mock_get):
        """Test handling of network errors"""
        mock_get.side_effect = requests.ConnectionError("Network error")
        
        api_client = APIClient()
        
        with pytest.raises(requests.ConnectionError):
            api_client.get_users()
    
    @patch('requests.Session.get')
    def test_http_error_handling(self, mock_get):
        """Test handling of HTTP errors"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        api_client = APIClient()
        
        with pytest.raises(requests.HTTPError):
            api_client.get_todos()
    
    @patch('requests.Session.get')
    def test_invalid_json_response(self, mock_get):
        """Test handling of invalid JSON response"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        api_client = APIClient()
        
        with pytest.raises(ValueError):
            api_client.get_user_todos(1)


class TestAPIClientMocked:
    """Unit tests with mocked responses"""
    
    @patch('requests.Session.get')
    def test_get_users_mocked(self, mock_get):
        """Test get_users with mocked response"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                "id": 1,
                "name": "Test User",
                "username": "testuser",
                "email": "test@example.com",
                "address": {
                    "geo": {
                        "lat": "0.0",
                        "lng": "50.0"
                    }
                }
            }
        ]
        mock_get.return_value = mock_response
        
        api_client = APIClient()
        users = api_client.get_users()
        
        assert len(users) == 1
        assert users[0].name == "Test User"
        assert users[0].lat == 0.0
        assert users[0].lng == 50.0
    
    @patch('requests.Session.get')
    def test_get_todos_mocked(self, mock_get):
        """Test get_todos with mocked response"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                "id": 1,
                "userId": 1,
                "title": "Test Todo",
                "completed": True
            }
        ]
        mock_get.return_value = mock_response
        
        api_client = APIClient()
        todos = api_client.get_todos()
        
        assert len(todos) == 1
        assert todos[0].title == "Test Todo"
        assert todos[0].completed is True


@pytest.mark.performance
class TestAPIClientPerformance:
    """Performance tests for API client"""
    
    def test_users_api_response_time(self):
        """Test that users API responds within acceptable time"""
        import time
        
        api_client = APIClient()
        start_time = time.time()
        users = api_client.get_users()
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 5.0, f"API response time {response_time}s is too slow"
        assert len(users) > 0, "Should return users"
    
    def test_todos_api_response_time(self):
        """Test that todos API responds within acceptable time"""
        import time
        
        api_client = APIClient()
        start_time = time.time()
        todos = api_client.get_todos()
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 5.0, f"API response time {response_time}s is too slow"
        assert len(todos) > 0, "Should return todos"
