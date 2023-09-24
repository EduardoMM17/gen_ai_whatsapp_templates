from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Any
from dotenv import find_dotenv
from pydantic import PostgresDsn, validator
import os

print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", os.getenv("POSTGRES_SERVER"))

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(".env"), env_file_encoding="utf-8"
    )

    API_V1_STR: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    PROJECT_NAME: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        # cls is a refference to the class
        # v is the value of the field
        # values is a dict containing the values of all the fields in the model up to the point of validation
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )


settings = Settings()
