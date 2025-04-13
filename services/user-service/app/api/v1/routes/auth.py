from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas.user import UserAuthRequest, TokenResponse
from app.db.models.user import User
from app.core.security import hash_password, create_access_token
from app.db.session import get_async_session
from app.core.security import verify_password

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
async def register(user_in: UserAuthRequest, db: AsyncSession = Depends(get_async_session)):
    # Check if user exists
    result = await db.execute(select(User).where(User.email == user_in.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Create new user
    new_user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token(new_user)

    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
async def login(user_in: UserAuthRequest, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    user = result.scalars().first()

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user)

    return TokenResponse(access_token=token)

