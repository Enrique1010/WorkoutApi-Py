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


class WorkoutBase(BaseModel):
    user_id: Optional[int] = None
    workout_type: Optional[str] = None
    duration: Optional[int] = None
    calories: Optional[int] = None
    is_schedule: Optional[bool] = False
    schedule_date: Optional[int] = None


class CreateWorkoutDTO(WorkoutBase):
    user_id: int
    workout_type: str
    duration: int
    calories: int


class UpdateWorkoutDTO(WorkoutBase):
    pass