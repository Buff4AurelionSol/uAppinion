from pydantic import BaseModel, ConfigDict
from backend.schemas.genre import GenreResponse
from backend.schemas.author import AuthorResponse

class BookBase(BaseModel):
    key: str
    title: str
    first_publish_year: int | None = None
    cover_i: int | None  = None
 


class BookCreate(BookBase):
    genres: list[str] = []
    authors: list[str] = []

class BookResponse(BookBase):
    genres: list[GenreResponse]
    authors: list[AuthorResponse]

    model_config = ConfigDict(from_attributes=True)