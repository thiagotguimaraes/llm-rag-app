from fastapi import FastAPI
from app.api.v1.routes import health, auth

app = FastAPI(title="User Service")

app.include_router(health.router, prefix="/api/v1/health")
app.include_router(auth.router, prefix="/api/v1/auth")

