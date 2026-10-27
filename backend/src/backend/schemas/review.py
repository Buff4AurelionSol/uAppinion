from datetime import date
from pydantic import BaseModel, ConfigDict
from backend.schemas.book import BookCreate, BookResponse

class ReviewCreate(BaseModel):
    id: str
    book_id: str
    text_review: str | None = None


class ReviewResponse(BaseModel):
    id: str
    text_review: str | None = None

    model_config = ConfigDict(from_attributes=True)

