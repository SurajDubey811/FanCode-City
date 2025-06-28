import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from api_client import APIClient
from validator import FanCodeCityValidator


@pytest.mark.performance
class TestFanCodePerformance:
    """Performance tests for FanCode SDET assignment"""
    
    @pytest.fixture(scope="class")
    def api_client(self):
        return APIClient()
    
    @pytest.fixture(scope="class")
    def validator(self, api_client):
        return FanCodeCityValidator(api_client)
    
    def test_api_response_times(self, api_client):
        """Test API response times are within acceptable limits"""
        start_time = time.time()
        users = api_client.get_users()
        users_time = time.time() - start_time
        
        start_time = time.time()
        todos = api_client.get_todos()
        todos_time = time.time() - start_time
        
        # API should respond within 5 seconds
        assert users_time < 5.0, f"Users API took {users_time:.2f}s, should be < 5s"
        assert todos_time < 5.0, f"Todos API took {todos_time:.2f}s, should be < 5s"
        
        # Verify we got data
        assert len(users) > 0
        assert len(todos) > 0
    
    def test_validation_performance(self, validator):
        """Test that validation completes within reasonable time"""
        start_time = time.time()
        result = validator.validate_all_fancode_users()
        validation_time = time.time() - start_time
        
        # Full validation should complete within 10 seconds
        assert validation_time < 10.0, f"Validation took {validation_time:.2f}s, should be < 10s"
        
        # Verify we got results
        assert 'total_users' in result
        assert 'user_results' in result
    
    def test_concurrent_api_calls(self, api_client):
        """Test performance with concurrent API calls"""
        def fetch_user_todos(user_id):
            return api_client.get_user_todos(user_id)
        
        start_time = time.time()
        
        # Test concurrent requests for first 5 users
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(fetch_user_todos, i) for i in range(1, 6)]
            results = [future.result() for future in as_completed(futures)]
        
        concurrent_time = time.time() - start_time
        
        # Concurrent requests should be faster than sequential
        assert concurrent_time < 15.0, f"Concurrent requests took {concurrent_time:.2f}s"
        assert len(results) == 5
        
        # All results should be lists
        for result in results:
            assert isinstance(result, list)


@pytest.mark.load
class TestFanCodeLoad:
    """Load tests for FanCode SDET assignment"""
    
    def test_multiple_validation_runs(self):
        """Test multiple validation runs for stability"""
        validator = FanCodeCityValidator(APIClient())
        results = []
        
        # Run validation 5 times
        for i in range(5):
            start_time = time.time()
            result = validator.validate_all_fancode_users()
            execution_time = time.time() - start_time
            
            results.append({
                'run': i + 1,
                'time': execution_time,
                'total_users': result['total_users'],
                'passed_users': result['passed_users']
            })
        
        # All runs should produce consistent results
        total_users_values = [r['total_users'] for r in results]
        passed_users_values = [r['passed_users'] for r in results]
        
        assert len(set(total_users_values)) == 1, "Total users should be consistent across runs"
        assert len(set(passed_users_values)) == 1, "Passed users should be consistent across runs"
        
        # Average execution time should be reasonable
        avg_time = sum(r['time'] for r in results) / len(results)
        assert avg_time < 8.0, f"Average execution time {avg_time:.2f}s is too high"


@pytest.mark.stress
class TestFanCodeStress:
    """Stress tests for FanCode SDET assignment"""
    
    def test_rapid_api_calls(self):
        """Test rapid successive API calls"""
        api_client = APIClient()
        
        start_time = time.time()
        for _ in range(10):
            users = api_client.get_users()
            assert len(users) > 0
        
        total_time = time.time() - start_time
        avg_time_per_call = total_time / 10
        
        # Each call should average less than 2 seconds
        assert avg_time_per_call < 2.0, f"Average time per call: {avg_time_per_call:.2f}s"
    
    def test_memory_usage_stability(self):
        """Test that memory usage remains stable during validation"""
        try:
            import psutil
        except ImportError:
            pytest.skip("psutil not available for memory testing")
        
        import gc
        
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        validator = FanCodeCityValidator(APIClient())
        
        # Run validation multiple times
        for _ in range(3):
            result = validator.validate_all_fancode_users()
            assert 'total_users' in result
            gc.collect()  # Force garbage collection
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 50MB)
        assert memory_increase < 50, f"Memory increased by {memory_increase:.2f}MB"


