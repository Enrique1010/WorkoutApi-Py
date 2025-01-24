import logging
from datetime import datetime
from functools import wraps

from fastapi import HTTPException
from fastapi.websockets import WebSocket
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


def get_current_time():
    """
    Simple function to get a timestamp of current unix time.
    """
    return int(datetime.now().timestamp())


def handle_errors(func):
    """
    Decorator function to maintain generic error handling.
    """

    @wraps(func)
    async def wrapper(*args, db, **kwargs):
        try:
            return await func(*args, db=db, **kwargs)
        except SQLAlchemyError as error:
            logging.error("Data base error has occurred: %s", error, exc_info=True)
            raise HTTPException(
                status_code=500,
                detail='An internal database-related error occurred. Please try again later.'
            ) from error
        except HTTPException:
            # Raise the HTTPExceptions to avoid them for being
            # overwritten by the general Exception block
            raise
        except Exception as error:
            logging.error("An unexpected error occurred: %s", error, exc_info=True)
            raise HTTPException(
                status_code=500,
                detail='An internal server error occurred. Please try again later.'
            ) from error
        finally:
            await db.close()

    return wrapper


@handle_errors
async def get_schema(db: AsyncSession):
    """
    Function to get the current database schema version.
    """
    query = text("SELECT version_num FROM alembic_version;")
    result = await db.execute(query)
    version = result.scalar()
    return version


class WebsocketTrackingHandler:
    """
    Class to handle the websocket tracking.
    """

    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket):
        """
        Function to connect to the websocket.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket):
        """
        Function to disconnect from the websocket.
        """
        await websocket.close()
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_message(data, websocket: WebSocket):
        """
        Function to send a message to the websocket.
        """
        await websocket.send_json(data)

    async def broadcast(self, data):
        """
        Function to broadcast data to all websockets.
        """
        for connection in self.active_connections:
            await connection.send_json(data)


tracking_ws_handler = WebsocketTrackingHandler()
