"""
repository.py
Module to handle all CRUD operations related
to the tasks endpoints.
"""
import sqlalchemy as sa
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import Workout, Exercise
from repository.utils import handle_errors, get_current_time

ERROR_401 = 'You are not authorized to perform this action.'


@handle_errors
async def crud_create_new_workout(workout_data: dict, db: AsyncSession):
    """
    Function to add a new workout into the "workouts" table.

    Returns:
        The new_workout info.
    """
    creation_date = get_current_time()
    schedule_date = workout_data.get('schedule_date')
    workout_data['created_at'] = creation_date
    if schedule_date:
        workout_data['is_schedule'] = True
    else:
        workout_data['is_schedule'] = False
        workout_data['schedule_date'] = creation_date

    new_workout = Workout(**workout_data)

    db.add(new_workout)
    query = sa.select(Workout.id).order_by(Workout.id.desc()).limit(1)
    result = await db.execute(query)
    workout_id = result.scalar()
    await db.commit()
    return {'status': 'success',
            'message': f'Task {workout_id} added successfully.',
            'data': workout_id }


@handle_errors
async def crud_create_new_exercise(exercise_data: dict, db: AsyncSession):
    """
    Function to add a new exercise into the "exercises" table.

    Returns:
        The new_exercise info.
    """
    creation_date = get_current_time()
    exercise_data['created_at'] = creation_date
    new_exercise = Exercise(**exercise_data)

    db.add(new_exercise)
    query = sa.select(Exercise.id).order_by(Exercise.id.desc()).limit(1)
    result = await db.execute(query)
    exercise_id = result.scalar()
    await db.commit()
    return {'status': 'success',
            'message': f'Task {exercise_id} added successfully.',
            'data': exercise_id }


@handle_errors
async def crud_get_workouts(db: AsyncSession):
    """
    Function to get all workouts from the "workouts" table.

    Returns:
        The list of workouts.
    """
    query = sa.select(Workout)
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