from typing import Optional
from pydantic import BaseModel, field_validator
from crypto import hash_password


class UserBase(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
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


class GetUserDTO(UserBase):
    id: int
    name: str
    age: int
    username: str
    email: str


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
    workout_type: str | None = None
    duration: int | None = None
    calories: int | None = None
    is_schedule: bool | None = None
    schedule_date: int | None = None


class ExerciseBase(BaseModel):
    workout_id: Optional[int] = None
    name: Optional[str] = None
    exercise_type: Optional[str] = None
    duration: Optional[int] = None
    calories: Optional[int] = None


class CreateExerciseDTO(ExerciseBase):
    workout_id: int
    name: str
    exercise_type: str
    duration: int
    calories: int


class UpdateExerciseDTO(ExerciseBase):
    name: str | None = None
    exercise_type: str | None = None
    duration: int | None = None
    calories: int | None = None


class TrackingBase(BaseModel):
    id: Optional[int] = None
    exercise_id: Optional[int] = None
    duration: Optional[int] = None
    description: Optional[str] = None
    is_new_set: Optional[bool] = False
    is_new_record: Optional[bool] = False
    distance_covered: Optional[int] = None


class CreateTrackingRoomDTO(TrackingBase):
    duration: int
    description: str
