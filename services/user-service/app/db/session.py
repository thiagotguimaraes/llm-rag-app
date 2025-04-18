import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
# TODO: Fix database host. When running locally it requires to be 'user-db', 
# but in integration tests and github CI it requires to be 'localhost'
DATABASE_URL = os.getenv("DATABASE_URL")#.replace("localhost", "user-db")

engine = create_engine(DATABASE_URL, echo=True)
sync_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_sync_session():
    with sync_session() as session:
        yield session
