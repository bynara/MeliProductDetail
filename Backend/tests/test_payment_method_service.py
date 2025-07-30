import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.payment_method_service import list_payment_methods, get_payment_method_by_id
from app.schemas.payment_method import PaymentMethodSchema


class TestPaymentMethodService(unittest.TestCase):
    """Test cases for payment method service functions."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_db = {
            "payment_methods": [
                {
                    "id": 1,
                    "name": "Credit Card",
                    "description": "Payment with credit card from different banks."
                },
                {
                    "id": 2,
                    "name": "Debit Card",
                    "description": "Payment with debit card."
                },
                {
                    "id": 3,
                    "name": "Mercado Pago",
                    "description": "Payment through the Mercado Pago platform."
                },
                {
                    "id": 4,
                    "name": "Cash",
                    "description": "Cash payment at authorized locations."
                }
            ]
        }
    
    @patch('app.services.payment_method_service.get_all')
    def test_list_payment_methods_success(self, mock_get_all):
        """Test successful retrieval of all payment methods."""
        # Arrange
        mock_get_all.return_value = self.mock_db["payment_methods"]
        
        # Act
        result = list_payment_methods(self.mock_db)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)
        self.assertIsInstance(result[0], PaymentMethodSchema)
        self.assertEqual(result[0].name, "Credit Card")
        mock_get_all.assert_called_once_with(self.mock_db, "payment_methods")
    
    @patch('app.services.payment_method_service.get_all')
    def test_list_payment_methods_empty(self, mock_get_all):
        """Test retrieval when no payment methods exist."""
        # Arrange
        mock_get_all.return_value = []
        
        # Act
        result = list_payment_methods(self.mock_db)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        mock_get_all.assert_called_once_with(self.mock_db, "payment_methods")
    
    @patch('app.services.payment_method_service.get_all')
    def test_list_payment_methods_exception(self, mock_get_all):
        """Test handling of exceptions during payment method listing."""
        # Arrange
        mock_get_all.side_effect = Exception("Database error")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            list_payment_methods(self.mock_db)
        
        self.assertIn("Database error", str(context.exception))
        mock_get_all.assert_called_once_with(self.mock_db, "payment_methods")
    
    @patch('app.services.payment_method_service.get_item_by_id')
    def test_get_payment_method_by_id_success(self, mock_get_item):
        """Test successful retrieval of payment method by ID."""
        # Arrange
        payment_method_id = 1
        expected_method = self.mock_db["payment_methods"][0]
        mock_get_item.return_value = expected_method
        
        # Act
        result = get_payment_method_by_id(self.mock_db, payment_method_id)
        
        # Assert
        self.assertIsInstance(result, PaymentMethodSchema)
        self.assertEqual(result.id, payment_method_id)
        self.assertEqual(result.name, "Credit Card")
        mock_get_item.assert_called_once_with(self.mock_db, "payment_methods", payment_method_id)
    
    @patch('app.services.payment_method_service.get_item_by_id')
    def test_get_payment_method_by_id_not_found(self, mock_get_item):
        """Test handling when payment method is not found."""
        # Arrange
        payment_method_id = 999
        mock_get_item.side_effect = ValueError(f"Item with id {payment_method_id} not found in table payment_methods.")
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            get_payment_method_by_id(self.mock_db, payment_method_id)
        
        self.assertIn("not found", str(context.exception))
        mock_get_item.assert_called_once_with(self.mock_db, "payment_methods", payment_method_id)
    
    @patch('app.services.payment_method_service.get_item_by_id')
    def test_get_payment_method_by_id_exception(self, mock_get_item):
        """Test handling of exceptions during payment method retrieval by ID."""
        # Arrange
        payment_method_id = 1
        mock_get_item.side_effect = Exception("Database error")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            get_payment_method_by_id(self.mock_db, payment_method_id)
        
        self.assertIn("Database error", str(context.exception))
        mock_get_item.assert_called_once_with(self.mock_db, "payment_methods", payment_method_id)
    
    def test_payment_method_schema_validation(self):
        """Test PaymentMethodSchema validation with valid data."""
        # Arrange
        method_data = {"id": 1, "name": "Test Method", "description": "Test description"}
        
        # Act
        method = PaymentMethodSchema.model_validate(method_data)
        
        # Assert
        self.assertEqual(method.id, 1)
        self.assertEqual(method.name, "Test Method")
        self.assertEqual(method.description, "Test description")
    
    def test_payment_method_schema_validation_missing_fields(self):
        """Test PaymentMethodSchema validation with missing required fields."""
        # Arrange
        invalid_data = {"name": "Test Method"}  # Missing id
        
        # Act & Assert
        with self.assertRaises(Exception):
            PaymentMethodSchema.model_validate(invalid_data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
