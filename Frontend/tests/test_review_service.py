import unittest
from unittest.mock import patch, MagicMock
import requests
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock streamlit before importing services that use it
sys.modules['streamlit'] = MagicMock()

# Import mock models instead of real ones
from mock_models import MockReview, create_mock_review

# Mock the models module
sys.modules['models'] = MagicMock()
sys.modules['models.review'] = MagicMock()
sys.modules['models.review'].Review = MockReview

from services.review_service import get_product_reviews


class TestReviewService(unittest.TestCase):
    """Test cases for review service functionality"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Mock streamlit session state
        self.mock_st = MagicMock()
        self.mock_st.session_state.get.return_value = "test_token"
        self.mock_st.error = MagicMock()
        
        # Replace the streamlit import in the service module
        import services.review_service
        services.review_service.st = self.mock_st
        
        # Replace Review import in the service module
        services.review_service.Review = MockReview

    def _create_sample_review_data(self, review_id=1):
        """Helper method to create sample review data"""
        return {
            "id": review_id,
            "product_id": 1,
            "buyer": "Test Buyer",
            "rating": 5.0,
            "review": "Great product!",
            "date": "2024-01-01"
        }

    @patch('services.review_service.requests.get')
    def test_get_product_reviews_success(self, mock_get):
        """Test successful product reviews retrieval"""
        # Arrange
        reviews_data = [
            self._create_sample_review_data(1),
            self._create_sample_review_data(2)
        ]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = reviews_data
        mock_get.return_value = mock_response
        
        # Act
        result = get_product_reviews(1)
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], MockReview)
        self.assertIsInstance(result[1], MockReview)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[1].id, 2)
        self.assertEqual(result[0].buyer, "Test Buyer")
        mock_get.assert_called_once_with(
            "http://localhost:8000/reviews/product/1",
            headers={}
        )

    @patch('services.review_service.requests.get')
    def test_get_product_reviews_empty_list(self, mock_get):
        """Test product reviews retrieval with empty response"""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        # Act
        result = get_product_reviews(1)
        
        # Assert
        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, list)

    @patch('services.review_service.requests.get')
    def test_get_product_reviews_no_token(self, mock_get):
        """Test product reviews retrieval without token"""
        # Arrange
        self.mock_st.session_state.get.return_value = None
        reviews_data = [self._create_sample_review_data()]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = reviews_data
        mock_get.return_value = mock_response
        
        # Act
        result = get_product_reviews(1)
        
        # Assert
        self.assertEqual(len(result), 1)
        mock_get.assert_called_once_with(
            "http://localhost:8000/reviews/product/1",
            headers={}
        )

    @patch('services.review_service.requests.get')
    def test_get_product_reviews_error_response(self, mock_get):
        """Test product reviews retrieval with error response"""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Act
        result = get_product_reviews(1)
        
        # Assert
        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, list)

    @patch('services.review_service.requests.get')
    def test_get_product_reviews_parse_error(self, mock_get):
        """Test product reviews retrieval with JSON parse error"""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        # Act
        result = get_product_reviews(1)
        
        # Assert
        self.assertEqual(len(result), 0)
        self.mock_st.error.assert_called_once()

    @patch('services.review_service.requests.get')
    def test_get_product_reviews_network_error(self, mock_get):
        """Test product reviews retrieval with network error"""
        # Arrange
        mock_get.side_effect = requests.ConnectionError("Network error")
        
        # Act & Assert
        with self.assertRaises(requests.ConnectionError):
            get_product_reviews(1)


if __name__ == '__main__':
    unittest.main()
