import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.schemas.product import ProductSchema
from app.schemas.category import CategorySchema
from app.schemas.payment_method import PaymentMethodSchema
from app.schemas.general_rating import GeneralRating
from app.services.product_service import list_products, get_product_by_id, enrich_product, get_similar_products



class TestProductService(unittest.TestCase):
    """Test cases for product service functions."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_rating = GeneralRating(
            reviews_count=15,
            ratings_count={5: 8, 4: 4, 3: 2, 2: 1, 1: 0},
            average_rating=4.3
        )
        
        self.mock_db = {
            "products": [
                {
                    "id": 1,
                    "title": "Apple iPhone 14 Pro Max",
                    "description": "Latest generation smartphone with 6.7-inch Super Retina XDR display, triple 48MP camera, and A16 Bionic chip.",
                    "price": 1399.99,
                    "images": [
                        "https://cdn.pixabay.com/photo/2022/05/04/07/38/iphone-13-pro-max-7173413_1280.jpg",
                        "https://cdn.pixabay.com/photo/2022/09/25/22/25/iphones-7479304_1280.jpg"
                    ],
                    "seller_id": 1,
                    "payment_methods_ids": [1, 2, 3],
                    "stock": 12,
                    "category_ids": [1, 3, 4, 6],
                    "features": {
                        "color": ["Black", "Silver", "Gold", "Purple"],
                        "storage": ["128GB", "256GB", "512GB", "1TB"]
                    }
                },
                {
                    "id": 2,
                    "title": "Samsung Galaxy S23 Ultra",
                    "description": "Premium phone with 200MP camera, 6.8-inch Dynamic AMOLED 2X display, and long-lasting battery.",
                    "price": 1299.0,
                    "images": [
                        "https://images.pexels.com/photos/30466731/pexels-photo-30466731.jpeg",
                        "https://images.pexels.com/photos/30466740/pexels-photo-30466740.jpeg"
                    ],
                    "seller_id": 2,
                    "payment_methods_ids": [1, 2, 4],
                    "stock": 7,
                    "category_ids": [1, 2, 4, 6, 7],
                    "features": {
                        "color": ["Black", "Green", "Lavender", "Cream"],
                        "storage": ["256GB", "512GB", "1TB"]
                    }
                },
                {
                    "id": 3,
                    "title": "Xiaomi Redmi Note 12 Pro",
                    "description": "Smartphone with 108MP quad camera, 6.67-inch AMOLED display, and 67W fast charging.",
                    "price": 399.99,
                    "images": [
                        "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-note-12-pro-5g-1.jpg",
                        "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-note-12-pro-5g-2.jpg"
                    ],
                    "seller_id": 3,
                    "payment_methods_ids": [2, 1],
                    "stock": 3,
                    "category_ids": [1, 2, 5, 6, 7],
                    "features": {
                        "color": ["Blue", "Gray", "White"],
                        "storage": ["128GB", "256GB"]
                    }
                },
                {
                    "id": 4,
                    "title": "Motorola Edge 40",
                    "description": "Phone with 6.55-inch OLED display, 50MP main camera, and MediaTek Dimensity 8020 processor.",
                    "price": 499.0,
                    "images": [
                        "https://fdn2.gsmarena.com/vv/pics/motorola/motorola-edge-40-1.jpg",
                        "https://fdn2.gsmarena.com/vv/pics/motorola/motorola-edge-40-2.jpg"
                    ],
                    "seller_id": 4,
                    "payment_methods_ids": [1, 2, 3],
                    "stock": 15,
                    "category_ids": [1, 2, 5, 6, 7],
                    "features": {
                        "color": ["Black", "Green", "Blue"],
                        "storage": ["128GB", "256GB"]
                    }
                },
                {
                    "id": 5,
                    "title": "Google Pixel 6a",
                    "description": "Compact phone with 6.1-inch OLED display and 12MP dual camera.",
                    "price": 449.0,
                    "images": [
                        "https://upload.wikimedia.org/wikipedia/commons/2/2a/Google_Pixel_6a.png"
                    ],
                    "seller_id": 6,
                    "payment_methods_ids": [1, 2, 4],
                    "stock": 6,
                    "category_ids": [1, 2, 4, 6],
                    "features": {
                        "color": ["Charcoal", "Chalk", "Sage"],
                        "storage": ["128GB"]
                    }
                }
            ],
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
            ],
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
        
    def _create_product_schema(self, product_id=1, title="Test Product", description="Test description", 
                              price=99.99, category_ids=None, stock=10, seller_id=1, 
                              payment_methods_ids=None, features=None, images=None):
        """Helper method to create ProductSchema instances with default values."""
        if category_ids is None:
            category_ids = [1]
        if payment_methods_ids is None:
            payment_methods_ids = []
        if features is None:
            features = {}
        if images is None:
            images = ['https://example.com/image.jpg']
            
        return ProductSchema(
            id=product_id,
            title=title,
            description=description,
            price=price,
            images=images,
            seller_id=seller_id,
            payment_methods_ids=payment_methods_ids,
            stock=stock,
            category_ids=category_ids,
            features=features,
            categories=[],
            payment_methods=[],
            rating_info=self.mock_rating
        )
    
    def _create_test_product_data(self, product_id=3, title="Test Product", category_ids=None, payment_methods_ids=None):
        """Helper method to create test product data dictionaries."""
        if category_ids is None:
            category_ids = []
        if payment_methods_ids is None:
            payment_methods_ids = [1]
            
        return {
            "id": product_id,
            "title": title,
            "category_ids": category_ids,
            "payment_methods_ids": payment_methods_ids
        }
    
    @patch('app.services.product_service.generate_general_rating')
    def test_enrich_product_success(self, mock_generate_rating):
        """Test successful product enrichment."""
        # Arrange
        product_data = self.mock_db["products"][0].copy()
        mock_generate_rating.return_value = self.mock_rating
        
        # Act
        result = enrich_product(product_data, self.mock_db)
        
        # Assert
        self.assertIn("categories", result)
        self.assertIn("payment_methods", result)
        self.assertIn("rating_info", result)
        self.assertEqual(len(result["categories"]), 4)
        self.assertEqual(len(result["payment_methods"]), 3)
        self.assertEqual(result["rating_info"], self.mock_rating)
        mock_generate_rating.assert_called_once_with(self.mock_db, "product_id", 1)
    
    @patch('app.services.product_service.generate_general_rating')
    def test_enrich_product_empty_categories(self, mock_generate_rating):
        """Test product enrichment with no categories."""
        # Arrange
        product_data = self._create_test_product_data(category_ids=[], payment_methods_ids=[1])
        mock_generate_rating.return_value = self.mock_rating
        
        # Act
        result = enrich_product(product_data, self.mock_db)
        
        # Assert
        self.assertEqual(len(result["categories"]), 0)
        self.assertEqual(len(result["payment_methods"]), 1)
        mock_generate_rating.assert_called_once_with(self.mock_db, "product_id", 3)
    
    @patch('app.services.product_service.generate_general_rating')
    def test_enrich_product_missing_category_ids(self, mock_generate_rating):
        """Test product enrichment when category_ids is missing."""
        # Arrange
        product_data = self._create_test_product_data(product_id=4)
        del product_data["category_ids"]  # Remove category_ids to test missing field
        mock_generate_rating.return_value = self.mock_rating
        
        # Act
        result = enrich_product(product_data, self.mock_db)
        
        # Assert
        self.assertEqual(len(result["categories"]), 0)
        self.assertEqual(len(result["payment_methods"]), 1)
        mock_generate_rating.assert_called_once_with(self.mock_db, "product_id", 4)
    
    @patch('app.services.product_service.generate_general_rating')
    def test_enrich_product_exception(self, mock_generate_rating):
        """Test handling of exceptions during product enrichment."""
        # Arrange
        product_data = self.mock_db["products"][0].copy()
        mock_generate_rating.side_effect = Exception("Rating error")
        
        # Act & Assert
        with self.assertRaises(RuntimeError) as context:
            enrich_product(product_data, self.mock_db)
        
        self.assertIn("Error enriching product", str(context.exception))
        mock_generate_rating.assert_called_once_with(self.mock_db, "product_id", 1)
    
    @patch('app.services.product_service.enrich_product')
    @patch('app.services.product_service.get_all')
    def test_list_products_success(self, mock_get_all, mock_enrich_product):
        """Test successful retrieval of all products."""
        # Arrange
        mock_get_all.return_value = self.mock_db["products"]
        mock_enrich_product.side_effect = lambda obj, db: obj
        
        # Act
        result = list_products(self.mock_db)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(self.mock_db["products"]))
        self.assertIsInstance(result[0], ProductSchema)
        mock_get_all.assert_called_once_with(self.mock_db, "products")
        self.assertEqual(mock_enrich_product.call_count, len(self.mock_db["products"]))
    
    @patch('app.services.product_service.get_all')
    def test_list_products_empty(self, mock_get_all):
        """Test retrieval when no products exist."""
        # Arrange
        mock_get_all.return_value = []
        
        # Act
        result = list_products(self.mock_db)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        mock_get_all.assert_called_once_with(self.mock_db, "products")
    
    @patch('app.services.product_service.get_all')
    def test_list_products_exception(self, mock_get_all):
        """Test handling of exceptions during product listing."""
        # Arrange
        mock_get_all.side_effect = Exception("Database error")
        
        # Act & Assert
        with self.assertRaises(RuntimeError) as context:
            list_products(self.mock_db)
        
        self.assertIn("Error listing products", str(context.exception))
        mock_get_all.assert_called_once_with(self.mock_db, "products")
    
    @patch('app.services.product_service.enrich_product')
    @patch('app.services.product_service.get_item_by_id')
    def test_get_product_by_id_success(self, mock_get_item, mock_enrich_product):
        """Test successful retrieval of product by ID."""
        # Arrange
        product_id = 1
        expected_product = self.mock_db["products"][0]
        mock_get_item.return_value = expected_product
        mock_enrich_product.return_value = expected_product
        
        # Act
        result = get_product_by_id(self.mock_db, product_id)
        
        # Assert
        self.assertIsInstance(result, ProductSchema)
        self.assertEqual(result.id, product_id)
        mock_get_item.assert_called_once_with(self.mock_db, "products", product_id)
        mock_enrich_product.assert_called_once_with(expected_product, self.mock_db)
    
    @patch('app.services.product_service.get_item_by_id')
    def test_get_product_by_id_not_found(self, mock_get_item):
        """Test handling when product is not found."""
        # Arrange
        product_id = 999
        mock_get_item.side_effect = ValueError(f"Item with id {product_id} not found in table products.")
        
        # Act & Assert
        with self.assertRaises(RuntimeError) as context:
            get_product_by_id(self.mock_db, product_id)
        
        self.assertIn(f"Error getting product by id {product_id}", str(context.exception))
        mock_get_item.assert_called_once_with(self.mock_db, "products", product_id)
    
    @patch('app.services.product_service.enrich_product')
    @patch('app.services.product_service.get_item_by_id')
    def test_get_product_by_id_enrichment_error(self, mock_get_item, mock_enrich_product):
        """Test handling when product enrichment fails."""
        # Arrange
        product_id = 1
        expected_product = self.mock_db["products"][0]
        mock_get_item.return_value = expected_product
        mock_enrich_product.side_effect = RuntimeError("Enrichment error")
        
        # Act & Assert
        with self.assertRaises(RuntimeError) as context:
            get_product_by_id(self.mock_db, product_id)
        
        self.assertIn(f"Error getting product by id {product_id}", str(context.exception))
        mock_get_item.assert_called_once_with(self.mock_db, "products", product_id)
        mock_enrich_product.assert_called_once_with(expected_product, self.mock_db)
    
    def test_product_schema_validation(self):
        """Test ProductSchema validation with valid data."""
        # Arrange
        product_data = {
            "id": 1,
            "title": "Test Product",
            "description": "Test description",
            "price": 99.99,
            "images": ["https://example.com/image1.jpg"],
            "seller_id": 10,
            "payment_methods_ids": [1, 2],
            "stock": 5,
            "category_ids": [1, 2],
            "features": {
            "color": ["Black", "White"],
            "storage": ["64GB", "128GB"]
            },
            "categories": [],
            "payment_methods": [],
            "rating_info": self.mock_rating
        }
        
        # Act
        product = ProductSchema.model_validate(product_data)
        
        # Assert
        self.assertEqual(product.id, 1)
        self.assertEqual(product.title, "Test Product")
        self.assertEqual(product.price, 99.99)
        self.assertEqual(product.rating_info, self.mock_rating)
    
    def test_category_schema_validation(self):
        """Test CategorySchema validation within product enrichment."""
        # Arrange
        category_data = {"id": 1, "name": "Test Category", "description": "Test"}
        
        # Act
        category = CategorySchema.model_validate(category_data)
        
        # Assert
        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "Test Category")
    
    def test_payment_method_schema_validation(self):
        """Test PaymentMethodSchema validation within product enrichment."""
        # Arrange
        payment_data = {"id": 1, "name": "Test Payment", "description": "Test"}
        
        # Act
        payment_method = PaymentMethodSchema.model_validate(payment_data)
        
        # Assert
        self.assertEqual(payment_method.id, 1)
        self.assertEqual(payment_method.name, "Test Payment")

    @patch('app.services.product_service.get_all')
    @patch('app.services.product_service.get_item_by_id')
    def test_get_similar_products_success(self, mock_get_item, mock_get_all):
        """Test successful retrieval of similar products."""
        # Arrange
        target_product_data = self.mock_db["products"][0]  # iPhone 14 Pro Max
        mock_get_item.return_value = target_product_data
        mock_get_all.return_value = self.mock_db["products"]

        # Act
        result = get_similar_products(self.mock_db, 1, limit=3)

        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        # Product 2 (Samsung) shares categories [1,4,6] with iPhone
        # Product 5 (Pixel) shares categories [1,4,6] with iPhone  
        # Product 3 (Xiaomi) shares categories [1,6] with iPhone
        # Product 4 (Motorola) shares categories [1,6] with iPhone
        # Products with more shared categories come first, then sorted by id
        self.assertEqual(result[0].id, 2)  # Samsung - 3 shared categories [1,4,6]
        self.assertEqual(result[1].id, 5)  # Pixel - 3 shared categories [1,4,6]
        self.assertEqual(result[2].id, 3)  # Xiaomi - 2 shared categories [1,6]
        mock_get_item.assert_called_once_with(self.mock_db, "products", 1)
        mock_get_all.assert_called_once_with(self.mock_db, "products")

    @patch('app.services.product_service.get_item_by_id')
    def test_get_similar_products_no_categories(self, mock_get_item):
        """Test similar products when target product has no categories."""
        # Arrange
        product_data = self.mock_db["products"][0].copy()
        product_data["category_ids"] = []
        mock_get_item.return_value = product_data
        
        # Act
        result = get_similar_products(self.mock_db, 1)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        mock_get_item.assert_called_once_with(self.mock_db, "products", 1)

    @patch('app.services.product_service.get_item_by_id')
    def test_get_similar_products_no_similar_found(self, mock_get_item):
        """Test similar products when no similar products are found."""
        # Arrange
        product_data = self.mock_db["products"][0].copy()
        product_data["category_ids"] = []
        mock_get_item.return_value = product_data
        
        # Act
        result = get_similar_products(self.mock_db, 1)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        mock_get_item.assert_called_once_with(self.mock_db, "products", 1)

    @patch('app.services.product_service.get_all')
    @patch('app.services.product_service.get_item_by_id')
    def test_get_similar_products_custom_limit(self, mock_get_item, mock_get_all):
        """Test similar products with custom limit."""
        # Arrange
        target_product_data = self.mock_db["products"][0].copy()
        target_product_data["category_ids"] = [1]
        
        # Create additional products with category [1] to test the limit
        additional_products = []
        for i in range(2, 12):  # Products 2-11
            product = self.mock_db["products"][0].copy()
            product["id"] = i
            product["title"] = f"Product {i}"
            product["description"] = f"Description {i}"
            product["price"] = float(i * 100)
            product["category_ids"] = [1]
            additional_products.append(product)
        
        mock_get_item.return_value = target_product_data
        mock_get_all.return_value = [target_product_data] + additional_products
        
        # Act
        result = get_similar_products(self.mock_db, 1, limit=3)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)  # Should respect the limit
        # Should return first 3 products by ID (2, 3, 4)
        self.assertEqual(result[0].id, 2)
        self.assertEqual(result[1].id, 3)
        self.assertEqual(result[2].id, 4)
        mock_get_item.assert_called_once_with(self.mock_db, "products", 1)
        mock_get_all.assert_called_once_with(self.mock_db, "products")

    @patch('app.services.product_service.get_item_by_id')
    def test_get_similar_products_target_not_found(self, mock_get_item):
        """Test similar products when target product is not found."""
        # Arrange
        mock_get_item.side_effect = ValueError("Item with id 999 not found in table products.")
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            get_similar_products(self.mock_db, 999)
        
        self.assertIn("Item with id 999 not found in table products", str(context.exception))
        mock_get_item.assert_called_once_with(self.mock_db, "products", 999)

    @patch('app.services.product_service.get_all')
    @patch('app.services.product_service.get_item_by_id')
    def test_get_similar_products_list_products_error(self, mock_get_item, mock_get_all):
        """Test similar products when listing all products fails."""
        # Arrange
        target_product_data = self.mock_db["products"][0].copy()
        target_product_data["category_ids"] = [1]
        
        mock_get_item.return_value = target_product_data
        mock_get_all.side_effect = Exception("Database error")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            get_similar_products(self.mock_db, 1)
        
        self.assertIn("Database error", str(context.exception))
        mock_get_item.assert_called_once_with(self.mock_db, "products", 1)
        mock_get_all.assert_called_once_with(self.mock_db, "products")

    @patch('app.services.product_service.get_all')
    @patch('app.services.product_service.get_item_by_id')
    def test_get_similar_products_missing_category_ids_attribute(self, mock_get_item, mock_get_all):
        """Test similar products when some products don't have category_ids attribute."""
        # Arrange
        target_product_data = self.mock_db["products"][0].copy()
        target_product_data["category_ids"] = [1]
        
        # Products with and without category_ids
        product_without_categories = self.mock_db["products"][1].copy()
        product_without_categories["category_ids"] = []  # Empty categories instead of missing
        
        similar_product = self.mock_db["products"][2].copy()
        similar_product["category_ids"] = [1]  # Has matching category
        
        all_products_data = [
            target_product_data,
            product_without_categories,
            similar_product
        ]
        
        mock_get_item.return_value = target_product_data
        mock_get_all.return_value = all_products_data
        
        # Act
        result = get_similar_products(self.mock_db, 1)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)  # Only the product with matching categories
        self.assertEqual(result[0].id, 3)
        mock_get_item.assert_called_once_with(self.mock_db, "products", 1)
        mock_get_all.assert_called_once_with(self.mock_db, "products")


if __name__ == "__main__":
    unittest.main(verbosity=2)
