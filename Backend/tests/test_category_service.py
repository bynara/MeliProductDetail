import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.category_service import list_categories, get_category_by_id
from app.schemas.category import CategorySchema


class TestCategoryService(unittest.TestCase):
    """Test cases for category service functions."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_db = {
            "categories": [
                {
                    "id": 1,
                    "name": "Smartphones",
                    "description": "Teléfonos inteligentes de última generación con diversas características y sistemas operativos."
                },
                {
                    "id": 2,
                    "name": "Android",
                    "description": "Dispositivos móviles que utilizan el sistema operativo Android."
                },
                {
                    "id": 3,
                    "name": "iOS",
                    "description": "Dispositivos móviles de Apple que utilizan el sistema operativo iOS."
                },
                {
                    "id": 4,
                    "name": "Gama Alta",
                    "description": "Celulares premium con las mejores especificaciones y tecnología avanzada."
                },
                {
                    "id": 5,
                    "name": "Gama Media",
                    "description": "Celulares con buenas prestaciones a precio accesible."
                },
                {
                    "id": 6,
                    "name": "Fotografía",
                    "description": "Dispositivos destacados por sus capacidades fotográficas."
                },
                {
                    "id": 7,
                    "name": "Carga Rápida",
                    "description": "Celulares que cuentan con tecnología de carga rápida."
                }
            ]
        }
    
    @patch('app.services.category_service.get_all')
    def test_list_categories_success(self, mock_get_all):
        """Test successful retrieval of all categories."""
        # Arrange
        mock_get_all.return_value = self.mock_db["categories"]
        
        # Act
        result = list_categories(self.mock_db)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 7)
        self.assertIsInstance(result[0], CategorySchema)
        self.assertEqual(result[0].name, "Smartphones")
        mock_get_all.assert_called_once_with(self.mock_db, "categories")
    
    @patch('app.services.category_service.get_all')
    def test_list_categories_empty(self, mock_get_all):
        """Test retrieval when no categories exist."""
        # Arrange
        mock_get_all.return_value = []
        
        # Act
        result = list_categories(self.mock_db)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        mock_get_all.assert_called_once_with(self.mock_db, "categories")
    
    @patch('app.services.category_service.get_all')
    def test_list_categories_exception(self, mock_get_all):
        """Test handling of exceptions during category listing."""
        # Arrange
        mock_get_all.side_effect = Exception("Database error")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            list_categories(self.mock_db)
        
        self.assertIn("Database error", str(context.exception))
        mock_get_all.assert_called_once_with(self.mock_db, "categories")
    
    @patch('app.services.category_service.get_item_by_id')
    def test_get_category_by_id_success(self, mock_get_item):
        """Test successful retrieval of category by ID."""
        # Arrange
        category_id = 1
        expected_category = self.mock_db["categories"][0]
        mock_get_item.return_value = expected_category
        
        # Act
        result = get_category_by_id(self.mock_db, category_id)
        
        # Assert
        self.assertIsInstance(result, CategorySchema)
        self.assertEqual(result.id, category_id)
        self.assertEqual(result.name, "Smartphones")
        mock_get_item.assert_called_once_with(self.mock_db, "categories", category_id)
    
    @patch('app.services.category_service.get_item_by_id')
    def test_get_category_by_id_not_found(self, mock_get_item):
        """Test handling when category is not found."""
        # Arrange
        category_id = 999
        mock_get_item.side_effect = ValueError(f"Item with id {category_id} not found in table categories.")
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            get_category_by_id(self.mock_db, category_id)
        
        self.assertIn("not found", str(context.exception))
        mock_get_item.assert_called_once_with(self.mock_db, "categories", category_id)
    
    @patch('app.services.category_service.get_item_by_id')
    def test_get_category_by_id_exception(self, mock_get_item):
        """Test handling of exceptions during category retrieval by ID."""
        # Arrange
        category_id = 1
        mock_get_item.side_effect = Exception("Database error")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            get_category_by_id(self.mock_db, category_id)
        
        self.assertIn("Database error", str(context.exception))
        mock_get_item.assert_called_once_with(self.mock_db, "categories", category_id)
    
    def test_category_schema_validation(self):
        """Test CategorySchema validation with valid data."""
        # Arrange
        category_data = {"id": 1, "name": "Test Category", "description": "Test description"}
        
        # Act
        category = CategorySchema.model_validate(category_data)
        
        # Assert
        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.description, "Test description")
    
    def test_category_schema_validation_missing_fields(self):
        """Test CategorySchema validation with missing required fields."""
        # Arrange
        invalid_data = {"name": "Test Category"}  # Missing id
        
        # Act & Assert
        with self.assertRaises(Exception):
            CategorySchema.model_validate(invalid_data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
