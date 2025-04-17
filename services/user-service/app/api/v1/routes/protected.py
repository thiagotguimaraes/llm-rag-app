from app.core.security import get_current_user, require_role
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/me")
def read_my_profile(user=Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "role": user.role}


@router.get("/admin-only")
def admin_endpoint(user=Depends(require_role("admin"))):
    return {"message": f"Hello Admin {user.email}"}
