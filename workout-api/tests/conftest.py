"""
conftest.py
- This file is used to configure the tests for the workout-api
"""
import asyncio
import pytest_asyncio
import sqlalchemy as sa
from httpx import AsyncClient, ASGITransport
from db_context import test_async_session
from app import app
from models import User, Workout
from routers.utils import get_db, AsyncSession

async def replace_db() -> AsyncSession:
    """
    Function to replace the session with the test db session.
    """
    async with test_async_session() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """
    Fixture to create an event loop.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_client():
    """
    Fixture to create a test client. override the db session with the test db session.
    """
    app.dependency_overrides[get_db] = replace_db
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver"
    ) as _test_client:
        yield _test_client


@pytest_asyncio.fixture(name="db", scope="session")
async def db_fixture() -> AsyncSession:
    """
    Fixture to create a test db session.
    """
    async with test_async_session() as session:
        yield session
        await session.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def clean_test_db(db: AsyncSession):
    """
    Fixture to clean the test db before each test run.
    """
    query = sa.delete(User).where(User.id > 1)
    await db.execute(query)
    await db.commit()

    yield
