from pydantic import BaseModel
from datetime import datetime

class CreateRefreshTokens(BaseModel):
    token_hash: str
    user_id: str
    expires_at: datetime
    user_agent: str | None = None


class LogoutRequest(BaseModel):
    refresh_token: str