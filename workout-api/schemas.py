from pydantic import BaseModel
from typing import Optional

class APIResponse(BaseModel):
    status: bool
    message: str
    data: dict

class APIErrorResponse(BaseModel):
    status: bool
    message: str
    error: str

class AccessToken(BaseModel):
    """
    Model for the access token.
    """
    access_token: str
    token_type: str


class AccessTokenData(BaseModel):
    """
    Model for the data contained within the access token
    """
    id: Optional[int] = None