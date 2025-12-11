from functools import lru_cache
from typing import Optional
from pydantic import Field, AnyHttpUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "fastapi-pydantic-mini"
    WEATHER_API_BASE_URL: AnyHttpUrl = Field(
        "https://api.openweathermap.org/data/2.5", env="WEATHER_API_BASE_URL"
    )
    WEATHER_API_TIMEOUT: int = Field(10, env="WEATHER_API_TIMEOUT")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    # add API key if you used one in .env
    WEATHER_API_KEY: Optional[str] = Field(None, env="WEATHER_API_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()