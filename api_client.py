import requests
import logging
from typing import List
from user import User
from todo import Todo

logger = logging.getLogger(__name__)

class APIClient:
    """API client for JSONPlaceholder endpoints"""

    BASE_URL = "http://jsonplaceholder.typicode.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def get_users(self) -> List[User]:
        """Fetch all users from the API"""
        try:
            response = self.session.get(f"{self.BASE_URL}/users")
            response.raise_for_status()
            users_data = response.json()
            return [User.from_dict(user_data) for user_data in users_data]
        except requests.RequestException as e:
            logger.error(f"Failed to fetch users: {e}")
            raise

    def get_todos(self) -> List[Todo]:
        """Fetch all todos from the API"""
        try:
            response = self.session.get(f"{self.BASE_URL}/todos")
            response.raise_for_status()
            todos_data = response.json()
            return [Todo.from_dict(todo_data) for todo_data in todos_data]
        except requests.RequestException as e:
            logger.error(f"Failed to fetch todos: {e}")
            raise

    def get_user_todos(self, user_id: int) -> List[Todo]:
        """Fetch todos for a specific user"""
        try:
            response = self.session.get(f"{self.BASE_URL}/todos?userId={user_id}")
            response.raise_for_status()
            todos_data = response.json()
            return [Todo.from_dict(todo_data) for todo_data in todos_data]
        except requests.RequestException as e:
            logger.error(f"Failed to fetch todos for user {user_id}: {e}")
            raise
