from pydantic_settings import BaseSettings, SettingsConfigDict

# Inheriting from BaseSettings, pydantic knows to look for our environmental variables
class Settings(BaseSettings):
    # Our settings variables
    PROJECT_NAME: str = "Hybrid Hour"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    
    DATABASE_URL: str 
    GROQ_API_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  
    ALGORITHM: str = "HS256"
    
    # Letting the settings class know where to get the .env variables
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8', 
        case_sensitive=True
    )

# Creates a settings object and pulls in the env variables
settings = Settings()