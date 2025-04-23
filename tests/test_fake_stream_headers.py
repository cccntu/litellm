import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import json

# Add the parent directory to the path to import litellm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import litellm
from litellm.llms.base_llm.chat.transformation import BaseConfig


# Create a concrete subclass of BaseConfig for testing
class TestConfig(BaseConfig):
    def get_supported_openai_params(self, model: str) -> list:
        return []
    
    def map_openai_params(self, non_default_params: dict, optional_params: dict, model: str, drop_params: bool) -> dict:
        return {}
    
    def validate_environment(self, headers: dict, model: str, messages: list, optional_params: dict, litellm_params: dict, api_key=None, api_base=None) -> dict:
        return {}
    
    def transform_request(self, model: str, messages: list, optional_params: dict, litellm_params: dict, headers: dict) -> dict:
        return {}
    
    def transform_response(self, model: str, raw_response, model_response, logging_obj, request_data: dict, messages: list, optional_params: dict, litellm_params: dict, encoding, api_key=None, json_mode=None) -> dict:
        return {}
    
    def get_error_class(self, error_message: str, status_code: int, headers: dict) -> Exception:
        return Exception(error_message)


class TestFakeStreamHeaders(unittest.TestCase):
    def test_sign_request_with_fake_stream(self):
        """
        Test that the sign_request method in BaseConfig sets the accept header to application/json
        when fake_stream is True
        """
        # Create an instance of our TestConfig class
        config = TestConfig()
        
        # Create a test headers dict
        headers = {
            "Content-Type": "application/json",
            "accept": "text/event-stream",  # This is what normally happens with streaming
        }
        
        # Test with fake_stream=True
        updated_headers = config.sign_request(
            headers=headers,
            optional_params={},
            request_data={},
            api_base="https://api.example.com",
            fake_stream=True
        )
        
        # Check that the accept header was changed to application/json
        self.assertEqual(updated_headers["accept"], "application/json")
        
        # Test with fake_stream=False
        headers = {
            "Content-Type": "application/json",
            "accept": "text/event-stream",
        }
        
        updated_headers = config.sign_request(
            headers=headers,
            optional_params={},
            request_data={},
            api_base="https://api.example.com",
            fake_stream=False
        )
        
        # Check that the accept header was not changed
        self.assertEqual(updated_headers["accept"], "text/event-stream")


if __name__ == "__main__":
    unittest.main()