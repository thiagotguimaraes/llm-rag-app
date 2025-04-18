from app.core.security import (create_access_token, hash_password,
                               verify_password)
from app.db.models.user import User
from app.db.session import get_sync_session
from app.schemas.user import TokenResponse, UserAuthRequest
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
def register(
    user_in: UserAuthRequest, db: AsyncSession = Depends(get_sync_session)
):
    # Check if user exists
    existing_user = (
        (db.execute(select(User).where(User.email == user_in.email)))
        .scalars()
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Create new user
    new_user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(new_user)

    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(
    user_in: UserAuthRequest, db: AsyncSession = Depends(get_sync_session)
):
    user = (
        (db.execute(select(User).where(User.email == user_in.email)))
        .scalars()
        .first()
    )

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user)

    return TokenResponse(access_token=token)
