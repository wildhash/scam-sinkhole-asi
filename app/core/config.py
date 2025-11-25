from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # AGI API Configuration
    agi_api_key: str = ""
    agi_api_base_url: str = "https://api.openai.com/v1"
    
    # Telnyx Configuration
    telnyx_api_key: str = ""
    telnyx_phone_number: str = ""
    
    # Application Configuration
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = False
    
    # Reporting Configuration
    report_webhook_url: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
