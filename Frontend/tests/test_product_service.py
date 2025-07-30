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
from mock_models import MockProduct, create_mock_product

# Mock the models module
sys.modules['models'] = MagicMock()
sys.modules['models.product'] = MagicMock()
sys.modules['models.product'].Product = MockProduct

from services.product_service import get_product_detail, get_similar_products


class TestProductService(unittest.TestCase):
    """Test cases for product service functionality"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Mock streamlit session state
        self.mock_st = MagicMock()
        self.mock_st.session_state.get.return_value = "test_token"
        self.mock_st.error = MagicMock()
        
        # Replace the streamlit import in the service module
        import services.product_service
        services.product_service.st = self.mock_st
        
        # Replace Product import in the service module
        services.product_service.Product = MockProduct

    def _create_sample_product_data(self):
        """Helper method to create sample product data"""
        return {
            "id": 1,
            "title": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "stock": 10,
            "seller_id": 1,
            "images": ["http://example.com/image1.jpg"],
            "payment_methods_ids": [1, 2],
            "category_ids": [1],
            "categories": None,
            "payment_methods": None,
            "features": None,
            "rating_info": None
        }

    @patch('services.product_service.requests.get')
    def test_get_product_detail_success(self, mock_get):
        """Test successful product detail retrieval"""
        # Arrange
        product_data = self._create_sample_product_data()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = product_data
        mock_get.return_value = mock_response
        
        # Act
        result = get_product_detail("1")
        
        # Assert
        self.assertIsInstance(result, MockProduct)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.title, "Test Product")
        self.assertEqual(result.price, 99.99)
        mock_get.assert_called_once_with(
            "http://localhost:8000/products/1",
            headers={"Authorization": "Bearer test_token"}
        )

    @patch('services.product_service.requests.get')
    def test_get_product_detail_not_found(self, mock_get):
        """Test product detail retrieval when product not found"""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Act
        result = get_product_detail("999")
        
        # Assert
        self.assertIsNone(result)

    @patch('services.product_service.requests.get')
    def test_get_product_detail_no_token(self, mock_get):
        """Test product detail retrieval without token"""
        # Arrange
        self.mock_st.session_state.get.return_value = None
        product_data = self._create_sample_product_data()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = product_data
        mock_get.return_value = mock_response
        
        # Act
        result = get_product_detail("1")
        
        # Assert
        self.assertIsInstance(result, MockProduct)
        mock_get.assert_called_once_with(
            "http://localhost:8000/products/1",
            headers={}
        )

    @patch('services.product_service.requests.get')
    def test_get_product_detail_parse_error(self, mock_get):
        """Test product detail retrieval with JSON parse error"""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        # Act
        result = get_product_detail("1")
        
        # Assert
        self.assertIsNone(result)
        self.mock_st.error.assert_called_once()

    @patch('services.product_service.requests.get')
    def test_get_similar_products_success(self, mock_get):
        """Test successful similar products retrieval"""
        # Arrange
        products_data = [
            self._create_sample_product_data(),
            {**self._create_sample_product_data(), "id": 2, "title": "Similar Product 2"}
        ]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = products_data
        mock_get.return_value = mock_response
        
        # Act
        result = get_similar_products("1")
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], MockProduct)
        self.assertIsInstance(result[1], MockProduct)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[1].id, 2)
        mock_get.assert_called_once_with(
            "http://localhost:8000/products/1/similar",
            headers={"Authorization": "Bearer test_token"}
        )

    @patch('services.product_service.requests.get')
    def test_get_similar_products_empty_list(self, mock_get):
        """Test similar products retrieval with empty response"""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        # Act
        result = get_similar_products("1")
        
        # Assert
        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, list)

    @patch('services.product_service.requests.get')
    def test_get_similar_products_error(self, mock_get):
        """Test similar products retrieval with error response"""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        # Act
        result = get_similar_products("1")
        
        # Assert
        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, list)

    @patch('services.product_service.requests.get')
    def test_get_similar_products_parse_error(self, mock_get):
        """Test similar products retrieval with parse error"""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        # Act
        result = get_similar_products("1")
        
        # Assert
        self.assertEqual(len(result), 0)
        self.mock_st.error.assert_called()


if __name__ == '__main__':
    unittest.main()
