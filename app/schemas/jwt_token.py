from datetime import datetime

from pydantic import BaseModel

class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class Refresh_token(BaseModel):
    user_id: int
    expires_at: datetime
    refresh_token_hashed: str

    class Config:
        from_attributes = True