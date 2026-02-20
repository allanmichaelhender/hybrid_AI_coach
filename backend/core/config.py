from pydantic import PostgresDsn, field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union

class Settings(BaseSettings):
    # 1. BASIC CONFIG
    PROJECT_NAME: str = "Hybrid Hour"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    
    # 2. THE SECRETS (Required, no defaults = safe production)
    DATABASE_URL: str 
    GROQ_API_KEY: str

    # 3. SECURITY
    # Change ["*"] to your React URL (http://localhost:5173) later
    BACKEND_CORS_ORIGINS: List[str] = ["*"] 

    # 4. LOADER CONFIG
    # Pydantic v2 modern settings loader
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8', 
        case_sensitive=True
    )

    # 5. THE ASYNC FIX (Automated)
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def make_async_compatible(cls, v: str) -> str:
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+psycopg://", 1)
        if v.startswith("postgresql://") and "+psycopg" not in v:
            return v.replace("postgresql://", "postgresql+psycopg://", 1)
        return v

settings = Settings()