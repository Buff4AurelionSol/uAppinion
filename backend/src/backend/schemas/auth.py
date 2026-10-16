from pydantic import BaseModel, EmailStr

class AuthenticationRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
