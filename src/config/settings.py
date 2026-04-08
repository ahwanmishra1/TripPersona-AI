from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    app_name: str = "TripPersona"
    app_env: str = "dev"

    openweather_api_key: str = ""
    tavily_api_key: str = ""
    exchangerate_api_key: str = ""

    openai_api_key: str = ""
    groq_api_key: str = ""

    llm_provider: str = "groq"
    llm_model: str = "llama-3.3-70b-versatile"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


settings = Settings()