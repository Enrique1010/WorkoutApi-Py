"""
test_users.py
This module contains the tests for the users endpoints.
"""
import random

from crypto import generate_random_string
from test_utils import login, get_test_token, Headers

BASE_URL = "api/v1/users"
test_user = {}
header = Headers()


async def test_register_user(test_client):
    """
    Function to test the user registration.
    Args:
        test_client:

    Returns: The test result.
    """
    user_data = {
        "name": f"Jhon {generate_random_string(random.randint(5, 15))}",
        "age": random.randint(20, 50),
        "username": f"jhon_doe_{generate_random_string(random.randint(5, 10))}",
        "email": f"j{generate_random_string(5)}@mail.com",
        "password": "test_password"
    }

    response = await test_client.post(f"{BASE_URL}/register", json=user_data)
    parsed_response = response.json()

    assert response.status_code == 201 or response.status_code == 200
    assert parsed_response["status"] == True
    assert parsed_response["message"] == "User created successfully."
    assert isinstance(parsed_response["data"], int)


async def test_existing_user(test_client):
    """
    Function to test the registration of an existing user.
    Args:
        test_client:

    Returns: The test result.
    """
    user = await login(test_client=test_client, base_url=BASE_URL, user_data=test_user)
    user_id = user["data"]
    header.token = await get_test_token(test_client=test_client, base_url=BASE_URL, user_data=test_user)

    response = await test_client.get(f"{BASE_URL}/{user_id}", headers=header.headers)
    parsed_response = response.json()

    assert response.status_code == 200
    assert parsed_response["id"] == user_id

    bad_response = await test_client.get(f"{BASE_URL}/454543", headers=header.headers)
    assert bad_response.status_code == 404


async def test_update_user(test_client):
    """
    Function to test the user update.
    Args:
        test_client:

    Returns: The test result.
    """
    user = await login(test_client=test_client, base_url=BASE_URL, user_data=test_user)
    user_id = user["data"]
    new_username = generate_random_string(random.randint(5, 10))
    new_user_data = {"username": new_username}
    header.token = await get_test_token(test_client=test_client, base_url=BASE_URL, user_data=test_user)

    response = await test_client.put(f"{BASE_URL}/{user_id}", json=new_user_data, headers=header.headers)
    parsed_response = response.json()

    assert response.status_code == 200
    assert parsed_response["status"] == True
    assert isinstance(parsed_response["data"], int)

    response = await test_client.put(f"{BASE_URL}/{user_id}", json=new_user_data, headers=header.headers)
    assert response.status_code == 409


async def test_get_user(test_client):
    """
    Function to test the user retrieval.
    Args:
        test_client:

    Returns: The test result.
    """
    user = await login(test_client=test_client, base_url=BASE_URL, user_data=test_user)
    user_id = user["data"]
    header.token = await get_test_token(test_client=test_client, base_url=BASE_URL, user_data=test_user)

    response = await test_client.get(f"{BASE_URL}/{user_id}", headers=header.headers)
    parsed_response = response.json()

    assert response.status_code == 200
    assert parsed_response["id"] == user_id

    bad_response = await test_client.get(f"{BASE_URL}/454543", headers=header.headers)
    assert bad_response.status_code == 404
