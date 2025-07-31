import unittest
from unittest.mock import patch, MagicMock
import requests
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.login_service import get_token


class TestLoginService(unittest.TestCase):
    """Test cases for login service functionality"""

    @patch('services.login_service.requests.post')
    def test_get_token_success(self, mock_post):
        """Test successful token retrieval"""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "test_token_123"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Act
        result = get_token("testuser", "testpass")
        
        # Assert
        self.assertEqual(result, "test_token_123")
        mock_post.assert_called_once_with(
            "http://localhost:8000/token",
            data={
                "grant_type": "password",
                "username": "testuser",
                "password": "testpass"
            }
        )

    @patch('services.login_service.requests.post')
    def test_get_token_http_error(self, mock_post):
        """Test token retrieval with HTTP error"""
        # Arrange
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("401 Unauthorized")
        mock_post.return_value = mock_response
        
        # Act & Assert
        with self.assertRaises(requests.HTTPError):
            get_token("invalid_user", "invalid_pass")

    @patch('services.login_service.requests.post')
    def test_get_token_network_error(self, mock_post):
        """Test token retrieval with network error"""
        # Arrange
        mock_post.side_effect = requests.ConnectionError("Network error")
        
        # Act & Assert
        with self.assertRaises(requests.ConnectionError):
            get_token("testuser", "testpass")

    @patch('services.login_service.requests.post')
    def test_get_token_invalid_response_format(self, mock_post):
        """Test token retrieval with invalid JSON response"""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Act & Assert
        with self.assertRaises(ValueError):
            get_token("testuser", "testpass")


if __name__ == '__main__':
    unittest.main()
