from fastapi import FastAPI
from app.api.v1.routes import health, auth, protected

app = FastAPI(title="User Service")

app.include_router(health.router, prefix="/api/v1/health")
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(protected.router, prefix="/api/v1/protected")

