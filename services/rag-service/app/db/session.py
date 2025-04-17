import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker as sync_sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")

sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)
sync_session = sync_sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


@contextmanager
def get_sync_session():
    """Provide a transactional scope around a series of operations."""
    session = sync_session()
    try:
        yield session
    finally:
        session.close()


async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session():
    async with async_session() as session:
        yield session
