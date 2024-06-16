import asyncio
from typing import AsyncGenerator, Generator, Any
import asyncpg

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker



from backend.auth.security import create_access_token
from backend.database import get_db, Base
from config import DB_NAME_TEST, DB_PORT_TEST, DB_USER, DB_PASSWORD, DB_HOST_TEST

from backend.main_app import app

DATABASE_URL_TEST = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'




engine_test = create_async_engine(DATABASE_URL_TEST, future=True, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
  async with async_session_maker() as session:
    yield session

app.dependency_overrides[get_db] = override_get_async_session


@pytest.fixture(scope='session', autouse=True)
async def prepare_db():
  async with engine_test.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
  yield

  async with engine_test.begin() as conn:
    await conn.run_sync(Base.metadata.drop_all)
    # conn.close()


@pytest.fixture(scope='session')
def get_event_loop():
  loop = asyncio.get_event_loop_policy().new_event_loop()
  yield loop
  loop.close()



@pytest.fixture
async def ac() -> AsyncGenerator[AsyncClient, None]:
  async with AsyncClient(app=app, base_url='http://test') as ac:
    yield ac














# @pytest.fixture(scope='session')
# async def async_session_test():
#   engine = create_async_engine(DATABASE_URL_TEST, future=True, echo=True)
#   test_async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
#   yield test_async_session
  
  
# @pytest.fixture(scope='function', autouse=True)
# async def clean_tables(async_session_test):
#   async with async_session_test() as session:
#     async with session.begin():
#       for table_clean in CLEAN_TABLES:
#         await session.execute(f"""TRUNCATE TABLE {table_clean};""")


# @pytest.fixture(scope='function')
# async def client() -> Generator[TestClient, Any, None]:
#   async def _get_test_db():
#     try:
#       yield test_async_session()
#     finally:
#       pass
    
#   app.dependency_overrides[get_db] = _get_test_db
#   with TestClient(app) as client:
#     yield client
    
# @pytest.fixture(scope='session')
# async def asyncpg_pool():
#   pool = await asyncpg.create_pool(''.join(DATABASE_URL_TEST.split('+asyncpg')))
#   yield pool
#   pool.close()
      
# @pytest.fixture
# async def get_group_collection_from_database(asyncpg_pool):
#   async def get_group_collection_by_id(group_id: int):
#     async with asyncpg_pool.acquire() as connection:
#       return await connection.fetch("""SELECT * FROM group_collection WHERE id = $1;""", group_id)
    
#     return get_group_collection_by_id