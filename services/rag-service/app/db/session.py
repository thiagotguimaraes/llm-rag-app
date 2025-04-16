from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker as sync_sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

sync_engine = create_engine(DATABASE_URL, echo=True)
sync_session = sync_sessionmaker(bind=sync_engine)

def get_sync_session():
    with sync_session() as session:
        yield session
        
        
async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session():
    async with async_session() as session:
        yield session
        
        
