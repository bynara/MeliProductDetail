"""
Mock models for testing
Simple classes that mimic Pydantic models without dependencies
"""

class MockGeneralRating:
    def __init__(self, average_rating=4.5, ratings_count=100, reviews_count=50):
        self.average_rating = average_rating
        self.ratings_count = ratings_count
        self.reviews_count = reviews_count

class MockCategory:
    def __init__(self, id=1, name="Test Category"):
        self.id = id
        self.name = name

class MockPaymentMethod:
    def __init__(self, id=1, name="Credit Card"):
        self.id = id
        self.name = name

class MockProduct:
    def __init__(self, id=1, title="Test Product", description="Test Description", 
                 price=99.99, stock=10, seller_id=1, images=None, 
                 payment_methods_ids=None, category_ids=None, **kwargs):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.stock = stock
        self.seller_id = seller_id
        self.images = images or ["http://example.com/image1.jpg"]
        self.payment_methods_ids = payment_methods_ids or [1, 2]
        self.category_ids = category_ids or [1]
        self.categories = kwargs.get('categories')
        self.payment_methods = kwargs.get('payment_methods')
        self.features = kwargs.get('features')
        self.rating_info = kwargs.get('rating_info')
        self.reviews = kwargs.get('reviews')

class MockReview:
    def __init__(self, id=1, product_id=1, seller_id=1, buyer="Test Buyer", 
                 review="Great product!", rating=5, date="2024-01-01"):
        self.id = id
        self.product_id = product_id
        self.seller_id = seller_id
        self.buyer = buyer
        self.review = review
        self.rating = rating
        self.date = date

class MockSeller:
    def __init__(self, id=1, name="Test Seller", location="Test City", 
                 email="test@example.com", phone="123-456-7890", rating_info=None):
        self.id = id
        self.name = name
        self.location = location
        self.email = email
        self.phone = phone
        self.rating_info = rating_info or MockGeneralRating()

# Factory functions to create instances easily
def create_mock_product(**kwargs):
    return MockProduct(**kwargs)

def create_mock_review(**kwargs):
    return MockReview(**kwargs)

def create_mock_seller(**kwargs):
    return MockSeller(**kwargs)
