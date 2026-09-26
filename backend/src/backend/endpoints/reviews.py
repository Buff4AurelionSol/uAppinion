from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session
from backend.schemas.review import ReviewResponse, ReviewCreate
from backend.services.review_service import create_review_with_book, get_my_library_books, get_my_metrics_books
from backend.config.db import get_db
from datetime import date
from typing import Literal

router = APIRouter()

StatusType = Literal["read", "reading", "plan_to_read", "dropped"]

@router.post("/books/catalog", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_book_review(review_in: ReviewCreate, db: Session = Depends(get_db) ): 
    new_review = create_review_with_book(review_in, db)
    return new_review

@router.get("/books/library")
def get_library_book( 
    page: int = Query(1, ge=1, description="Número de página"), 
    limit: int = Query(10, ge=1, le=100, description="Tamaño de la página"), 
    search: str | None = Query(None, description="Término de búsqueda por título o autor"),
    genre_id: int | None = Query(None, description="ID del género para filtrar"),
    order_by: str | None = Query(None, description="Criterio de ordenamiento (title_asc, date, created_at)"),
    db: Session = Depends(get_db)
): 
    
    my_library_books = get_my_library_books(
        db=db, 
        page=page, 
        limit=limit,
        search=search,
        genre_id=genre_id,
        order_by=order_by
    )
    
    return my_library_books

@router.get("/books/metrics")
def get_metrics_books(
    status: StatusType = Query("read", description="Estado de lectura del libro"),
    year: int | None = Query(None, description="Año específico para filtrar"),
    start_date: date | None = Query(None, description="Fecha de inicio (YYYY-MM-DD)"),
    end_date: date | None = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    db:Session = Depends(get_db),
):
    return get_my_metrics_books(db= db, status=status, year=year, start_date=start_date, end_date=end_date)
    