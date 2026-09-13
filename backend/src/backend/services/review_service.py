from backend.schemas.review import ReviewCreate
from backend.models.review import Review
from backend.models.book import Book
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


def create_review_with_book(review_in: ReviewCreate, db: Session) -> Review:
    try:
        db_book = db.query(Book).filter(Book.key == review_in.book.key).first()
        if not db_book:
            db_book = Book(**review_in.book.model_dump())
            db.add(db_book)
            db.flush()

        review_data = review_in.model_dump(exclude={"book"})
        new_review = Review(**review_data, book_id=db_book.key)

        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review
       
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Error de integridad: Es probable que esta reseña (ID duplicado) ya esté registrada."
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error inesperado: {str(e)}"
        )