from pathlib import Path
from dotenv import load_dotenv
import os
from dataclasses import dataclass

ENV_DIR = Path("env")
DEFAULT_ENV_FILE: Path = ENV_DIR / ".env"


class EnvLoadError(Exception):
    """Raised when an environment file cannot be loaded."""


def load_environment() -> None:
    """
    Load environment variables based on APP_ENV.
    - 'production' always uses /env/.env
    - other environments use /env/.env.{APP_ENV}
    Raises EnvLoadError if the env file cannot be loaded.
    """
    app_env = os.getenv("APP_ENV", "development").lower()

    if app_env == "production":
        env_file = DEFAULT_ENV_FILE
    else:
        env_file = ENV_DIR / f".env.{app_env}"
        if not env_file.exists():
            env_file = DEFAULT_ENV_FILE

    if not load_dotenv(env_file):
        raise EnvLoadError(f"Failed to load environment file: {env_file}")


@dataclass(frozen=True)
class EnvData:
    """
    Singleton-like read-only environment configuration.
    Only one instance exists, loaded from environment variables.
    """

    APP_ENV: str = os.getenv("APP_ENV", "development").lower()
    DEBUG: bool = os.getenv("DEBUG", "0").lower() in ("1", "true", "yes")
    LOG_LEVEL: int = int(os.getenv("LOG_LEVEL", "2"))

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"


ENV_DATA = EnvData()
