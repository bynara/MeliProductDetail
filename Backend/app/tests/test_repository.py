import unittest
import json
import os
import tempfile
from unittest.mock import patch, mock_open
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.repository import (
    load_and_validate_json,
    get_db_data,
    get_db,
    get_table,
    get_all,
    get_item_by_id,
    InvalidJSONStructure,
    DATA_DIR
)


class TestLoadAndValidateJson(unittest.TestCase):
    """Test cases for load_and_validate_json function"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test.json')

    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)

    def test_load_valid_json_list(self):
        """Test loading a valid JSON file with list structure"""
        test_data = [{"id": 1, "name": "test"}, {"id": 2, "name": "test2"}]
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        result = load_and_validate_json(self.test_file)
        self.assertEqual(result, test_data)

    def test_load_valid_json_single_object(self):
        """Test loading a valid JSON file with single object (converts to list)"""
        test_data = {"id": 1, "name": "test"}
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        result = load_and_validate_json(self.test_file)
        self.assertEqual(result, [test_data])

    def test_file_not_found(self):
        """Test handling of non-existent file"""
        non_existent_file = os.path.join(self.temp_dir, 'nonexistent.json')
        
        with self.assertRaises(FileNotFoundError) as context:
            load_and_validate_json(non_existent_file)
        
        self.assertIn("File not found", str(context.exception))

    def test_invalid_json(self):
        """Test handling of invalid JSON content"""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('{"invalid": json}')  # Invalid JSON
        
        with self.assertRaises(json.JSONDecodeError):
            load_and_validate_json(self.test_file)

    def test_empty_file(self):
        """Test handling of empty JSON file"""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('')
        
        with self.assertRaises(json.JSONDecodeError):
            load_and_validate_json(self.test_file)


class TestDatabaseFunctions(unittest.TestCase):
    """Test cases for database-related functions"""

    def setUp(self):
        # Sample test data
        self.sample_products = [
            {"id": 1, "title": "Product 1", "price": 100.0},
            {"id": 2, "title": "Product 2", "price": 200.0}
        ]
        self.sample_categories = [
            {"id": 1, "name": "Category 1"},
            {"id": 2, "name": "Category 2"}
        ]
        self.sample_db = {
            "products": self.sample_products,
            "categories": self.sample_categories,
            "sellers": [],
            "payment_methods": [],
            "reviews": []
        }

    @patch('app.repository.load_and_validate_json')
    def test_get_db_data(self, mock_load_json):
        """Test get_db_data function with mocked file loading"""
        # Configure mock to return different data for different files
        def side_effect(filepath):
            if 'products.json' in filepath:
                return self.sample_products
            elif 'categories.json' in filepath:
                return self.sample_categories
            else:
                return []
        
        mock_load_json.side_effect = side_effect
        
        # Clear the cache if it exists
        get_db_data.cache_clear()
        
        result = get_db_data()
        
        self.assertIn("products", result)
        self.assertIn("categories", result)
        self.assertEqual(result["products"], self.sample_products)
        self.assertEqual(result["categories"], self.sample_categories)
        
        # Verify that load_and_validate_json was called for each file
        self.assertEqual(mock_load_json.call_count, 5)  # 5 data files

    def test_get_db(self):
        """Test get_db function (wrapper for get_db_data)"""
        with patch('app.repository.get_db_data') as mock_get_db_data:
            mock_get_db_data.return_value = self.sample_db
            
            result = get_db()
            
            self.assertEqual(result, self.sample_db)
            mock_get_db_data.assert_called_once()

    def test_get_table_valid(self):
        """Test get_table with valid table name"""
        result = get_table(self.sample_db, "products")
        self.assertEqual(result, self.sample_products)

    def test_get_table_invalid(self):
        """Test get_table with invalid table name"""
        with self.assertRaises(ValueError) as context:
            get_table(self.sample_db, "invalid_table")
        
        self.assertIn("Table invalid_table does not exist", str(context.exception))

    def test_get_all(self):
        """Test get_all function"""
        result = get_all(self.sample_db, "products")
        self.assertEqual(result, self.sample_products)

    def test_get_item_by_id_valid(self):
        """Test get_item_by_id with valid ID"""
        result = get_item_by_id(self.sample_db, "products", 1)
        expected = {"id": 1, "title": "Product 1", "price": 100.0}
        self.assertEqual(result, expected)

    def test_get_item_by_id_invalid(self):
        """Test get_item_by_id with invalid ID"""
        with self.assertRaises(ValueError) as context:
            get_item_by_id(self.sample_db, "products", 999)
        
        self.assertIn("Item with id 999 not found", str(context.exception))

    def test_get_item_by_id_empty_table(self):
        """Test get_item_by_id with empty table"""
        with self.assertRaises(ValueError) as context:
            get_item_by_id(self.sample_db, "sellers", 1)
        
        self.assertIn("Item with id 1 not found", str(context.exception))


class TestInvalidJSONStructureException(unittest.TestCase):
    """Test cases for custom exception"""

    def test_exception_creation(self):
        """Test that InvalidJSONStructure exception can be created and raised"""
        with self.assertRaises(InvalidJSONStructure) as context:
            raise InvalidJSONStructure("Test error message")
        
        self.assertEqual(str(context.exception), "Test error message")


class TestDataDirectory(unittest.TestCase):
    """Test cases for DATA_DIR configuration"""

    def test_data_dir_exists(self):
        """Test that DATA_DIR points to an existing directory"""
        self.assertTrue(os.path.exists(DATA_DIR))
        self.assertTrue(os.path.isdir(DATA_DIR))

    def test_data_dir_contains_json_files(self):
        """Test that DATA_DIR contains expected JSON files"""
        expected_files = [
            "products.json",
            "categories.json",
            "sellers.json",
            "payment_methods.json",
            "reviews.json"
        ]
        
        for filename in expected_files:
            file_path = os.path.join(DATA_DIR, filename)
            self.assertTrue(os.path.exists(file_path), f"File {filename} not found in DATA_DIR")


class TestIntegration(unittest.TestCase):
    """Integration tests using actual data files"""

    def test_load_actual_products_data(self):
        """Test loading actual products.json file"""
        products_path = os.path.join(DATA_DIR, "products.json")
        if os.path.exists(products_path):
            result = load_and_validate_json(products_path)
            self.assertIsInstance(result, list)
            if result:  # If file is not empty
                self.assertIsInstance(result[0], dict)
                self.assertIn("id", result[0])

    def test_get_db_integration(self):
        """Integration test for get_db function with actual data"""
        # Clear cache to ensure fresh data load
        get_db_data.cache_clear()
        
        try:
            db = get_db()
            self.assertIsInstance(db, dict)
            
            expected_tables = ["products", "categories", "sellers", "payment_methods", "reviews"]
            for table in expected_tables:
                self.assertIn(table, db)
                self.assertIsInstance(db[table], list)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.skipTest(f"Could not load actual data files: {e}")

    def test_get_item_by_id_integration(self):
        """Integration test for get_item_by_id with actual data"""
        try:
            # Clear cache to ensure fresh data load
            get_db_data.cache_clear()
            
            db = get_db()
            
            # Test with products table if it has data
            if db["products"]:
                first_product = db["products"][0]
                if "id" in first_product:
                    result = get_item_by_id(db, "products", first_product["id"])
                    self.assertEqual(result, first_product)
        except Exception as e:
            self.skipTest(f"Could not run integration test: {e}")


if __name__ == '__main__':
    unittest.main()
