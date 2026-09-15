from fastapi import FastAPI
from backend.endpoints.reviews import router as review_router
from sqlalchemy import text
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from backend.models.review import Review
from backend.models.book import Book

from backend.config.db import get_db, Base, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=['*'], 
    allow_headers=['*']
)

app.include_router(review_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "API de uAppinnion funcionando"}

