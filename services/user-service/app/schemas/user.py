from pydantic import BaseModel, EmailStr

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    tenant_name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