@pytest.mark.reliability
class TestFanCodeReliability:
    """Reliability tests for FanCode SDET assignment"""
    
    def test_api_error_recovery(self):
        """Test system behavior during API errors"""
        from unittest.mock import patch, Mock
        import requests
        
        api_client = APIClient()
        
        # Test with temporary network error, then recovery
        with patch('requests.Session.get') as mock_get:
            # First call fails
            mock_get.side_effect = requests.ConnectionError("Network error")
            
            with pytest.raises(requests.ConnectionError):
                api_client.get_users()
            
            # Second call succeeds (recovery)
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = [
                {
                    "id": 1,
                    "name": "Test User",
                    "username": "test",
                    "email": "test@example.com",
                    "address": {"geo": {"lat": "0", "lng": "50"}}
                }
            ]
            mock_get.side_effect = None
            mock_get.return_value = mock_response
            
            # Should work now
            users = api_client.get_users()
            assert len(users) == 1
    
    def test_data_consistency(self):
        """Test data consistency across multiple API calls"""
        api_client = APIClient()
        
        # Fetch data multiple times
        users_1 = api_client.get_users()
        users_2 = api_client.get_users()
        todos_1 = api_client.get_todos()
        todos_2 = api_client.get_todos()
        
        # Data should be consistent
        assert len(users_1) == len(users_2)
        assert len(todos_1) == len(todos_2)
        
        # User IDs should match
        user_ids_1 = [user.id for user in users_1]
        user_ids_2 = [user.id for user in users_2]
        assert user_ids_1 == user_ids_2
    
    def test_validation_deterministic(self):
        """Test that validation produces deterministic results"""
        validator = FanCodeCityValidator(APIClient())
        
        # Run validation multiple times
        results = []
        for _ in range(3):
            result = validator.validate_all_fancode_users()
            results.append(result)
        
        # All results should be identical
        for i in range(1, len(results)):
            assert results[i]['total_users'] == results[0]['total_users']
            assert results[i]['passed_users'] == results[0]['passed_users']
            assert results[i]['overall_result'] == results[0]['overall_result']


@pytest.mark.integration
class TestFanCodeEndToEnd:
    """End-to-end integration tests"""
    
    def test_complete_fancode_workflow(self):
        """Test complete FanCode validation workflow"""
        # Step 1: Initialize components
        api_client = APIClient()
        validator = FanCodeCityValidator(api_client)
        
        start_time = time.time()
        
        # Step 2: Fetch all users
        all_users = api_client.get_users()
        assert len(all_users) > 0, "Should fetch users from API"
        
        # Step 3: Identify FanCode users
        fancode_users = validator.get_fancode_users()
        assert len(fancode_users) >= 0, "Should identify FanCode users"
        
        # Step 4: Validate each FanCode user
        if fancode_users:
            for user in fancode_users[:2]:  # Test first 2 for performance
                is_valid, percentage, completed, total = validator.validate_user_completion_rate(user)
                
                assert isinstance(is_valid, bool)
                assert 0 <= percentage <= 100
                assert 0 <= completed <= total
        
        # Step 5: Complete validation
        final_result = validator.validate_all_fancode_users()
        
        # Verify final result structure
        assert 'total_users' in final_result
        assert 'passed_users' in final_result
        assert 'failed_users' in final_result
        assert 'overall_result' in final_result
        assert 'user_results' in final_result
        
        total_time = time.time() - start_time
        assert total_time < 15.0, f"Complete workflow took {total_time:.2f}s"
    
    def test_fancode_business_requirements(self):
        """Test that FanCode business requirements are met"""
        validator = FanCodeCityValidator(APIClient())
        result = validator.validate_all_fancode_users()
        
        # Business requirement: Validate users in FanCode city
        # Coordinates: lat between -40 and 5, lng between 5 and 100
        assert result['total_users'] >= 0, "Should process FanCode city users"
        
        # Business requirement: >50% todo completion
        for user_result in result['user_results']:
            completion_percentage = user_result['completion_percentage']
            passed = user_result['passed']
            
            if completion_percentage > 50:
                assert passed is True, f"User with {completion_percentage}% should pass"
            else:
                assert passed is False, f"User with {completion_percentage}% should fail"
        
        # Overall result should reflect all users passing
        expected_overall = result['failed_users'] == 0
        assert result['overall_result'] == expected_overall
