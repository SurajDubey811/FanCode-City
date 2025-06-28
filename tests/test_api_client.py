import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from api_client import APIClient


@pytest.mark.api
class TestAPIClient:
    """Basic API client tests for FanCode integration"""
    
    @pytest.fixture(scope="class")
    def api_client(self):
        return APIClient()
    
    def test_get_users_returns_list(self, api_client):
        """Test that API returns list of users"""
        users = api_client.get_users()
        assert isinstance(users, list)
        assert users, "API returned empty user list"

    def test_get_todos_returns_list(self, api_client):
        """Test that API returns list of todos"""
        todos = api_client.get_todos()
        assert isinstance(todos, list)
        assert todos, "API returned empty todo list"

    def test_get_user_todos(self, api_client):
        """Test fetching todos for specific user"""
        users = api_client.get_users()
        if users:
            user_id = users[0].id
            todos = api_client.get_user_todos(user_id)
            assert isinstance(todos, list)
            # Verify todos belong to correct user
            for todo in todos:
                assert todo.user_id == user_id
        else:
            pytest.skip("No users available to test get_user_todos")
    
    @pytest.mark.fancode
    def test_users_have_required_fields(self, api_client):
        """Test that users have all required fields for FanCode validation"""
        users = api_client.get_users()
        if users:
            user = users[0]
            # Required for FanCode city validation
            assert hasattr(user, 'id')
            assert hasattr(user, 'name')
            assert hasattr(user, 'lat')
            assert hasattr(user, 'lng')
            assert isinstance(user.lat, (int, float))
            assert isinstance(user.lng, (int, float))
    
    @pytest.mark.fancode  
    def test_todos_have_required_fields(self, api_client):
        """Test that todos have all required fields for completion calculation"""
        todos = api_client.get_todos()
        if todos:
            todo = todos[0]
            # Required for completion percentage calculation
            assert hasattr(todo, 'id')
            assert hasattr(todo, 'user_id') 
            assert hasattr(todo, 'completed')
            assert isinstance(todo.completed, bool)
