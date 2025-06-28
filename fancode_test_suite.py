import pytest
import requests
import logging
from typing import List, Dict, Tuple
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class User:
    """Data class to represent a user"""
    id: int
    name: str
    username: str
    email: str
    address: Dict
    lat: float
    lng: float
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Create User object from API response"""
        return cls(
            id=data['id'],
            name=data['name'],
            username=data['username'],
            email=data['email'],
            address=data['address'],
            lat=float(data['address']['geo']['lat']),
            lng=float(data['address']['geo']['lng'])
        )

@dataclass
class Todo:
    """Data class to represent a todo task"""
    id: int
    user_id: int
    title: str
    completed: bool
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Todo':
        """Create Todo object from API response"""
        return cls(
            id=data['id'],
            user_id=data['userId'],
            title=data['title'],
            completed=data['completed']
        )

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

# Test Class
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