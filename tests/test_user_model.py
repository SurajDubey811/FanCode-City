import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from user import User

def test_user_model_fields():
    address = {"geo": {"lat": "0.0", "lng": "0.0"}}
    user = User(id=1, name="Test User", username="testuser", email="test@example.com", address=address, lat=0.0, lng=0.0)
    assert user.id == 1
    assert user.name == "Test User"
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.address == address
    assert user.lat == 0.0
    assert user.lng == 0.0

def test_user_str_repr():
    address = {"geo": {"lat": "1.1", "lng": "2.2"}}
    user = User(id=2, name="Alice", username="alice", email="alice@example.com", address=address, lat=1.1, lng=2.2)
    assert "Alice" in str(user)
    assert "alice@example.com" in repr(user)
