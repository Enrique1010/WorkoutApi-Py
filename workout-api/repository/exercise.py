"""
repository.py
Module to handle all CRUD operations related
to the exercise and exercise tracking data endpoints.
"""
import sqlalchemy as sa
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import Exercise, Workout, TrackingData, MapPoint
from repository.utils import handle_errors, get_current_time

ERROR_401 = 'You are not authorized to perform this action.'

async def verify_user_id(user_id: int, workout_id: int, db: AsyncSession):
    """
    Function to verify the user_id of the exercise.

    Returns:
        The user_id of the exercise.
    """

    workout_query = sa.select(Workout).where(Workout.id == workout_id)
    workout_result = await db.execute(workout_query)
    retrieved_workout = workout_result.scalar()

    if not retrieved_workout:
        raise HTTPException(status_code=404, detail='Workout related to this exercise/tracking not found.')

    if retrieved_workout.user_id != user_id:
        raise HTTPException(status_code=401, detail=ERROR_401)


async def verify_if_exercise_exists(exercise_id: int, db: AsyncSession):
    """
    Function to verify if the exercise exists.

    Returns:
        The exercise info.
    """
    query = sa.select(Exercise).where(Exercise.id == exercise_id)
    result = await db.execute(query)
    exercise = result.scalar()
    if not exercise:
        raise HTTPException(status_code=404, detail='Exercise not found.')
    return exercise.workout_id


@handle_errors
async def create_new_exercise(exercise_data: dict, user_id: int, db: AsyncSession):
    """
    Function to add a new exercise into the "exercise" table.

    Returns:
        The new_exercise info.
    """
    # compare workout user_id with the current user_id
    workout_id = exercise_data['workout_id']
    await verify_user_id(user_id, workout_id, db)

    creation_date = get_current_time()
    exercise_data.update({"created_at": creation_date})
    exercise_data.update({"workout_id": workout_id})

    new_exercise = Exercise(**exercise_data)

    db.add(new_exercise)
    query = sa.select(Exercise.id).order_by(Exercise.id.desc()).limit(1)
    result = await db.execute(query)
    exercise_id = result.scalar()
    await db.commit()

    return {'status': 'success',
            'message': f'Exercise {exercise_id} added successfully.'}


@handle_errors
async def update_exercise(exercise_id: int, exercise_data: dict, user_id: int, db: AsyncSession):
    """
    Function to update an exercise in the "exercise" table.

    Returns:
        Success message.
    """
    query = sa.select(Exercise).where(Exercise.id == exercise_id)
    result = await db.execute(query)
    exercise = result.scalar()

    if not exercise:
        raise HTTPException(status_code=404, detail='Exercise not found.')

    await verify_user_id(user_id, exercise.workout_id, db)

    update_query = sa.update(Exercise).where(Exercise.id == exercise_id).values(**exercise_data)
    await db.execute(update_query)
    await db.commit()

    return {'status': 'success',
            'message': f'Exercise {exercise_id} updated successfully.'}


@handle_errors
async def get_exercises(db: AsyncSession, user_id: int, workout_id: int):
    """
    Function to get all exercises from the "exercise" table.

    Returns:
        All exercises.
    """
    await verify_user_id(user_id, workout_id, db)

    query = sa.select(Exercise).where(Exercise.workout_id == workout_id)
    result = await db.execute(query)
    exercises = result.scalars().all()

    return {
        'status': 'success',
        'data': exercises
    }


@handle_errors
async def get_exercise(db: AsyncSession, user_id: int, exercise_id: int):
    """
    Function to get an exercise from the "exercise" table.

    Returns:
        The exercise info.
    """

    query = sa.select(Exercise).where(Exercise.id == exercise_id)
    result = await db.execute(query)
    exercise = result.scalar()

    if not exercise:
        raise HTTPException(status_code=404, detail='Exercise not found.')

    await verify_user_id(user_id, exercise.workout_id, db)

    return {
        'status': 'success',
        'data': exercise
    }

@handle_errors
async def delete_exercise(db: AsyncSession, user_id: int, exercise_id: int):
    """
    Function to delete an exercise from the "exercise" table.

    Returns:
        The deleted exercise info.
    """
    query = sa.select(Exercise).where(Exercise.id == exercise_id)
    result = await db.execute(query)
    exercise_to_delete = result.scalar()

    if not exercise_to_delete:
        raise HTTPException(status_code=404, detail='Exercise not found.')

    await verify_user_id(user_id, exercise_to_delete.workout_id, db)

    await db.delete(exercise_to_delete)
    await db.commit()

    return {'status': 'success',
            'message': f'Exercise with {exercise_id} deleted successfully.'}


