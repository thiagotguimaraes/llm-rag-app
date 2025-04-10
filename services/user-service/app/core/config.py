from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "user-service"
    API_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"
