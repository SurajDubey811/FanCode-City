"""
Utility functions for the FanCode test suite
"""

import json
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import asdict

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generate various types of reports from test results"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_csv_report(self, validation_results: Dict) -> str:
        """Generate CSV report from validation results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = self.output_dir / f"fancode_users_report_{timestamp}.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            fieldnames = [
                'user_id', 'user_name', 'username', 'latitude', 'longitude',
                'total_todos', 'completed_todos', 'completion_percentage',
                'passed', 'test_timestamp'
            ]
            
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for user_result in validation_results.get('user_results', []):
                row = {
                    'user_id': user_result['user_id'],
                    'user_name': user_result['user_name'],
                    'username': user_result['username'],
                    'latitude': user_result['coordinates']['lat'],
                    'longitude': user_result['coordinates']['lng'],
                    'total_todos': user_result['total_todos'],
                    'completed_todos': user_result['completed_todos'],
                    'completion_percentage': round(user_result['completion_percentage'], 2),
                    'passed': user_result['passed'],
                    'test_timestamp': datetime.now().isoformat()
                }
                writer.writerow(row)
        
        logger.info(f"CSV report generated: {csv_file}")
        return str(csv_file)
    
    def generate_json_summary(self, validation_results: Dict) -> str:
        """Generate JSON summary report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = self.output_dir / f"test_summary_{timestamp}.json"
        
        summary = {
            "test_execution": {
                "timestamp": datetime.now().isoformat(),
                "test_framework": "pytest",
                "api_endpoint": "http://jsonplaceholder.typicode.com"
            },
            "fancode_criteria": {
                "latitude_range": [-40, 5],
                "longitude_range": [5, 100],
                "completion_threshold": 50.0
            },
            "results": validation_results
        }
        
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(summary, file, indent=2, ensure_ascii=False)
        
        logger.info(f"JSON summary generated: {json_file}")
        return str(json_file)

class DataValidator:
    """Additional data validation utilities"""
    
    @staticmethod
    def validate_user_data(user_data: Dict) -> bool:
        """Validate user data structure"""
        required_fields = ['id', 'name', 'username', 'email', 'address']
        
        for field in required_fields:
            if field not in user_data:
                return False
        
        # Validate address structure
        if 'geo' not in user_data['address']:
            return False
        
        geo = user_data['address']['geo']
        if 'lat' not in geo or 'lng' not in geo:
            return False
        
        # Validate coordinate types
        try:
            float(geo['lat'])
            float(geo['lng'])
        except (ValueError, TypeError):
            return False
        
        return True
    
    @staticmethod
    def validate_todo_data(todo_data: Dict) -> bool:
        """Validate todo data structure"""
        required_fields = ['id', 'userId', 'title', 'completed']
        
        for field in required_fields:
            if field not in todo_data:
                return False
        
        # Validate data types
        try:
            int(todo_data['id'])
            int(todo_data['userId'])
            bool(todo_data['completed'])
        except (ValueError, TypeError):
            return False
        
        return True

class TestDataGenerator:
    """Generate test data for unit testing"""
    
    @staticmethod
    def create_mock_user(user_id: int, lat: float, lng: float, name: str = None) -> Dict:
        """Create mock user data"""
        return {
            "id": user_id,
            "name": name or f"Test User {user_id}",
            "username": f"testuser{user_id}",
            "email": f"testuser{user_id}@example.com",
            "address": {
                "street": "Test Street",
                "suite": "Apt. 123",
                "city": "Test City",
                "zipcode": "12345",
                "geo": {
                    "lat": str(lat),
                    "lng": str(lng)
                }
            },
            "phone": "123-456-7890",
            "website": "example.com",
            "company": {
                "name": "Test Company",
                "catchPhrase": "Test catchphrase",
                "bs": "test business"
            }
        }
    
    @staticmethod
    def create_mock_todos(user_id: int, total: int, completed_count: int) -> List[Dict]:
        """Create mock todo data"""
        todos = []
        
        for i in range(total):
            todo = {
                "userId": user_id,
                "id": i + 1 + (user_id * 100),  # Ensure unique IDs
                "title": f"Todo item {i + 1} for user {user_id}",
                "completed": i < completed_count
            }
            todos.append(todo)
        
        return todos

class PerformanceMonitor:
    """Monitor performance metrics during test execution"""
    
    def __init__(self):
        self.metrics = {
            "api_calls": 0,
            "api_response_times": [],
            "start_time": None,
            "end_time": None
        }
    
    def start_monitoring(self):
        """Start performance monitoring"""
        self.metrics["start_time"] = datetime.now()
        logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.metrics["end_time"] = datetime.now()
        logger.info("Performance monitoring stopped")
    
    def record_api_call(self, response_time: float):
        """Record API call metrics"""
        self.metrics["api_calls"] += 1
        self.metrics["api_response_times"].append(response_time)
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary"""
        if not self.metrics["start_time"] or not self.metrics["end_time"]:
            return {"error": "Monitoring not properly started/stopped"}
        
        total_time = (self.metrics["end_time"] - self.metrics["start_time"]).total_seconds()
        response_times = self.metrics["api_response_times"]
        
        summary = {
            "total_execution_time": total_time,
            "total_api_calls": self.metrics["api_calls"],
            "average_response_time": sum(response_times) / len(response_times) if response_times else 0,
            "min_response_time": min(response_times) if response_times else 0,
            "max_response_time": max(response_times) if response_times else 0,
            "api_calls_per_second": self.metrics["api_calls"] / total_time if total_time > 0 else 0
        }
        
        return summary

def setup_custom_logger(name: str, log_file: str = None, level: int = logging.INFO) -> logging.Logger:
    """Setup custom logger with file and console handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def clean_old_reports(reports_dir: str = "reports", days_to_keep: int = 7):
    """Clean old report files"""
    reports_path = Path(reports_dir)
    if not reports_path.exists():
        return
    
    cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
    
    for file_path in reports_path.iterdir():
        if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
            try:
                file_path.unlink()
                logger.info(f"Deleted old report: {file_path}")
            except OSError as e:
                logger.warning(f"Failed to delete {file_path}: {e}")

if __name__ == "__main__":
    # Example usage
    print("FanCode SDET Assignment - Utility Functions")
    print("This module provides utility functions for the test suite.")
    
    # Clean old reports
    clean_old_reports()
    
    # Setup logger
    test_logger = setup_custom_logger("test_logger", "test.log")
    test_logger.info("Utility functions module loaded successfully")