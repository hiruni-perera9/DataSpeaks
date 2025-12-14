# Application configuration management using Pydantic Settings

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Application settings loaded from environment variables

    # Database
    database_url: str = "sqlite:///./customer_data.db"

    # API Keys
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    google_api_key: str = ""

    # App
    app_name: str = "DataSpeaks"
    debug: bool = True
    log_level: str = "INFO"

    # Security
    secret_key: str = "change_this_in_production"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    # Cached settings instance
    # Only loading settings once to improve performance

    return Settings()

settings = get_settings()



    
