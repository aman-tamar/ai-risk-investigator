from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Risk Investigator"
    app_version: str = "0.1.0"
    debug: bool = True

    groq_api_key: str = ""
    groq_model: str = ""

    database_url: str = ""

    neo4j_uri: str = ""
    neo4j_username: str = ""
    neo4j_password: str = ""

    langsmith_api_key: str = ""
    langsmith_project: str = "ai-risk-investigator"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()