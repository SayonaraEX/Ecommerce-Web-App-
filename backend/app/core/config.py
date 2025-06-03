# backend/app/core/config.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "b391d1e70e3c5a6f2b8d0c7e9a4f1b6d8c3e7a2f5b9d0c1e7a4f1b6d8c3e7a2f") 


    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
