import logging
from typing import List, Tuple, Dict
from user import User
from todo import Todo
from api_client import APIClient

logger = logging.getLogger(__name__)

class FanCodeCityValidator:
    """Validator class for FanCode city users and their todo completion rates"""

    # FanCode city coordinates constraints
    LAT_MIN = -40
    LAT_MAX = 5
    LNG_MIN = 5
    LNG_MAX = 100
    COMPLETION_THRESHOLD = 50.0  # 50% completion threshold

    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def is_fancode_city_user(self, user: User) -> bool:
        """Check if user belongs to FanCode city based on coordinates"""
        return (self.LAT_MIN <= user.lat <= self.LAT_MAX and 
                self.LNG_MIN <= user.lng <= self.LNG_MAX)

    def calculate_completion_percentage(self, todos: List[Todo]) -> float:
        """Calculate the percentage of completed todos"""
        if not todos:
            return 0.0

        completed_todos = sum(1 for todo in todos if todo.completed)
        total_todos = len(todos)
        return (completed_todos / total_todos) * 100

    def get_fancode_users(self) -> List[User]:
        """Get all users belonging to FanCode city"""
        all_users = self.api_client.get_users()
        fancode_users = [user for user in all_users if self.is_fancode_city_user(user)]

        logger.info(f"Found {len(fancode_users)} users in FanCode city out of {len(all_users)} total users")
        return fancode_users

    def validate_user_completion_rate(self, user: User) -> Tuple[bool, float, int, int]:
        """
        Validate if user has more than 50% todos completed
        Returns: (is_valid, completion_percentage, completed_count, total_count)
        """
        user_todos = self.api_client.get_user_todos(user.id)
        completion_percentage = self.calculate_completion_percentage(user_todos)
        completed_count = sum(1 for todo in user_todos if todo.completed)
        total_count = len(user_todos)

        is_valid = completion_percentage > self.COMPLETION_THRESHOLD

        logger.info(f"User {user.name} (ID: {user.id}): {completed_count}/{total_count} "
                   f"todos completed ({completion_percentage:.1f}%) - {'PASS' if is_valid else 'FAIL'}")

        return is_valid, completion_percentage, completed_count, total_count

    def validate_all_fancode_users(self) -> Dict:
        """Validate all FanCode city users' todo completion rates"""
        fancode_users = self.get_fancode_users()

        if not fancode_users:
            logger.warning("No users found in FanCode city")
            return {
                'total_users': 0,
                'passed_users': 0,
                'failed_users': 0,
                'overall_result': False,
                'user_results': []
            }

        user_results = []
        passed_count = 0

        for user in fancode_users:
            is_valid, completion_percentage, completed_count, total_count = self.validate_user_completion_rate(user)

            user_result = {
                'user_id': user.id,
                'user_name': user.name,
                'username': user.username,
                'coordinates': {'lat': user.lat, 'lng': user.lng},
                'total_todos': total_count,
                'completed_todos': completed_count,
                'completion_percentage': completion_percentage,
                'passed': is_valid
            }

            user_results.append(user_result)

            if is_valid:
                passed_count += 1

        overall_result = passed_count == len(fancode_users)

        result_summary = {
            'total_users': len(fancode_users),
            'passed_users': passed_count,
            'failed_users': len(fancode_users) - passed_count,
            'overall_result': overall_result,
            'user_results': user_results
        }

        logger.info(f"Validation Summary: {passed_count}/{len(fancode_users)} users passed the 50% completion criteria")

        return result_summary
