"""
test_workouts.py
This module contains the tests for the workouts endpoints.
"""
import random
import re
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from conftest import app
from test_utils import get_test_token, Headers

sync_client = TestClient(app)
BASE_URL = "api/v1/exercise"
WORKOUT_BASE_URL = "api/v1/workout"
USER_BASE_URL = "api/v1/users"
header = Headers()
test_user = {}


async def get_workout_id(test_client, workout_data):
    """
    Function to get the workout id.
    Args:
        test_client:
        workout_data:

    Returns: The workout id.
    """
    header.token = await get_test_token(test_client, base_url=USER_BASE_URL, user_data=test_user)
    response = await test_client.post(f"{WORKOUT_BASE_URL}/create", json=workout_data, headers=header.headers)
    match = re.search(r'Workout (\d+) added successfully.', response.json()['message'])
    workout_id = match.group(1)
    return workout_id


async def get_exercise_id(test_client, exercise_data):
    """
    Function to get the workout id.
    Args:
        test_client:
        exercise_data:

    Returns: The workout id.
    """
    header.token = await get_test_token(test_client, base_url=USER_BASE_URL, user_data=test_user)
    response = await test_client.post(f"{BASE_URL}/create", json=exercise_data, headers=header.headers)
    match = re.search(r'Exercise (\d+) added successfully.', response.json()['message'])
    workout_id = match.group(1)
    return workout_id


def test_ping():
    response = sync_client.get("api/v1/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Workout API"}


async def test_db_schema_version(test_client):
    """
    Function to test the database schema version.
    """
    response = await test_client.get("/api/v1/schema")
    assert response.status_code == 200
    assert isinstance(response.json(), str)


async def test_get_exercises(test_client):
    """
    Function to test the get Exercises endpoint.
    Args:
        test_client:

    Returns: The test result.
    """
    header.token = await get_test_token(test_client, base_url=USER_BASE_URL, user_data=test_user)
    workout_data = {
        "user_id": random.randint(1, 100),
        "workout_type": "cardio",
        "duration": 60,
        "calories": 4000,
    }
    workout_id = await get_workout_id(test_client, workout_data)

    response = await test_client.get(f"{BASE_URL}/list/{workout_id}", headers=header.headers)

    if response.status_code != 204 and isinstance(response.json(), dict):
        assert response.status_code == 200
        assert isinstance(response.json()['data'], list)

    unauthorized_response = await test_client.get(f"{BASE_URL}/list/{workout_id}")
    assert unauthorized_response.status_code == 401


async def test_get_exercise(test_client):
    """
    Function to test the get Exercise endpoint.
    Args:
        test_client:

    Returns: The test result.
    """
    header.token = await get_test_token(test_client, base_url=USER_BASE_URL, user_data=test_user)
    workout_data = {
        "user_id": random.randint(1, 100),
        "workout_type": "cardio",
        "duration": 60,
        "calories": 4000,
    }
    workout_id = await get_workout_id(test_client, workout_data)

    exercise_data = {
        "workout_id": workout_id,
        "name": "run 10 miles",
        "exercise_type": "run",
        "duration": 10,
        "calories": 3
    }
    exercise_id = await get_exercise_id(test_client, exercise_data)

    response = await test_client.get(f"{BASE_URL}/{exercise_id}", headers=header.headers)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    bad_response = await test_client.get(f"{BASE_URL}/454543", headers=header.headers)
    assert bad_response.status_code == 404

    unauthorized_response = await test_client.get(f"{BASE_URL}/{workout_id}")
    assert unauthorized_response.status_code == 401


async def test_create_exercise(test_client):
    """
    Function to test the create exercise endpoint.
    Args:
        test_client:
    Returns: The test result.
    """

    header.token = await get_test_token(test_client, base_url=USER_BASE_URL, user_data=test_user)
    workout_data = {
        "user_id": random.randint(1, 100),
        "workout_type": "cardio",
        "duration": 60,
        "calories": 4000,
    }
    workout_id = await get_workout_id(test_client, workout_data)

    exercise_data = {
        "workout_id": workout_id,
        "name": "run 10 miles",
        "exercise_type": "run",
        "duration": 10,
        "calories": 3
    }

    response = await test_client.post(f"{BASE_URL}/create", json=exercise_data, headers=header.headers)

    assert response.status_code == 201
    assert isinstance(response.json(), dict)

    bad_response = await test_client.post(f"{BASE_URL}/create", json=exercise_data)
    assert bad_response.status_code == 401


async def test_update_exercise(test_client):
    """
    Function to test the update exercise endpoint.
    Args:
        test_client:

    Returns: The test result.
    """

    header.token = await get_test_token(test_client, base_url=USER_BASE_URL, user_data=test_user)
    workout_data = {
        "user_id": random.randint(1, 100),
        "workout_type": "cardio",
        "duration": 60,
        "calories": 4000,
    }
    workout_id  = await get_workout_id(test_client, workout_data)

    exercise_data = {
        "workout_id": workout_id,
        "name": "run 10 miles",
        "exercise_type": "run",
        "duration": 10,
        "calories": 3
    }
    exercise_id = await get_exercise_id(test_client, exercise_data)
    new_exercise_data = {
        "exercise_type": "push-up",
        "duration": 10,
        "calories": 300
    }

    response = await test_client.patch(f"{BASE_URL}/{exercise_id}", json=new_exercise_data, headers=header.headers)

    assert response.status_code == 200
    assert "status" in response.json()
    assert "message" in response.json()
    assert isinstance(response.json(), dict)

    bad_response = await test_client.patch(f"{BASE_URL}/{exercise_id}", json=new_exercise_data)
    assert bad_response.status_code == 401


