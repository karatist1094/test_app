from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    cors_allowed_origins: List[str]


def get_settings() -> Settings:
    return Settings(
        DATABASE_URL = "postgresql+psycopg://postgres:admin123@localhost:5432/postgres",
        cors_allowed_origins = ["http://localhost:5500", "http://127.0.0.1:5500"],
    )


