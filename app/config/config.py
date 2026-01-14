from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    log_level: str = "INFO"
    database_url: str
    resume_chat_collection: str

    llm_model: str
    llm_tools_model: str
    llm_provider: str

    langsmith_tracing: bool = True
    langsmith_api_key: str
    langsmith_project: str = "default"

    tavily_api_key: str

    # Tell Pydantic to look for a .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Create a singleton instance
settings = Settings()
