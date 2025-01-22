from typing import Optional, Union
from pydantic import BaseModel, field_validator, ConfigDict
from crypto import hash_password


class UserBase(BaseModel):
    name: Optional[str]
    age: Optional[int]
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    @field_validator('password', mode='before')
    def hash_password(cls, value: Optional[str]) -> Optional[bytes]:
        if value is not None:
            return hash_password(value)
        return value


class CreateUserDTO(UserBase):
    name: str
    age: int
    username: str
    email: str
    password: str


class UpdateUserDTO(UserBase):
    pass
