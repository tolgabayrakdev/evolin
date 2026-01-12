from typing import List, Optional, Union

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/fa"
    database_echo: bool = False
    cors_origins: Union[str, List[str]] = "http://localhost:5173,https://localhost:5173"
    log_dir: str = "logs"
    app_name: str = "Evolin API"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "localhost"
    port: int = 8000
    reload: bool = True

    # JWT Settings
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Cookie Settings
    cookie_secure: bool = False  # Set to True in production with HTTPS
    cookie_same_site: str = "lax"  # lax, strict, or none
    cookie_domain: Optional[str] = None

    @property
    def cors_origins_list(self) -> List[str]:
        if isinstance(self.cors_origins, list):
            return self.cors_origins
        origins = self.cors_origins.split(",")
        return [o.strip() for o in origins if o.strip()]

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


settings = Settings()
