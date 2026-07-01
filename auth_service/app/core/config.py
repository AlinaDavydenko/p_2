from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, populated from environment variables / .env file."""

    APP_NAME: str = "auth-service"
    ENV: str = "local"

    JWT_SECRET: str = "change_me_super_secret"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    SQLITE_PATH: str = "./auth.db"
    DATABASE_URL: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"sqlite+aiosqlite:///{self.SQLITE_PATH}"


settings = Settings()
