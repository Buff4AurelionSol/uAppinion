from pydantic import BaseModel, ConfigDict
from backend.schemas.genre import GenreResponse

class BookCreate(BaseModel):
    key: str
    title: str
    first_publish_year: int | None = None
    cover_i: int | None  = None
    genres: list[str] = []

class BookResponse(BookCreate):
    genres: list[GenreResponse]
    model_config = ConfigDict(from_attributes=True)