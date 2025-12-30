"""Application configuration using pydantic-settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/dbname"

    # Application
    secret_key: str = "dev-secret-key-change-in-production"
    debug: bool = True

    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # LiveKit
    livekit_api_key: str = "devAPIKeyXXX"
    livekit_api_secret: str = "devSecretYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"
    livekit_url: str = "ws://localhost:7880"

    # Firebase
    firebase_project_id: str = ""
    firebase_private_key_path: str = "./firebase-service-account.json"

    @property
    def LIVEKIT_API_KEY(self) -> str:
        return self.livekit_api_key

    @property
    def LIVEKIT_API_SECRET(self) -> str:
        return self.livekit_api_secret

    @property
    def LIVEKIT_URL(self) -> str:
        return self.livekit_url

    @property
    def cors_origins_list(self) -> list[str]:
        """Return CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
