from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    api_key: str
    llama_server_url: str = "http://llama-cpp:8080"
    request_timeout: float = 120.0
    port: int = 8000


settings = Settings()
