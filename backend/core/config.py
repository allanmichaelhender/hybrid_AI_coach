from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from pydantic import PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str 
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore", 
    )

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def make_async_compatible(cls, v: any) -> str:
        if isinstance(v, str):
            # Handle Neon/Heroku style strings
            if v.startswith("postgres://"):
                return v.replace("postgres://", "postgresql+psycopg://", 1)
            # Handle standard Postgres strings missing the driver
            if v.startswith("postgresql://"):
                return v.replace("postgresql://", "postgresql+psycopg://", 1)
        return str(v)

settings = Settings()
