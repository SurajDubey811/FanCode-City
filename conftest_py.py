"""
Pytest configuration and shared fixtures
"""

import pytest
import logging
import os
from datetime import datetime
from pathlib import Path

def pytest_configure(config):
    """Configure pytest"""
    # Create reports directory
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(reports_dir / f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
            logging.StreamHandler()
        ]
    )

def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "FanCode SDET Assignment - Test Report"

def pytest_html_results_summary(prefix, summary, postfix):
    """Customize HTML report summary"""
    prefix.extend([
        "<h3>Test Environment</h3>",
        f"<p>Test execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
        f"<p>API Base URL: http://jsonplaceholder.typicode.com</p>",
        f"<p>FanCode City Coordinates: Lat(-40 to 5), Lng(5 to 100)</p>",
        f"<p>Completion Threshold: >50%</p>"
    ])

@pytest.fixture(scope="session")
def test_session_data():
    """Session-wide test data"""
    return {
        "start_time": datetime.now(),
        "test_environment": "JSONPlaceholder API",
        "fancode_coordinates": {
            "lat_range": (-40, 5),
            "lng_range": (5, 100)
        }
    }

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment(test_session_data):
    """Setup test environment"""
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("FANCODE SDET ASSIGNMENT - TEST EXECUTION STARTED")
    logger.info("=" * 60)
    logger.info(f"Start Time: {test_session_data['start_time']}")
    logger.info(f"Test Environment: {test_session_data['test_environment']}")
    logger.info("=" * 60)
    
    yield
    
    end_time = datetime.now()
    duration = end_time - test_session_data['start_time']
    logger.info("=" * 60)
    logger.info("TEST EXECUTION COMPLETED")
    logger.info(f"End Time: {end_time}")
    logger.info(f"Total Duration: {duration}")
    logger.info("=" * 60)

@pytest.fixture
def api_timeout():
    """API timeout configuration"""
    return 30

@pytest.fixture
def fancode_coordinates():
    """FanCode city coordinate boundaries"""
    return {
        "lat_min": -40,
        "lat_max": 5,
        "lng_min": 5,
        "lng_max": 100
    }

# Pytest markers
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "api: mark test as API test")
    config.addinivalue_line("markers", "fancode: mark test as FanCode specific")