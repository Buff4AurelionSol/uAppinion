from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from backend.schemas.book import BookResponse, BookCreate
from backend.schemas.review import ReviewResponse, ReviewCreate

class UserBookCreate(BaseModel):
    id: str
    book_id: str
    status: str
    num_pages: int | None = None
    start_date: date | None = None
    finish_date: date | None = None

    model_config = ConfigDict(from_attributes=True)

class UserBookWithReview(BaseModel):
    id: str
    status: str
    num_pages: int | None = None
    start_date: date | None = None
    finish_date: date | None = None

    book: BookCreate
    review: ReviewCreate | None = None

    model_config = ConfigDict(from_attributes=True)


class UserBookUpdate(BaseModel):
    status: str | None = None
    num_pages: int | None = None
    start_date: date | None = None
    finish_date: date | None = None 


class ResponseUserBook(UserBookCreate):
    created_at: datetime | None = None
    updated_at: datetime | None = None

    book: BookResponse
    review: ReviewResponse | None = None

    model_config = ConfigDict(from_attributes=True)
    