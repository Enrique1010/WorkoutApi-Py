from fastapi import APIRouter, Depends
from fastapi.websockets import WebSocketDisconnect, WebSocket

from dtos import CreateExerciseDTO, UpdateExerciseDTO, CreateTrackingRoomDTO
from repository.auth import get_current_user
from repository.exercise import create_new_exercise, get_exercise, get_exercises, update_exercise, delete_exercise, \
    get_exercise_tracking_data_list, create_exercise_tracking_data_room, update_exercise_tracking_data, \
    create_map_point, get_exercise_tracking_data_updates
from repository.utils import tracking_ws_handler
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


@router.patch("/{exercise_id}", status_code=200)
async def update(exercise_data: UpdateExerciseDTO, db: AsyncSession = Depends(get_db),
                 user_id: int = Depends(get_current_user_id), exercise_id: int = None):
    """
    Function to update an exercise.
    Args:
        exercise_id:
        user_id:
        exercise_data:
        db:

    Returns: The updated exercise info.
    """
    exercise_data_dump = exercise_data.model_dump(exclude_unset=True)
    return await update_exercise(exercise_data=exercise_data_dump, exercise_id=exercise_id, user_id=user_id, db=db)


@router.get("/list/{workout_id}", status_code=200)
async def get(db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user_id),
              workout_id: int = None):
    """
    Function to get all exercises.
    Returns: List of exercises.
    """
    exercises = await get_exercises(db=db, user_id=user_id, workout_id=workout_id)
    return exercises


@router.get("/{exercise_id}", status_code=200)
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


@router.delete("/{exercise_id}", status_code=200)
async def delete(exercise_id: int, db: AsyncSession = Depends(get_db),
                 user_id: int = Depends(get_current_user_id)):
    """
    Function to delete an exercise.
    Args:
        exercise_id:
        db:
        user_id:

    Returns: The deleted exercise id.
    """
    return await delete_exercise(db=db, user_id=user_id, exercise_id=exercise_id)


"""
Websockets operations and tracking endpoints
"""


@router.post("/tracking/{exercise_id}", status_code=201)
async def post_tracking(tracking_data: CreateTrackingRoomDTO, exercise_id: int, db: AsyncSession = Depends(get_db),
                        user_id: int = Depends(get_current_user_id)):
    """
    Function to create a new exercise tracking.
    Args:
        tracking_data:
        exercise_id:
        db:
        user_id:

    Returns: The new exercise tracking id.

    """
    tracking_data_dump = tracking_data.model_dump()
    return await create_exercise_tracking_data_room(exercise_id=exercise_id, user_id=user_id,
                                                    tracking_data=tracking_data_dump, db=db)


@router.get("/tracking/list/{exercise_id}", status_code=200)
async def get_tracking(exercise_id: int, db: AsyncSession = Depends(get_db),
                       user_id: int = Depends(get_current_user_id)):
    """
    Function to get all exercise tracking.
    Args:
        exercise_id:
        db:
        user_id:

    Returns: List of exercise tracking data.

    """
    return await get_exercise_tracking_data_list(db=db, user_id=user_id, exercise_id=exercise_id)


# websockets operations
@router.websocket("/ws/tracking/{tracking_data_id}")
async def start_tracking(websocket: WebSocket, tracking_data_id: int, db: AsyncSession = Depends(get_db)):
    """
    Function to start the tracking of an exercise using websockets if the tracking room exists (or if needed).
    Args:
        tracking_data_id:
        websocket:
        db:

    Returns: The tracking status.

    """

    websocket_handler = tracking_ws_handler
    await websocket_handler.connect(websocket=websocket)
    await websocket_handler.broadcast({"status": True, "message": "The tracking has started."})

    try:
        while True:
            data = await websocket.receive_json()
            # this is the data that the client sends to the server every time the user moves
            response = await create_map_point(map_point=data['map_point'], tracking_data_id=tracking_data_id, db=db)

            if data['update_tracking_data'] is True:
                # if the user wants to update the tracking data every x seconds
                update_response = await update_exercise_tracking_data(data=data['updated_tracking_data'],
                                                                      tracking_data_id=response['data'], db=db)
            else:
                update_response = None

            if update_response['status']:
                await websocket_handler.broadcast({"status": True, "message": "The tracking data has been updated."})
                tracking_updates = await get_exercise_tracking_data_updates(tracking_data_id=response['data'], db=db)
                await websocket_handler.broadcast(tracking_updates)
            else:
                await websocket_handler.broadcast(
                    {"status": False, "message": "The tracking data has not been updated."})

    except WebSocketDisconnect:
        await websocket_handler.broadcast({"status": False, "message": "The tracking has stopped."})
        await websocket_handler.disconnect(websocket=websocket)
        return {"status": True, "message": "The tracking has stopped."}
