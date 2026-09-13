from pydantic import BaseModel, ConfigDict

class BookCreate(BaseModel):
    key: str
    title: str
    first_publish_year: int | None = None
    cover_i: int | None  = None

class BookResponse(BookCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)