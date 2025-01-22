"""
auth.py
Handles token creation and verification.
"""
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from schemas import AccessTokenData
from settings import SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/login')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2160 # 1.5 days

def create_access_token(data: dict):
    """
    Function to create a new access token.
    """
    token_data_to_encode = data.copy()
    expiration = \
        datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data_to_encode.update({"exp": expiration})

    encoded_token = jwt.encode(token_data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token


def verify_access_token(access_token, credentials_exception):
    """
    Function to verify the access token.
    """
    try:
        payload = jwt.decode(key=SECRET_KEY, token=access_token, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise credentials_exception
        token_data = AccessTokenData(id=user_id)

    except PyJWTError as error:
        raise credentials_exception from error

    return token_data.id, token_data.role


def get_current_user(access_token: str = Depends(oauth2_scheme)):
    """
    Function to identify the current user.
    """
    credentials_exception = HTTPException(status_code=401,
                                          detail='Could not validate credentials.',
                                          headers={"WWW-Authenticate": "Bearer"})

    user_id, user_role = verify_access_token(access_token,
                                             credentials_exception=credentials_exception)
    return user_id, user_role