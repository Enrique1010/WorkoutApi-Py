"""
test_workouts.py
This module contains the tests for the workouts endpoints.
"""
import random
import re

from fastapi.testclient import TestClient

from conftest import app
from test_utils import get_test_token, Headers

sync_client = TestClient(app)
BASE_URL = "api/v1/workout"
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
    response = await test_client.post(f"{BASE_URL}/create", json=workout_data, headers=header.headers)
    match = re.search(r'Workout (\d+) added successfully.', response.json()['message'])
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


async def test_get_workouts(test_client):
    """
    Function to test the get workouts endpoint.
    Args:
        test_client:

    Returns: The test result.
    """
    header.token = await get_test_token(test_client, base_url=USER_BASE_URL, user_data=test_user)
    response = await test_client.get(f"{BASE_URL}/", headers=header.headers)

    assert response.status_code == 204

    if response.status_code != 204 and isinstance(response.json(), dict):
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    unauthorized_response = await test_client.get(f"{BASE_URL}/")
    assert unauthorized_response.status_code == 401


async def test_get_workout(test_client):
    """
    Function to test the get workout endpoint.
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

    response = await test_client.get(f"{BASE_URL}/{workout_id}", headers=header.headers)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    bad_response = await test_client.get(f"{BASE_URL}/454543", headers=header.headers)
    assert bad_response.status_code == 204

    unauthorized_response = await test_client.get(f"{BASE_URL}/{workout_id}")
    assert unauthorized_response.status_code == 401


async def test_create_workout(test_client):
    """
    Function to test the create workout endpoint.
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
    response = await test_client.post(f"{BASE_URL}/create", json=workout_data, headers=header.headers)

    assert response.status_code == 201
    assert isinstance(response.json(), dict)

    bad_response = await test_client.post(f"{BASE_URL}/create", json=workout_data)
    assert bad_response.status_code == 401


async def test_update_workout(test_client):
    """
    Function to test the update workout endpoint.
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
    new_workout_data = {
        "duration": 45,
        "calories": 300,
    }
    workout_id = await get_workout_id(test_client, workout_data)

    response = await test_client.patch(f"{BASE_URL}/{workout_id}", json=new_workout_data, headers=header.headers)

    assert response.status_code == 200
    assert "status" in response.json()
    assert "message" in response.json()
    assert isinstance(response.json(), dict)

    bad_response = await test_client.patch(f"{BASE_URL}/{workout_id}", json=new_workout_data)
    assert bad_response.status_code == 401


async def test_delete_workout(test_client):
    """
    Function to test the delete workout endpoint.
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
    response = await test_client.delete(f"{BASE_URL}/{workout_id}", headers=header.headers)

    assert response.status_code == 200
    assert "status" in response.json()
    assert "message" in response.json()

    # test non-existent workout
    bad_response = await test_client.delete(f"{BASE_URL}/454543", headers=header.headers)
    assert bad_response.status_code == 204 or bad_response.status_code == 404

    bad_response = await test_client.delete(f"{BASE_URL}/{workout_id}")
    assert bad_response.status_code == 401
