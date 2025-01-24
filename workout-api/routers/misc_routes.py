"""
misc_routes.py is a file that contains all the miscellaneous routes that are not related to the main routes of the application.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repository.utils import get_schema
from routers.utils import get_db

router = APIRouter()

@router.get("/", status_code=200)
def ping():
    """
    Function to test the API.
    Returns: The test result.
    """
    return {"message": "Welcome to the Workout API"}


@router.get("/schema", status_code=200)
async def get_db_schema(db: AsyncSession = Depends(get_db)):
    """
    Function to get the database schema version.
    Returns: The schema version.
    """
    result = await get_schema(db=db)
    return result