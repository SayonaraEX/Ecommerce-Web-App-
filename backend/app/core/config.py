# backend/app/core/config.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict 

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore") 

settings = Settings()