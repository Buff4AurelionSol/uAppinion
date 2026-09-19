from fastapi import APIRouter
from backend.endpoints.reviews import router as review_router
from backend.endpoints.genres import router as genres_router

central_router = APIRouter()

central_router.include_router(review_router, tags=['Reviews'])
central_router.include_router(genres_router, prefix="/genres", tags=['Genres'])
