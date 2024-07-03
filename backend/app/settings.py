import sys
import pytz
from pydantic import field_validator, PostgresDsn, ValidationInfo

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEV: bool = False

    JWT_SECRET_KEY: str = "1"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRE_IN_MINUTES: int = 180
    JWT_REFRESH_EXPIRE_IN_MINUTES: int = 270

    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    TIME_ZONE: pytz.BaseTzInfo = pytz.timezone("Asia/Bangkok")

    @field_validator("JWT_SECRET_KEY", "POSTGRES_PASSWORD")
    @classmethod
    def check_default_secret(cls, value: str, info: ValidationInfo):
        if info.data.get("DEV"):
            return value
        if value == "change_this":
            raise ValueError(f"Please change value of {info.field_name}")

    @property
    def db_uri(self) -> PostgresDsn:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def db_async_uri(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


sys.modules[__name__] = Settings()
