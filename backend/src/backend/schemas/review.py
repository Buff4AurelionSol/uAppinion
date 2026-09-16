from datetime import date
from pydantic import BaseModel, ConfigDict
from backend.schemas.book import BookCreate, BookResponse

class ReviewCreate(BaseModel):
    id: str
    status: str
    num_pages: int | None = None
    start_date: date | None = None
    finish_date: date | None = None
    is_read: bool = False
    text_review: str | None = None
    book: BookCreate

class ReviewResponse(BaseModel):
    id: str
    status: str
    num_pages: int | None = None
    start_date: date | None = None
    finish_date: date | None = None
    is_read: bool = False
    text_review: str | None = None
    book: BookResponse

    model_config = ConfigDict(from_attributes=True)

