import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from user import User
from todo import Todo


class TestUserModel:
    """Test User data model"""
    
    def test_user_creation_valid_data(self):
        """Test creating user with valid data"""
        address = {"street": "Test St", "geo": {"lat": "0.0", "lng": "0.0"}}
        user = User(
            id=1, 
            name="John Doe", 
            username="johndoe", 
            email="john@example.com",
            address=address,
            lat=0.0, 
            lng=0.0
        )
        
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.username == "johndoe"
        assert user.email == "john@example.com"
        assert user.address == address
        assert user.lat == 0.0
        assert user.lng == 0.0
    
    def test_user_from_dict_jsonplaceholder_format(self):
        """Test creating user from JSONPlaceholder API format"""
        api_data = {
            "id": 1,
            "name": "Leanne Graham",
            "username": "Bret",
            "email": "Sincere@april.biz",
            "address": {
                "street": "Kulas Light",
                "suite": "Apt. 556",
                "city": "Gwenborough",
                "zipcode": "92998-3874",
                "geo": {
                    "lat": "-37.3159",
                    "lng": "81.1496"
                }
            }
        }
        
        user = User.from_dict(api_data)
        
        assert user.id == 1
        assert user.name == "Leanne Graham"
        assert user.username == "Bret"
        assert user.email == "Sincere@april.biz"
        assert user.lat == -37.3159
        assert user.lng == 81.1496
        assert user.address == api_data["address"]
    
    def test_user_fancode_city_coordinates(self):
        """Test users with FanCode city coordinates"""
        # User within FanCode city bounds
        fancode_address = {"geo": {"lat": "0.0", "lng": "50.0"}}
        fancode_user = User(
            id=1, name="FanCode User", username="fancode", 
            email="user@fancode.com", address=fancode_address, lat=0.0, lng=50.0
        )
        
        # Verify coordinates are within FanCode bounds
        assert -40 <= fancode_user.lat <= 5
        assert 5 <= fancode_user.lng <= 100
    
    def test_user_str_representation(self):
        """Test string representation of user"""
        address = {"geo": {"lat": "1.0", "lng": "2.0"}}
        user = User(1, "Alice", "alice", "alice@test.com", address, 1.0, 2.0)
        
        user_str = str(user)
        assert "Alice" in user_str
        assert "1" in user_str  # ID should be in string
    
    def test_user_repr_representation(self):
        """Test repr representation of user"""
        address = {"geo": {"lat": "1.0", "lng": "2.0"}}
        user = User(1, "Alice", "alice", "alice@test.com", address, 1.0, 2.0)
        
        user_repr = repr(user)
        assert "alice@test.com" in user_repr


class TestTodoModel:
    """Test Todo data model"""
    
    def test_todo_creation_valid_data(self):
        """Test creating todo with valid data"""
        todo = Todo(id=1, user_id=1, title="Test Task", completed=True)
        
        assert todo.id == 1
        assert todo.user_id == 1
        assert todo.title == "Test Task"
        assert todo.completed is True
    
    def test_todo_from_dict_jsonplaceholder_format(self):
        """Test creating todo from JSONPlaceholder API format"""
        api_data = {
            "userId": 1,
            "id": 1,
            "title": "delectus aut autem",
            "completed": False
        }
        
        todo = Todo.from_dict(api_data)
        
        assert todo.id == 1
        assert todo.user_id == 1
        assert todo.title == "delectus aut autem"
        assert todo.completed is False
    
    def test_todo_completion_states(self):
        """Test todo with different completion states"""
        completed_todo = Todo(1, 1, "Completed Task", True)
        pending_todo = Todo(2, 1, "Pending Task", False)
        
        assert completed_todo.completed is True
        assert pending_todo.completed is False
    
    def test_todo_str_representation(self):
        """Test string representation of todo"""
        todo = Todo(1, 1, "Sample Task", False)
        
        todo_str = str(todo)
        assert "Sample Task" in todo_str
    
    def test_todo_repr_representation(self):
        """Test repr representation of todo"""
        todo = Todo(1, 1, "Sample Task", False)
        
        todo_repr = repr(todo)
        assert "False" in todo_repr


