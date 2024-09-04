from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class EnviromentSettings(BaseSettings):
    """
    EnviromentSettings handles configuration settings for the environment.

    This class inherits from BaseSettings and utilizes pydantic for managing
    environment variables and settings. It reads configurations from an `.env` file.

    Attributes:
        `model_config` (SettingsConfigDict): Configuration for the settings model.
        `debug_mode` (bool): Flag indicating if the application is in debug mode.
        `secret` (str): Secret key used on JWT signature
        `algorithm` (str): Algorithm used in JWT handling
        `postgres_dsn` (PostgresDsn): Data Source Name for PostgreSQL connection.
    """
    model_config = SettingsConfigDict(
                            extra="ignore", env_file=".env",
                            env_file_encoding="utf-8"
                        )
    secret: str
    algorithm: str
    postgres_dsn: PostgresDsn

# Creating an instance of EnviromentSettings
enviroment_settings = EnviromentSettings(_env_file=".env", _env_file_encoding='utf-8')
