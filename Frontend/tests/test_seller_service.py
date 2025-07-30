import unittest
from unittest.mock import patch, MagicMock
import requests
import sys
import os

# Add the parent directory to the path so we can import from services
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock streamlit before importing services that use it
sys.modules['streamlit'] = MagicMock()

# Import mock models instead of real ones
from mock_models import MockSeller, create_mock_seller

# Mock the models module
sys.modules['models'] = MagicMock()
sys.modules['models.seller'] = MagicMock()
sys.modules['models.seller'].Seller = MockSeller

from services.seller_service import get_seller_detail


class TestSellerService(unittest.TestCase):
    """Test cases for seller service functionality"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Mock streamlit session state
        self.mock_st = MagicMock()
        self.mock_st.session_state.get.return_value = "test_token"
        self.mock_st.error = MagicMock()
        
        # Replace the streamlit import in the service module
        import services.seller_service
        services.seller_service.st = self.mock_st
        
        # Replace Seller import in the service module
        services.seller_service.Seller = MockSeller

    def _create_sample_seller_data(self):
        """Helper method to create sample seller data"""
        return {
            "id": 1,
            "name": "Test Seller",
            "location": "Test City",
            "rating_info": {
                "average_rating": 4.5,
                "ratings_count": 100
            }
        }

    @patch('services.seller_service.requests.get')
    def test_get_seller_detail_success(self, mock_get):
        """Test successful seller detail retrieval"""
        # Arrange
        seller_data = self._create_sample_seller_data()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = seller_data
        mock_get.return_value = mock_response
        
        # Act
        result = get_seller_detail(1)
        
        # Assert
        self.assertIsInstance(result, MockSeller)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, "Test Seller")
        self.assertEqual(result.location, "Test City")
        mock_get.assert_called_once_with(
            "http://localhost:8000/sellers/1",
            headers={"Authorization": "Bearer test_token"}
        )

    @patch('services.seller_service.requests.get')
    def test_get_seller_detail_not_found(self, mock_get):
        """Test seller detail retrieval when seller not found"""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Act
        result = get_seller_detail(999)
        
        # Assert
        self.assertIsNone(result)

    @patch('services.seller_service.requests.get')
    def test_get_seller_detail_no_token(self, mock_get):
        """Test seller detail retrieval without token"""
        # Arrange
        self.mock_st.session_state.get.return_value = None
        seller_data = self._create_sample_seller_data()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = seller_data
        mock_get.return_value = mock_response
        
        # Act
        result = get_seller_detail(1)
        
        # Assert
        self.assertIsInstance(result, MockSeller)
        mock_get.assert_called_once_with(
            "http://localhost:8000/sellers/1",
            headers={}
        )

    @patch('services.seller_service.requests.get')
    def test_get_seller_detail_parse_error(self, mock_get):
        """Test seller detail retrieval with JSON parse error"""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        # Act
        result = get_seller_detail(1)
        
        # Assert
        self.assertIsNone(result)
        self.mock_st.error.assert_called_once()

    @patch('services.seller_service.requests.get')
    def test_get_seller_detail_server_error(self, mock_get):
        """Test seller detail retrieval with server error"""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        # Act
        result = get_seller_detail(1)
        
        # Assert
        self.assertIsNone(result)

    @patch('services.seller_service.requests.get')
    def test_get_seller_detail_network_error(self, mock_get):
        """Test seller detail retrieval with network error"""
        # Arrange
        mock_get.side_effect = requests.ConnectionError("Network error")
        
        # Act & Assert
        with self.assertRaises(requests.ConnectionError):
            get_seller_detail(1)

    @patch('services.seller_service.requests.get')
    def test_get_seller_detail_timeout_error(self, mock_get):
        """Test seller detail retrieval with timeout error"""
        # Arrange
        mock_get.side_effect = requests.Timeout("Request timeout")
        
        # Act & Assert
        with self.assertRaises(requests.Timeout):
            get_seller_detail(1)


if __name__ == '__main__':
    unittest.main()