async def test_delete_exercise(test_client):
    """
    Function to test the delete exercise endpoint.
    Args:
        test_client:

    Returns: The test result.
    """

    header.token = await get_test_token(test_client, base_url=USER_BASE_URL, user_data=test_user)
    workout_data = {
        "user_id": random.randint(1, 100),
        "workout_type": "cardio",
        "duration": 60,
        "calories": 4000,
    }
    workout_id = await get_workout_id(test_client, workout_data)

    exercise_data = {
        "workout_id": workout_id,
        "name": "run 10 miles",
        "exercise_type": "run",
        "duration": 10,
        "calories": 3
    }
    exercise_id = await get_exercise_id(test_client, exercise_data)

    response = await test_client.delete(f"{BASE_URL}/{exercise_id}", headers=header.headers)

    assert response.status_code == 200
    assert "status" in response.json()
    assert "message" in response.json()

    # test non-existent workout
    bad_response = await test_client.delete(f"{BASE_URL}/454543", headers=header.headers)
    assert bad_response.status_code == 204 or bad_response.status_code == 404

    bad_response = await test_client.delete(f"{BASE_URL}/{exercise_id}")
    assert bad_response.status_code == 401


async def test_tracking_creation(test_client):
    """
    Function to test the tracking websocket endpoint.
    Args:
        test_client:

    Returns: The test result.
    """
    header.token = await get_test_token(test_client, base_url=USER_BASE_URL, user_data=test_user)
    workout_data = {
        "user_id": random.randint(1, 100),
        "workout_type": "cardio",
        "duration": 60,
        "calories": 4000,
    }
    workout_id = await get_workout_id(test_client, workout_data)

    exercise_data = {
        "workout_id": workout_id,
        "name": "run 10 miles",
        "exercise_type": "run",
        "duration": 10,
        "calories": 3
    }
    exercise_id = await get_exercise_id(test_client, exercise_data)

    tracking_data = {
        "duration": 45,
        "description": "test"
    }

    response = await test_client.post(f"{BASE_URL}/tracking/{exercise_id}", json=tracking_data, headers=header.headers)
    print(response.json())

    assert response.status_code == 201
    assert "status" in response.json()
    assert "message" in response.json()
    assert isinstance(response.json(), dict)


async def test_get_tracking_data_list(test_client):
    """
    Function to test the get tracking data list endpoint.
    Args:
        test_client:

    Returns: The test result.
    """
    header.token = await get_test_token(test_client, base_url=USER_BASE_URL, user_data=test_user)
    workout_data = {
        "user_id": random.randint(1, 100),
        "workout_type": "cardio",
        "duration": 60,
        "calories": 4000,
    }
    workout_id = await get_workout_id(test_client, workout_data)

    exercise_data = {
        "workout_id": workout_id,
        "name": "run 10 miles",
        "exercise_type": "run",
        "duration": 10,
        "calories": 3
    }
    exercise_id = await get_exercise_id(test_client, exercise_data)

    tracking_data = {
        "duration": 45,
        "description": "test"
    }
    await test_client.post(f"{BASE_URL}/tracking/{exercise_id}", json=tracking_data, headers=header.headers)

    response = await test_client.get(f"{BASE_URL}/tracking/list/{exercise_id}", headers=header.headers)

    if response.status_code != 204 and isinstance(response.json(), dict):
        assert response.status_code == 200
        assert isinstance(response.json()['data'], list)

    unauthorized_response = await test_client.get(f"{BASE_URL}/tracking/list/{exercise_id}")
    assert unauthorized_response.status_code == 401


async def test_start_tracking(test_client):
    """
    Function to test the start tracking endpoint.
    Args:
        test_client:

    Returns: The test result.
    """
    header.token = await get_test_token(test_client, base_url=USER_BASE_URL, user_data=test_user)
    workout_data = {
        "user_id": random.randint(1, 100),
        "workout_type": "cardio",
        "duration": 60,
        "calories": 4000,
    }
    workout_id = await get_workout_id(test_client, workout_data)

    exercise_data = {
        "workout_id": workout_id,
        "name": "run 10 miles",
        "exercise_type": "run",
        "duration": 10,
        "calories": 3
    }
    exercise_id = await get_exercise_id(test_client, exercise_data)

    tracking_data = {
        "duration": 45,
        "description": "test"
    }
    response = await test_client.post(f"{BASE_URL}/tracking/{exercise_id}", json=tracking_data, headers=header.headers)
    match = re.search(r'Tracking data (\d+) added successfully.', response.json()['message'])
    tracking_data_id = match.group(1)

    with sync_client.websocket_connect(f"{BASE_URL}/ws/tracking/{tracking_data_id}") as websocket:
        try:
            data = websocket.receive_json()
            assert data['status'] == True
            assert data['message'] == "The tracking has started."
        except WebSocketDisconnect:
            assert True