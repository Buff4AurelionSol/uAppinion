from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from backend.schemas.review import ReviewResponse, ReviewCreate
from backend.services.review_service import create_review_with_book, get_my_library_books
from backend.config.db import get_db


router = APIRouter()

@router.post("/books/catalog", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_book_review(review_in: ReviewCreate, db: Session = Depends(get_db) ): 
    new_review = create_review_with_book(review_in, db)
    return new_review

@router.get("/books/library")
def get_library_book(db: Session = Depends(get_db)): 
    my_library_books = get_my_library_books(db)
    return my_library_books