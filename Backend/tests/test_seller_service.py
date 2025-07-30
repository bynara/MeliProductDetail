import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.schemas.seller import SellerSchema
from app.services.seller_service import list_sellers, get_seller_by_id
from app.schemas.general_rating import GeneralRating


class TestSellerService(unittest.TestCase):
    """Test cases for seller service functions."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_db = {
            "sellers": [
                {"id": 1, "name": "Apple Store", "location": "Ciudad de México", "email": "contacto@apple.com", "phone": "555-1234"},
                {"id": 2, "name": "Samsung Shop", "location": "Guadalajara", "email": "ventas@samsung.com", "phone": "555-5678"},
                {"id": 3, "name": "Xiaomi Center", "location": "Monterrey", "email": "info@xiaomi.com", "phone": "555-8765"}
            ]
        }
        
        self.mock_rating = GeneralRating(
            reviews_count=10,
            ratings_count={5: 5, 4: 3, 3: 1, 2: 1, 1: 0},
            average_rating=4.2
        )
    
    @patch('app.services.seller_service.get_all')
    def test_list_sellers_success(self, mock_get_all):
        """Test successful retrieval of all sellers."""
        # Arrange
        mock_get_all.return_value = self.mock_db["sellers"]
        
        # Act
        result = list_sellers(self.mock_db)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].name, "Apple Store")
        mock_get_all.assert_called_once_with(self.mock_db, "sellers")
    
    @patch('app.services.seller_service.get_all')
    def test_list_sellers_empty(self, mock_get_all):
        """Test retrieval when no sellers exist."""
        # Arrange
        mock_get_all.return_value = []
        
        # Act
        result = list_sellers(self.mock_db)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        mock_get_all.assert_called_once_with(self.mock_db, "sellers")
    
    @patch('app.services.seller_service.get_all')
    def test_list_sellers_exception(self, mock_get_all):
        """Test handling of exceptions during seller listing."""
        # Arrange
        mock_get_all.side_effect = Exception("Database error")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            list_sellers(self.mock_db)
        
        self.assertIn("Database error", str(context.exception))
        mock_get_all.assert_called_once_with(self.mock_db, "sellers")
    
    @patch('app.services.seller_service.generate_general_rating')
    @patch('app.services.seller_service.get_item_by_id')
    def test_get_seller_by_id_success(self, mock_get_item, mock_generate_rating):
        """Test successful retrieval of seller by ID."""
        # Arrange
        seller_id = 1
        expected_seller = self.mock_db["sellers"][0]
        mock_get_item.return_value = expected_seller
        mock_generate_rating.return_value = self.mock_rating
        
        # Act
        result = get_seller_by_id(self.mock_db, seller_id)
        
        # Assert
        self.assertEqual(result.id, seller_id)
        self.assertEqual(result.name, "Apple Store")
        self.assertEqual(result.rating_info, self.mock_rating)
        mock_get_item.assert_called_once_with(self.mock_db, "sellers", seller_id)
        mock_generate_rating.assert_called_once_with(self.mock_db, "seller_id", seller_id)
    
    @patch('app.services.seller_service.get_item_by_id')
    def test_get_seller_by_id_not_found(self, mock_get_item):
        """Test handling when seller is not found."""
        # Arrange
        seller_id = 999
        mock_get_item.return_value = None
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            get_seller_by_id(self.mock_db, seller_id)
        
        self.assertEqual(str(context.exception), "Seller not found")
        mock_get_item.assert_called_once_with(self.mock_db, "sellers", seller_id)
    
    @patch('app.services.seller_service.get_item_by_id')
    def test_get_seller_by_id_exception(self, mock_get_item):
        """Test handling of exceptions during seller retrieval by ID."""
        # Arrange
        seller_id = 1
        mock_get_item.side_effect = Exception("Database error")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            get_seller_by_id(self.mock_db, seller_id)
        
        self.assertIn("Database error", str(context.exception))
        mock_get_item.assert_called_once_with(self.mock_db, "sellers", seller_id)
    
    @patch('app.services.seller_service.generate_general_rating')
    @patch('app.services.seller_service.get_item_by_id')
    def test_get_seller_by_id_rating_generation_error(self, mock_get_item, mock_generate_rating):
        """Test handling when rating generation fails."""
        # Arrange
        seller_id = 1
        expected_seller = self.mock_db["sellers"][0]
        mock_get_item.return_value = expected_seller
        mock_generate_rating.side_effect = Exception("Rating error")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            get_seller_by_id(self.mock_db, seller_id)
        
        self.assertIn("Rating error", str(context.exception))
        mock_get_item.assert_called_once_with(self.mock_db, "sellers", seller_id)
        mock_generate_rating.assert_called_once_with(self.mock_db, "seller_id", seller_id)
    
    def test_seller_schema_validation(self):
        """Test SellerSchema validation with valid data."""
        # Arrange
        seller_data = {
            "id": 1, 
            "name": "Apple Store", 
            "location": "Ciudad de México",
            "email": "contacto@apple.com",
            "phone": "555-1234"
        }
        
        # Act
        seller = SellerSchema.model_validate(seller_data)
        
        # Assert
        self.assertEqual(seller.id, 1)
        self.assertEqual(seller.name, "Apple Store")
        self.assertEqual(seller.location, "Ciudad de México")
        self.assertEqual(seller.email, "contacto@apple.com")
        self.assertEqual(seller.phone, "555-1234")
    
    def test_seller_schema_validation_missing_fields(self):
        """Test SellerSchema validation with missing required fields."""
        # Arrange
        invalid_data = {"name": "Apple Store"}  # Missing required fields like id, location, email, phone
        
        # Act & Assert
        with self.assertRaises(Exception):
            SellerSchema.model_validate(invalid_data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
