from pydantic import BaseModel, ConfigDict

class GenreResponse(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)