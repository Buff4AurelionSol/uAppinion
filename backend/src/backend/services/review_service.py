from backend.schemas.review import ReviewCreate
from backend.models.review import Review
from backend.models.book import Book
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
import math


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

def get_my_library_books(db:Session, page: int = 1, limit:int = 10): 

    offset = (page - 1) * limit
    total = db.query(Review).count()

    if(total < 1): return {"reviews": [], "total": 0, "limit": limit, "pages": 0}

    items = (
        db.query(Review)
        .options(joinedload(Review.book))
        .limit(limit)
        .offset(offset)
        .all()
    )

    pages = math.ceil(total/limit)


    return { 
        "reviews": items, 
        "total": total, 
        "limit":limit, 
        "pages": pages
    }
    