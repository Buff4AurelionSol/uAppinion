from fastapi import APIRouter
from backend.endpoints.reviews import router as review_router
from backend.endpoints.genres import router as genres_router
from backend.endpoints.user import router as user_router
from backend.endpoints.auth import router as auth_router
from backend.endpoints.user_book import router as user_book_router

central_router = APIRouter()

## central_router.include_router(review_router, tags=['Reviews'])
central_router.include_router(genres_router, prefix="/genres", tags=['Genres'])
central_router.include_router(user_router, prefix="/user", tags=['Users'])
central_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
central_router.include_router(user_book_router, tags=["User_Books"])
