"""
users.py
Routes are configured for the users endpoints.
"""
from fastapi import APIRouter, Depends

from dtos import CreateUserDTO, UpdateUserDTO, GetUserDTO
from repository.users import create_new_user, update_user, get_user
from routers.utils import get_db, AsyncSession
from schemas import CreatedResponse

router = APIRouter()


@router.post("/register", response_model=CreatedResponse)
async def post(user: CreateUserDTO, db: AsyncSession = Depends(get_db)):
    """
    Endpoint to register a new user.

    Returns:
       Returns info about the newly created user.
    """
    user_data = user.model_dump()
    new_user = await create_new_user(user_data=user_data, db=db)
    result = CreatedResponse(status=True, message="User created successfully.", data=new_user.id)
    return result


@router.put("/{user_id}", response_model=CreatedResponse)
async def update(user_data: UpdateUserDTO, db: AsyncSession = Depends(get_db), user_id: int = None):
    """
    Endpoint to update a user.

    Returns:
        The updated user info.
    """
    updated_user = await update_user(user_data=user_data, user_id=user_id, requester_id=user_id, db=db)
    result = CreatedResponse(status=True, message="User updated successfully.", data=updated_user.id)
    return result


@router.get("/{user_id}", response_model=GetUserDTO)
async def get(user_id: int = None, db: AsyncSession = Depends(get_db)):
    """
    Endpoint to get a user.

    Returns:
        The user info.
    """
    user = await get_user(user_id=user_id, db=db)
    result = GetUserDTO(id=user.id, name=user.name, username=user.username, age=user.age, email=user.email)
    return result
