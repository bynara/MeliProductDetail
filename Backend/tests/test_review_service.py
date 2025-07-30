import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import the app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.review_service import (
    list_reviews, get_review_by_id, get_reviews_by_key,
    calculate_ratings_count, calculate_average_rating, generate_general_rating
)
from app.schemas.review import ReviewSchema
from app.schemas.general_rating import GeneralRating


class TestReviewService(unittest.TestCase):
    """Test cases for review service functions."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_db = {
            "reviews": [
                {"id": 1, "product_id": 1, "seller_id": 1, "buyer": "Carlos Méndez", "review": "Excelente cámara y rendimiento, muy satisfecho con la compra.", "rating": 5, "date": "2024-05-01"},
                {"id": 2, "product_id": 1, "seller_id": 1, "buyer": "Ana Torres", "review": "El precio es alto pero la calidad lo vale. Muy buen equipo.", "rating": 4, "date": "2024-05-02"},
                {"id": 3, "product_id": 2, "seller_id": 2, "buyer": "Luis García", "review": "La cámara de 200MP es impresionante, batería dura todo el día.", "rating": 5, "date": "2024-05-03"},
                {"id": 4, "product_id": 1, "seller_id": 1, "buyer": "María López", "review": "Pantalla espectacular, aunque esperaba más de la autonomía.", "rating": 4, "date": "2024-05-04"},
                {"id": 5, "product_id": 2, "seller_id": 2, "buyer": "Sergio Peña", "review": "Muy buen rendimiento en juegos.", "rating": 5, "date": "2024-05-05"}
            ]
        }
    
    @patch('app.services.review_service.get_all')
    def test_list_reviews_success(self, mock_get_all):
        """Test successful retrieval of all reviews."""
        # Arrange
        mock_get_all.return_value = self.mock_db["reviews"]
        
        # Act
        result = list_reviews(self.mock_db)
        
        # Assert
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].rating, 5)
        self.assertEqual(result[0].buyer, "Carlos Méndez")
        mock_get_all.assert_called_once_with(self.mock_db, "reviews")
    
    @patch('app.services.review_service.get_all')
    def test_list_reviews_empty(self, mock_get_all):
        """Test retrieval when no reviews exist."""
        # Arrange
        mock_get_all.return_value = []
        
        # Act
        result = list_reviews(self.mock_db)
        
        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        mock_get_all.assert_called_once_with(self.mock_db, "reviews")
    
    @patch('app.services.review_service.get_item_by_id')
    def test_get_review_by_id_success(self, mock_get_item):
        """Test successful retrieval of review by ID."""
        # Arrange
        review_id = 1
        expected_review = self.mock_db["reviews"][0]
        mock_get_item.return_value = expected_review
        
        # Act
        result = get_review_by_id(self.mock_db, review_id)
        
        # Assert
        self.assertEqual(result.id, review_id)
        self.assertEqual(result.rating, 5)
        self.assertEqual(result.buyer, "Carlos Méndez")
        mock_get_item.assert_called_once_with(self.mock_db, "reviews", review_id)
    
    def test_get_reviews_by_key_product_id(self):
        """Test filtering reviews by product_id."""
        # Act
        result = get_reviews_by_key(self.mock_db, "product_id", 1)
        
        # Assert
        self.assertEqual(len(result), 3)  # 3 reviews for product_id 1
        for review in result:
            self.assertEqual(review["product_id"], 1)
    
    def test_get_reviews_by_key_seller_id(self):
        """Test filtering reviews by seller_id."""
        # Act
        result = get_reviews_by_key(self.mock_db, "seller_id", 2)
        
        # Assert
        self.assertEqual(len(result), 2)  # 2 reviews for seller_id 2
        for review in result:
            self.assertEqual(review["seller_id"], 2)
    
    def test_get_reviews_by_key_no_matches(self):
        """Test filtering reviews with no matches."""
        # Act
        result = get_reviews_by_key(self.mock_db, "product_id", 999)
        
        # Assert
        self.assertEqual(len(result), 0)
    
    def test_calculate_ratings_count(self):
        """Test calculation of ratings count distribution."""
        # Arrange
        reviews = [
            {"rating": 5}, {"rating": 5}, {"rating": 4}, 
            {"rating": 3}, {"rating": 2}
        ]
        
        # Act
        result = calculate_ratings_count(reviews)
        
        # Assert
        expected = {5: 2, 4: 1, 3: 1, 2: 1, 1: 0}
        self.assertEqual(result, expected)
    
    def test_calculate_ratings_count_empty(self):
        """Test calculation of ratings count with empty reviews."""
        # Act
        result = calculate_ratings_count([])
        
        # Assert
        expected = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        self.assertEqual(result, expected)
    
    def test_calculate_average_rating(self):
        """Test calculation of average rating."""
        # Arrange
        reviews = [{"rating": 5}, {"rating": 4}, {"rating": 3}]
        
        # Act
        result = calculate_average_rating(reviews)
        
        # Assert
        self.assertEqual(result, 4.0)
    
    def test_calculate_average_rating_empty(self):
        """Test calculation of average rating with empty reviews."""
        # Act
        result = calculate_average_rating([])
        
        # Assert
        self.assertEqual(result, 0)
    
    def test_calculate_average_rating_single_review(self):
        """Test calculation of average rating with single review."""
        # Arrange
        reviews = [{"rating": 5}]
        
        # Act
        result = calculate_average_rating(reviews)
        
        # Assert
        self.assertEqual(result, 5.0)
    
    @patch('app.services.review_service.get_reviews_by_key')
    def test_generate_general_rating_success(self, mock_get_reviews):
        """Test successful generation of general rating."""
        # Arrange
        mock_reviews = [
            {"rating": 5}, {"rating": 4}, {"rating": 5}, {"rating": 3}
        ]
        mock_get_reviews.return_value = mock_reviews
        
        # Act
        result = generate_general_rating(self.mock_db, "product_id", 1)
        
        # Assert
        self.assertEqual(result.reviews_count, 4)
        self.assertEqual(result.average_rating, 4.25)
        expected_ratings_count = {5: 2, 4: 1, 3: 1, 2: 0, 1: 0}
        self.assertEqual(result.ratings_count, expected_ratings_count)
        mock_get_reviews.assert_called_once_with(self.mock_db, "product_id", 1)
    
    @patch('app.services.review_service.get_reviews_by_key')
    def test_generate_general_rating_no_reviews(self, mock_get_reviews):
        """Test generation of general rating with no reviews."""
        # Arrange
        mock_get_reviews.return_value = []
        
        # Act
        result = generate_general_rating(self.mock_db, "product_id", 999)
        
        # Assert
        self.assertEqual(result.reviews_count, 0)
        self.assertEqual(result.average_rating, 0)
        expected_ratings_count = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        self.assertEqual(result.ratings_count, expected_ratings_count)
        mock_get_reviews.assert_called_once_with(self.mock_db, "product_id", 999)
    
    def test_review_schema_validation(self):
        """Test ReviewSchema validation with valid data."""
        # Arrange
        review_data = {
            "id": 1,
            "product_id": 1,
            "seller_id": 1,
            "buyer": "Carlos Méndez",
            "review": "Excelente cámara y rendimiento, muy satisfecho con la compra.",
            "rating": 5,
            "date": "2024-05-01"
        }
        # Act
        review = ReviewSchema.model_validate(review_data)
        
        # Assert
        self.assertEqual(review.id, 1)
        self.assertEqual(review.product_id, 1)
        self.assertEqual(review.seller_id, 1)
        self.assertEqual(review.buyer, "Carlos Méndez")
        self.assertEqual(review.review, "Excelente cámara y rendimiento, muy satisfecho con la compra.")
        self.assertEqual(review.rating, 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
