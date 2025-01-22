"""
utils.py
DB function to get sessions instances.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from db_context import async_session


async def get_db() -> AsyncSession:
    """
    Provides a new database session for the request.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
