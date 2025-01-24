from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import connection_string, test_connection_string

db_engine = create_async_engine(connection_string)
async_session = async_sessionmaker(db_engine, expire_on_commit=False)

test_db_engine = create_async_engine(test_connection_string)
test_async_session = async_sessionmaker(test_db_engine, expire_on_commit=False)
