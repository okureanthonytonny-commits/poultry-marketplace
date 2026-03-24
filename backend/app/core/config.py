from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    OAUTH_REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    SECRET_KEY: str

    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()
