"""
users.py
Routes are configured for the users endpoints.
"""
from fastapi import APIRouter, Depends
from repository.users import create_new_user
from dtos import CreateUserDTO
from schemas import CreatedResponse
from routers.utils import get_db, AsyncSession

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
