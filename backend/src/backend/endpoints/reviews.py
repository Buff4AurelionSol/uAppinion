from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session
from backend.schemas.review import ReviewResponse, ReviewCreate
from backend.services.review_service import create_review_with_book, get_my_library_books
from backend.config.db import get_db


router = APIRouter()

@router.post("/catalog", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_book_review(review_in: ReviewCreate, db: Session = Depends(get_db) ): 
    new_review = create_review_with_book(review_in, db)
    return new_review

@router.get("/library")
def get_library_book( page: int = Query(1, ge=1, description="Número de página"), limit: int = Query(1, ge=1, le=100, description="Tamaño de la página"),  db: Session = Depends(get_db)): 
    my_library_books = get_my_library_books(db, page, limit)
    return my_library_books