"""
repository.py
Module to handle all CRUD operations related
to the workout endpoints.
"""
import sqlalchemy as sa
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import Workout, Exercise
from repository.utils import handle_errors, get_current_time

ERROR_401 = 'You are not authorized to perform this action.'


@handle_errors
async def create_new_workout(workout_data: dict, user_id: int, db: AsyncSession):
    """
    Function to add a new workout into the "workouts" table.

    Returns:
        The new_workout info.
    """
    creation_date = get_current_time()
    workout_data.update({"created_at": creation_date})
    workout_data.update({"user_id": user_id})
    workout_data.update({"schedule_date": creation_date})

    new_workout = Workout(**workout_data)

    db.add(new_workout)
    query = sa.select(Workout.id).order_by(Workout.id.desc()).limit(1)
    result = await db.execute(query)
    workout_id = result.scalar()
    await db.commit()
    return {'status': 'success',
            'message': f'Workout {workout_id} added successfully.',
            'data': workout_id}


@handle_errors
async def update_workout(workout_data: dict, user_id: int, db: AsyncSession):
    """
    Function to update a workout in the "workouts" table.

    Returns:
        The updated_workout info.
    """
    workout_data.update({"user_id": user_id})
    workout_id = workout_data.get('id')
    query = sa.select(Workout).where(Workout.id == workout_id)
    result = await db.execute(query)
    workout = result.scalar()
    if not workout:
        raise HTTPException(status_code=404, detail='Workout not found.')

    for key, value in workout_data.items():
        setattr(workout, key, value)

    await db.commit()
    return {'status': 'success',
            'message': f'Workout {workout_id} updated successfully.',
            'data': workout_id}


@handle_errors
async def get_workouts(db: AsyncSession, user_id: int):
    """
    Function to get all workouts from the "workouts" table.

    Returns:
        The list of workouts.
    """
    query = sa.select(Workout).where(Workout.user_id == user_id)
    result = await db.execute(query)
    workouts = result.scalars().all()
    if not workouts:
        raise HTTPException(status_code=204, detail='No workouts found.')
    mapped_workouts = [
        {
            "id": workout.id,
            "user_id": workout.user_id,
            "workout_type": workout.workout_type,
            "duration": workout.duration,
            "calories": workout.calories,
            "created_at": workout.created_at,
            "is_schedule": workout.is_schedule,
            "schedule_date": workout.schedule_date
        }
        for workout in workouts
    ]
    return mapped_workouts


@handle_errors
async def get_workout(db: AsyncSession, workout_id: int, user_id: int):
    """
    Function to get all workouts with exercises from the "workouts" table.

    Returns:
        The list of workouts with exercises.
    """
    query = (
        sa.select(Workout)
        .options(joinedload(Workout.exercises))  # Eager load the exercises relationship
        .where(Workout.id == workout_id)
        .where(Workout.user_id == user_id)
    )

    result = await db.execute(query)
    workout = result.scalars().first()

    if not workout:
        raise HTTPException(status_code=204, detail='No workouts found.')

    mapped_workout = {
        "id": workout.id,
        "user_id": workout.user_id,
        "workout_type": workout.workout_type,
        "duration": workout.duration,
        "calories": workout.calories,
        "created_at": workout.created_at,
        "is_schedule": workout.is_schedule,
        "schedule_date": workout.schedule_date,
        "exercises": [
            {
                "id": exercise.id,
                "name": exercise.name,
                "exercise_type": exercise.exercise_type,
                "duration": exercise.duration,
                "calories": exercise.calories,
                "created_at": exercise.created_at
            }
            for exercise in workout.exercises
        ]
    }

    return mapped_workout