class TestModelEdgeCases:
    """Test edge cases for data models"""
    
    def test_user_with_extreme_coordinates(self):
        """Test user with extreme but valid coordinates"""
        address = {"geo": {"lat": "-90.0", "lng": "180.0"}}
        user = User(1, "Extreme User", "extreme", "extreme@test.com", address, -90.0, 180.0)
        
        assert user.lat == -90.0
        assert user.lng == 180.0
    
    def test_todo_with_empty_title(self):
        """Test todo with empty title"""
        todo = Todo(1, 1, "", True)
        
        assert todo.title == ""
        assert todo.completed is True
    
    def test_user_with_unicode_name(self):
        """Test user with unicode characters in name"""
        address = {"geo": {"lat": "0.0", "lng": "0.0"}}
        user = User(1, "José María", "jose", "jose@test.com", address, 0.0, 0.0)
        
        assert user.name == "José María"
    
    def test_todo_with_long_title(self):
        """Test todo with very long title"""
        long_title = "A" * 1000
        todo = Todo(1, 1, long_title, False)
        
        assert len(todo.title) == 1000


class TestModelValidation:
    """Test model validation and data integrity"""
    
    def test_user_email_format_examples(self):
        """Test users with various email formats"""
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk"
        ]
        
        for email in valid_emails:
            address = {"geo": {"lat": "0.0", "lng": "0.0"}}
            user = User(1, "Test User", "test", email, address, 0.0, 0.0)
            assert user.email == email
    
    def test_todo_user_id_consistency(self):
        """Test that todo user_id is consistent with user id"""
        user_id = 5
        todo = Todo(1, user_id, "Task for user 5", True)
        
        assert todo.user_id == user_id
    
    def test_coordinate_precision(self):
        """Test coordinate precision handling"""
        address = {"geo": {"lat": "12.345678", "lng": "98.765432"}}
        user = User(1, "Precise User", "precise", "precise@test.com", address, 12.345678, 98.765432)
        
        assert abs(user.lat - 12.345678) < 0.000001
        assert abs(user.lng - 98.765432) < 0.000001


@pytest.mark.fancode_specific
class TestFanCodeModelUseCases:
    """Test models with FanCode-specific use cases"""
    
    def test_fancode_city_user_models(self):
        """Test user models for FanCode city residents"""
        # Sample FanCode city coordinates
        fancode_coordinates = [
            (-30.0, 10.0),  # Within bounds
            (-10.0, 50.0),  # Within bounds
            (0.0, 99.0),    # Within bounds
        ]
        
        for i, (lat, lng) in enumerate(fancode_coordinates, 1):
            address = {"geo": {"lat": str(lat), "lng": str(lng)}}
            user = User(
                id=i,
                name=f"FanCode User {i}",
                username=f"fancode{i}",
                email=f"user{i}@fancode.com",
                address=address,
                lat=lat,
                lng=lng
            )
            
            # Verify within FanCode bounds
            assert -40 <= user.lat <= 5
            assert 5 <= user.lng <= 100
    
    def test_todo_completion_scenarios(self):
        """Test various todo completion scenarios for FanCode users"""
        # High completion rate (>50%)
        high_completion_todos = [
            Todo(i, 1, f"Task {i}", i <= 7) for i in range(1, 11)  # 7/10 = 70%
        ]
        
        # Low completion rate (≤50%)
        low_completion_todos = [
            Todo(i, 2, f"Task {i}", i <= 3) for i in range(1, 11)  # 3/10 = 30%
        ]
        
        # Calculate completion rates
        high_completed = sum(1 for todo in high_completion_todos if todo.completed)
        low_completed = sum(1 for todo in low_completion_todos if todo.completed)
        
        assert (high_completed / len(high_completion_todos)) * 100 > 50
        assert (low_completed / len(low_completion_todos)) * 100 <= 50
