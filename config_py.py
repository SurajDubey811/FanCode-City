"""
Configuration management for the FanCode test suite
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class APIConfig:
    """API configuration settings"""
    base_url: str = "http://jsonplaceholder.typicode.com"
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0

@dataclass
class FanCodeConfig:
    """FanCode city specific configuration"""
    lat_min: float = -40.0
    lat_max: float = 5.0
    lng_min: float = 5.0
    lng_max: float = 100.0
    completion_threshold: float = 50.0

@dataclass
class TestConfig:
    """Test execution configuration"""
    generate_html_report: bool = True
    generate_json_report: bool = True
    log_level: str = "INFO"
    parallel_execution: bool = False
    max_workers: int = 4

@dataclass
class Config:
    """Main configuration class"""
    api: APIConfig
    fancode: FanCodeConfig
    test: TestConfig
    
    @classmethod
    def load_from_env(cls) -> 'Config':
        """Load configuration from environment variables"""
        api_config = APIConfig(
            base_url=os.getenv('API_BASE_URL', APIConfig.base_url),
            timeout=int(os.getenv('API_TIMEOUT', APIConfig.timeout)),
            max_retries=int(os.getenv('API_MAX_RETRIES', APIConfig.max_retries))
        )
        
        fancode_config = FanCodeConfig(
            lat_min=float(os.getenv('FANCODE_LAT_MIN', FanCodeConfig.lat_min)),
            lat_max=float(os.getenv('FANCODE_LAT_MAX', FanCodeConfig.lat_max)),
            lng_min=float(os.getenv('FANCODE_LNG_MIN', FanCodeConfig.lng_min)),
            lng_max=float(os.getenv('FANCODE_LNG_MAX', FanCodeConfig.lng_max)),
            completion_threshold=float(os.getenv('COMPLETION_THRESHOLD', FanCodeConfig.completion_threshold))
        )
        
        test_config = TestConfig(
            generate_html_report=os.getenv('GENERATE_HTML_REPORT', 'true').lower() == 'true',
            generate_json_report=os.getenv('GENERATE_JSON_REPORT', 'true').lower() == 'true',
            log_level=os.getenv('LOG_LEVEL', TestConfig.log_level),
            parallel_execution=os.getenv('PARALLEL_EXECUTION', 'false').lower() == 'true',
            max_workers=int(os.getenv('MAX_WORKERS', TestConfig.max_workers))
        )
        
        return cls(
            api=api_config,
            fancode=fancode_config,
            test=test_config
        )

# Global configuration instance
config = Config.load_from_env()