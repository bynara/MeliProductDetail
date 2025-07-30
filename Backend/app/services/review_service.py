from collections import Counter
from ..schemas.general_rating import GeneralRating
from ..repository import get_all, get_item_by_id
from ..schemas.review import ReviewSchema
from ..core.logger import logger

def list_reviews(db: dict) -> list[ReviewSchema]:
    logger.info("Starting to list all reviews")
    try:
        reviews = [ReviewSchema.model_validate(obj) for obj in get_all(db, "reviews")]
        logger.info(f"Successfully retrieved {len(reviews)} reviews")
        return reviews
    except Exception as e:
        logger.error(f"Error listing reviews: {e}")
        raise

def get_review_by_id(db: dict, review_id: int) -> ReviewSchema:
    logger.info(f"Getting review by id: {review_id}")
    try:
        review = ReviewSchema.model_validate(get_item_by_id(db, "reviews", review_id))
        logger.info(f"Successfully retrieved review with id: {review_id}")
        return review
    except Exception as e:
        logger.error(f"Error getting review by id {review_id}: {e}")
        raise

def get_reviews_by_key(db: dict, key: str, id: int) -> list[dict]:
    logger.debug(f"Getting reviews by {key}: {id}")
    try:
        filtered_reviews = [r for r in db["reviews"] if r[key] == id]
        logger.debug(f"Found {len(filtered_reviews)} reviews for {key}: {id}")
        return filtered_reviews
    except Exception as e:
        logger.error(f"Error getting reviews by {key} {id}: {e}")
        raise

def calculate_ratings_count(reviews: list[dict]) -> dict:
    """Return a dict with the count of each rating (1-5)."""
    logger.debug(f"Calculating ratings count for {len(reviews)} reviews")
    try:
        ratings_counter = Counter(r["rating"] for r in reviews)
        ratings_count = {i: ratings_counter.get(i, 0) for i in range(5, 0, -1)}
        logger.debug(f"Ratings count calculated: {ratings_count}")
        return ratings_count
    except Exception as e:
        logger.error(f"Error calculating ratings count: {e}")
        raise

def calculate_average_rating(reviews: list[dict]) -> float:
    """Return the average rating for the given reviews."""
    logger.debug(f"Calculating average rating for {len(reviews)} reviews")
    try:
        total_reviews = len(reviews)
        total_score = sum(r["rating"] for r in reviews)
        avg_rating = round(total_score / total_reviews, 2) if total_reviews > 0 else 0
        logger.debug(f"Average rating calculated: {avg_rating}")
        return avg_rating
    except Exception as e:
        logger.error(f"Error calculating average rating: {e}")
        raise

def generate_general_rating(db: dict, key: str, id: int) -> GeneralRating:
    logger.info(f"Generating general rating for {key}: {id}")
    try:
        filtered_reviews = get_reviews_by_key(db, key, id)
        ratings_count = calculate_ratings_count(filtered_reviews)
        avg_rating = calculate_average_rating(filtered_reviews)
        total_reviews = len(filtered_reviews)

        general_rating = GeneralRating(
            reviews_count=total_reviews,
            ratings_count=ratings_count,
            average_rating=avg_rating
        )
        logger.info(f"Successfully generated general rating for {key}: {id} - {total_reviews} reviews, avg: {avg_rating}")
        return general_rating
    except Exception as e:
        logger.error(f"Error generating general rating for {key} {id}: {e}")
        raise