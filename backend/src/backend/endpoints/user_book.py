from fastapi import APIRouter, status, Response, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.db import get_db
from backend.schemas.user_book import UserBookWithReview, UserBookUpdate
from backend.services.auth import get_current_user
from backend.services.user_book import create_user_book_with_review, update_user_book, delete_user_book, get_my_library, get_my_metrics, get_my_years_library
from datetime import date
from typing import Literal

StatusType = Literal["read", "reading", "plan_to_read", "dropped"]

router = APIRouter()

@router.get("/books/library")
async def get_library_user(
    current_user: str = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(10, ge=1, description="Tamaño de la página"),
    search: str | None = Query(None, description="Busqueda por autor o título"),
    genre_id: int | None = Query(None, description="ID para filtrar por género"),
    order_by: str | None = Query(None, description="Criterio de ordenamiento"),
    db: AsyncSession = Depends(get_db)

):
    return await get_my_library(
        current_user.id, 
        db, 
        page, 
        limit, 
        search, 
        genre_id, 
        order_by, 
    )

@router.get("/books/metrics")
async def get_my_metrics_user(
    current_user: str = Depends(get_current_user),
    status: StatusType = Query("read", description="Estado de lectura del libro"),
    year: int | None = Query(None, description="Año específico para filtrar"),
    start_date: date | None = Query(None, description="Fecha de inicio (YYYY-MM-DD)"),
    end_date: date | None = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db),
):
    return await get_my_metrics(user_id=current_user.id, db= db, status=status, year=year, start_date=start_date, end_date=end_date)

@router.get("/books/years")
async def get_my_years(
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_my_years_library(user_id=current_user.id, db=db)

@router.post("/books/catalog", status_code=status.HTTP_201_CREATED)
async def create_user_book_and_review(
    payload: UserBookWithReview,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await create_user_book_with_review(payload, current_user.id, db)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error inesperado"
        )

@router.patch("/books/catalog/{user_book_id}")
async def update_userBook(
    user_book_id: str,
    payload: UserBookUpdate,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
): 
    return await update_user_book(current_user.id, user_book_id, payload, db)

@router.delete("/books/library/{user_book_id}")
async def delete_userBook(
    user_book_id: str,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await delete_user_book(current_user.id, user_book_id, db)