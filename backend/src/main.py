from fastapi import FastAPI
from backend.endpoints.reviews import router as review_router
from sqlalchemy import text
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from backend.models.review import Review
from backend.models.book import Book

from backend.config.db import get_db, Base, engine

app = FastAPI()

app.include_router(review_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "API de uAppinnion funcionando"}

