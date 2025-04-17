from app.db.session import engine
from app.api.v1.routes import health, auth, protected
from app.db.base import Base
from fastapi import FastAPI


async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # Lifespan continues after this point


app = FastAPI(title="User Service", lifespan=lifespan)

app.include_router(health.router, prefix="/api/v1/health")
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(protected.router, prefix="/api/v1/protected")
