import logging

from datetime import datetime
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException


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
            logging.error("SQLAlchemyError occurred: %s", error, exc_info=True)
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
