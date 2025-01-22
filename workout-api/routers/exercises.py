from fastapi import APIRouter, Depends

from dtos import CreateExerciseDTO, UpdateExerciseDTO
from repository.exercise import create_new_exercise, get_exercise, get_exercises, update_exercise, delete_exercise
from routers.utils import get_db, AsyncSession
from repository.auth import get_current_user

router = APIRouter()

async def get_current_user_id(current_user_id: int = Depends(get_current_user)):
    """
    Function to get the current user id.
    Args:
        current_user_id:

    Returns: The current user id.
    """
    return current_user_id


@router.post("/create", status_code=201)
async def post(exercise_data: CreateExerciseDTO, db: AsyncSession = Depends(get_db),
                             user_id: int = Depends(get_current_user_id)):
    """
    Function to create a new exercise.
    Args:
        exercise_data:
        user_id:
        db:

    Returns: The new exercise info.
    """
    exercise_data_dump = exercise_data.model_dump()
    return await create_new_exercise(exercise_data=exercise_data_dump, user_id=user_id, db=db)


@router.put("/update")
async def update(exercise_data: UpdateExerciseDTO, db: AsyncSession = Depends(get_db),
                user_id: int = Depends(get_current_user_id)):
    """
    Function to update an exercise.
    Args:
        user_id:
        exercise_data:
        db:

    Returns: The updated exercise info.
    """
    exercise_data_dump = exercise_data.model_dump()
    return await update_exercise(exercise_data_dump, user_id, db)


@router.get("/")
async def get(db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user_id),
              workout_id: int = None):
    """
    Function to get all exercises.
    Returns: All exercises.
    """
    exercises = await get_exercises(db=db, user_id=user_id, workout_id=workout_id)
    return exercises


@router.get("/{exercise_id}")
async def get(exercise_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """
    Function to get an exercise.
    Args:
        exercise_id:
        db:
        user_id:

    Returns: The exercise info.
    """
    exercise = await get_exercise(db=db, user_id=user_id, exercise_id=exercise_id)
    return exercise


@router.delete("/{exercise_id}")
async def delete(exercise_id: int, db: AsyncSession = Depends(get_db),
                 user_id: int = Depends(get_current_user_id)):
    """
    Function to delete an exercise.
    Args:
        exercise_id:
        db:
        user_id:

    Returns: The deleted exercise info.
    """
    return await delete_exercise(db=db, user_id=user_id, exercise_id=exercise_id)


# websockets operations
@router.websocket("/ws/update_tracking")
async def start_tracking():
    pass