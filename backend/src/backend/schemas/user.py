from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class CreateUser(BaseModel):
    id: str
    name: str
    email: EmailStr
    lastname: str
    password: str

class ResponseUser(BaseModel):
    id: str
    name: str
    lastname: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)