from pydantic import BaseModel, ConfigDict

class AuthorCreate(BaseModel):
    name: str

class AuthorResponse(AuthorCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)