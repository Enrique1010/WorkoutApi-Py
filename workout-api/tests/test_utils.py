"""
test_utils.py
helper functions for tests module
"""
import random

from crypto import generate_random_string
from repository.auth import create_access_token


async def create_test_user(test_client, base_url: str):
    """
    Function to create a test user.
    Args:
        test_client:
        base_url:

    Returns: The test user.
    """
    user_data = {
        "name": f"Jhon {generate_random_string(random.randint(5, 15))}",
        "age": random.randint(20, 50),
        "username": generate_random_string(random.randint(5, 10)),
        "email": f"{generate_random_string(random.randint(5, 10))}@mail.com",
        "password": "test_password"
    }
    response = await test_client.post(f"{base_url}/register", json=user_data)
    parsed_response = response.json()
    return parsed_response


async def login(test_client, base_url, user_data):
    """
    Function to test the login.
    Args:
        test_client:
        base_url:
        user_data:

    Returns: The user data.
    """
    if not user_data:
        new_user = await create_test_user(test_client=test_client, base_url=base_url)
        user_data.update(**new_user)

    return user_data


async def get_test_token(test_client, base_url:str, user_data):
    """
    Function to get a test token.
    Args:
        test_client:
        base_url:
        user_data:

    Returns: The test token.
    """
    new_user = await login(test_client=test_client, base_url=base_url, user_data=user_data)
    access_token = create_access_token(data={"user_id": new_user["data"]})

    return access_token


class Headers:
    """
    class to handle custom headers
    """
    def __init__(self):
        self.token = ""

    @property
    def headers(self):
        """
        generate headers based on the token
        """
        return {"Authorization": f"Bearer {self.token}"}