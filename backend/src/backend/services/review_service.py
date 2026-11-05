from backend.schemas.review import ReviewCreate
from backend.models.review import Review
from sqlalchemy.ext.asyncio import AsyncSession

async def create_review(reviewData: ReviewCreate, db: AsyncSession):
    newReview = Review(
        id=reviewData.id,
        user_book_id=reviewData.user_book_id,
        text_review=reviewData.text_review
    )

    db.add(newReview)
    return newReview


    