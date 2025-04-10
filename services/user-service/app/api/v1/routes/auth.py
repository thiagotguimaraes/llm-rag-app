from fastapi import APIRouter, HTTPException
from app.schemas.user import UserRegisterRequest, TokenResponse
from app.models.user import fake_users_db, fake_tenants_db, User
from app.core.security import hash_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register(user_in: UserRegisterRequest):
    if user_in.email in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    tenant = user_in.tenant_name.lower()
    if tenant not in fake_tenants_db:
        fake_tenants_db[tenant] = {"id": tenant}

    user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        tenant=tenant
    )
    fake_users_db[user.email] = user

    token = create_access_token({
        "sub": user.email,
        "tenant": user.tenant,
        "role": user.role
    })
    return TokenResponse(access_token=token)
