from fastapi import APIRouter, Depends
from backend.config.db import get_db
from sqlalchemy.orm import Session
from backend.services.genre_service import get_all_genres

router = APIRouter()

@router.get("/")
def all_genres(db: Session = Depends(get_db)):
    return get_all_genres(db)

