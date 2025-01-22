from typing import Optional, Union
from pydantic import BaseModel, field_validator
from crypto import hash_password


class UserBase(BaseModel):
    name: Optional[str]
    age: Optional[int]
    email: Optional[str] = None
    password: Optional[Union[str, bytes]] = None

    @field_validator('password', mode='before')
    def hash_password(cls, value: Optional[str]) -> Optional[bytes]:
        if value is not None:
            return hash_password(value)
        return value


class CreateUserDTO(UserBase):
    name: str
    age: int
    email: str
    password: Union[str, bytes]


class UpdateUserDTO(UserBase):
    pass