@handle_errors
async def create_exercise_tracking_data_room(db: AsyncSession, user_id: int, exercise_id: int, tracking_data: dict):
    """
    Function to create a new exercise tracking data room in the "tracking_data" table.

    Returns:
        The new tracking_data info.
    """
    workout_id = await verify_if_exercise_exists(exercise_id, db)

    await verify_user_id(user_id, workout_id, db)

    creation_date = get_current_time()
    tracking_data.update({"created_at": creation_date})
    tracking_data.update({"exercise_id": exercise_id})

    new_tracking_data = TrackingData(**tracking_data)

    db.add(new_tracking_data)
    query = sa.select(TrackingData.id).order_by(TrackingData.id.desc()).limit(1)
    result = await db.execute(query)
    tracking_data_id = result.scalar()
    await db.commit()
    return {'status': 'success',
            'message': f'Tracking data {tracking_data_id} added successfully.',
            'data': tracking_data_id }


@handle_errors
async def get_exercise_tracking_data_list(db: AsyncSession, user_id: int, exercise_id: int):
    """
    Function to get all exercise tracking data from the "tracking_data" table.

    Returns:
        The list of tracking_data.
    """
    query = sa.select(TrackingData).where(TrackingData.exercise_id == exercise_id)
    result = await db.execute(query)
    tracking_data = result.scalars().all()

    if not tracking_data:
        raise HTTPException(status_code=404, detail='Tracking data not found.')

    workout_id = await verify_if_exercise_exists(exercise_id, db)

    await verify_user_id(user_id, workout_id, db)

    return tracking_data


@handle_errors
async def get_exercise_tracking_data_updates(db: AsyncSession, user_id: int, tracking_data_id: int):
    """
    Function to get an exercise tracking data from the "tracking_data" table.

    Returns:
        The tracking_data info.
    """
    query = (
        sa.select(TrackingData)
        .options(joinedload(TrackingData.route))
        .where(TrackingData.id == tracking_data_id)
    )
    result = await db.execute(query)
    tracking_data = result.scalar()

    if not tracking_data:
        raise HTTPException(status_code=404, detail='Tracking data not found.')

    workout_id = await verify_if_exercise_exists(tracking_data.exercise_id, db)

    await verify_user_id(user_id, workout_id, db)

    mapped_tracking_data = {
        "id": tracking_data.id,
        "description": tracking_data.description,
        "user_id": tracking_data.user_id,
        "exercise_id": tracking_data.exercise_id,
        "duration": tracking_data.duration,
        "is_new_set": tracking_data.is_new_set,
        "is_new_record": tracking_data.is_new_record,
        "distance_covered": tracking_data.distance_covered,
        "created_at": tracking_data.created_at,
        "last_updated_at": tracking_data.last_updated_at,
        "route": [
            {
                "id": map_point.id,
                "latitude": map_point.lat,
                "longitude": map_point.lon,
                "tracking_data_id": map_point.tracking_data_id,
            }
            for map_point in tracking_data.route
        ],
    }

    return mapped_tracking_data


@handle_errors
async def update_exercise_tracking_data(db: AsyncSession, user_id: int, tracking_data_id: int,
                                        tracking_data: dict, map_point: dict):
    """
    Function to update an exercise tracking data in the "tracking_data" table.

    Returns:
        The updated tracking_data info.
    """
    global map_point_id
    query = sa.select(TrackingData).where(TrackingData.id == tracking_data_id)
    result = await db.execute(query)
    existing_tracking_data = result.scalar()

    if not existing_tracking_data:
        raise HTTPException(status_code=404, detail='Tracking data not found.')

    workout_id = await verify_if_exercise_exists(existing_tracking_data.exercise_id, db)

    await verify_user_id(user_id, workout_id, db)

    map_point.update({"tracking_data_id": tracking_data_id})

    new_map_point = MapPoint(**map_point)

    if map_point:
        db.add(new_map_point)
        query = sa.select(MapPoint.id).order_by(MapPoint.id.desc()).limit(1)
        result = await db.execute(query)
        map_point_id = result.scalar()


    update_query = sa.update(TrackingData).where(TrackingData.id == tracking_data_id).values(**tracking_data)
    await db.execute(update_query)
    await db.commit()

    if map_point:
        return { 'status': 'success',
                 'message': f'Tracking data {tracking_data_id} with location {map_point_id} updated successfully.'}
    else:
        return {'status': 'success',
            'message': f'Tracking data {tracking_data_id} updated successfully.' }

