from typing import Optional

from pydantic import BaseModel


class CreatedResponse(BaseModel):
    status: bool
    message: str
    data: int


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
