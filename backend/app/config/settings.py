from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), env_file_encoding="utf-8", extra="ignore")

    # APPLICATION
    app_name: str = "ZTP Assistant API"
    app_version: str = "0.1.0"
    app_env: Literal["development", "staging", "production"] = "development"
    app_debug: bool = False
    app_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:3000"
    log_level: str = "INFO"
    
    api_v1_prefix: str = "/api/v1"
    
    # DATABASE
    database_url: str
    
    # JWT
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    
    # AI
    gemini_api_key: str
    
    # CLOUDINARY
    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str
    
    # IMAGE PROVIDER
    image_provider: Literal["pollinations", "openai", "huggingface", "fal", "stability", "replicate"] = "pollinations"
    
    # CORS
    allowed_origins: str = "http://localhost:3000"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
