from fastapi import APIRouter, status, Response, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.db import get_db
from backend.schemas.user_book import UserBookWithReview, UserBookUpdate
from backend.services.auth import get_current_user
from backend.services.user_book import create_user_book_with_review, update_user_book

router = APIRouter()


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
    
