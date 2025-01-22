"""
users.py
Module to handle all CRUD operations related
to the users endpoints.
"""
import sqlalchemy as sa
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from crypto import verify_password
from dtos import UpdateUserDTO
from models import User
from repository.auth import create_access_token
from repository.utils import handle_errors, get_current_time

ERROR_401 = 'You are not authorized to perform this action.'
ERROR_403 = 'Invalid credentials.'
ERROR_409 = 'That username or email is already in use.'


@handle_errors
async def create_new_user(user_data: dict, db: AsyncSession):
    """
    Function to add a new user into the "users" table.

    Returns:
        The new_user info.
    """
    creation_date = get_current_time()
    user_data['created_at'] = creation_date
    new_user = User(**user_data)

    query = sa.select(User).where((User.email == user_data['username']))
    result = await db.execute(query)
    user_exists = result.scalars().first()
    if user_exists:
        raise HTTPException(status_code=409, detail=ERROR_409)

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(status_code=409, detail=ERROR_409)

    return new_user


@handle_errors
async def user_login(user_credentials: dict, db: AsyncSession):
    """
    Function to authenticate the user.

    Returns:
        A unique token for the user (if auth is successful).
    """
    query = sa.select(User).where(User.username == user_credentials.username)
    result = await db.execute(query)
    user = result.scalar()
    if user is None or not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=403, detail=ERROR_403)

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@handle_errors
async def update_user(user_id: int, requester_id, user_data: UpdateUserDTO, db: AsyncSession):
    """
    Function to update an existing user by ID.

    Returns:
        The updated user info (if successful).
    """
    query = sa.select(User).where(User.id == user_id)
    result = await db.execute(query)
    modified_user = result.scalar()
    if modified_user is None:
        raise HTTPException(status_code=404, detail=f'User with ID {user_id} not found.')
    if modified_user.id != requester_id:
        raise HTTPException(status_code=401, detail=ERROR_401)

    query_all = await db.execute(sa.select(User))
    existing = query_all.scalars().all()
    if any(user_data.email == user.email for user in existing):
        raise HTTPException(status_code=409, detail=ERROR_409)

    if user_data.username is not None:
        modified_user.username = user_data.username
    if user_data.email is not None:
        modified_user.email = user_data.email
    if user_data.password is not None:
        modified_user.password = user_data.password

    await db.commit()
    await db.refresh(modified_user)
    return modified_user


@handle_errors
async def get_user(user_id: int, db: AsyncSession):
    """
    Function to get a user by ID.

    Returns:
        The user info.
    """
    query = sa.select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar()

    if user is None:
        raise HTTPException(status_code=404, detail=f'User with ID {user_id} not found.')

    return user