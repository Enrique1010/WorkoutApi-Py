from fastapi import APIRouter, Depends

from dtos import UpdateWorkoutDTO, CreateWorkoutDTO
from repository.auth import get_current_user
from repository.workouts import create_new_workout, update_workout, get_workouts, get_workout, delete_workout
from routers.utils import get_db, AsyncSession

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
async def post(workout_data: CreateWorkoutDTO, db: AsyncSession = Depends(get_db),
               user_id: int = Depends(get_current_user_id)):
    """
    Function to create a new workout.
    Args:
        workout_data:
        user_id:
        db:

    Returns: The new workout info.
    """
    workout_data_dump = workout_data.model_dump()
    return await create_new_workout(workout_data=workout_data_dump, user_id=user_id, db=db)


@router.patch("/{workout_id}", status_code=200)
async def update(workout_data: UpdateWorkoutDTO, db: AsyncSession = Depends(get_db),
                 user_id: int = Depends(get_current_user_id), workout_id: int = None):
    """
    Function to update a workout.
    Args:
        workout_id:
        user_id:
        workout_data:
        db:

    Returns: The updated workout id.
    """
    workout_data_dump = workout_data.model_dump(exclude_unset=True)
    return await update_workout(workout_data=workout_data_dump, user_id=user_id, db=db)


@router.get("/", status_code=200)
async def get(db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """
    Function to get all workouts.
    Args:
        user_id:
        db

    Returns: workout list.
    """
    workout_results = await get_workouts(db=db, user_id=user_id)
    return workout_results


@router.get("/{workout_id}", status_code=200)
async def get(workout_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """
    Function to get a workout.
    Args:
        user_id:
        workout_id:
        db:

    Returns: The specified workout info.
    """
    workout = await get_workout(db=db, workout_id=workout_id, user_id=user_id)
    return workout


@router.delete("/{workout_id}", status_code=200)
async def delete(workout_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """
    Function to delete a workout.
    Args:
        workout_id:
        user_id:
        db:

    Returns: The deleted workout id.
    """
    return await delete_workout(workout_id=workout_id, user_id=user_id, db=db)
