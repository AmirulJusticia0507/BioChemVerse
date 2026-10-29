"""Konfigurasi BioChemVerse API — dibaca dari environment / file .env."""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Pengaturan aplikasi yang dimuat sekali di awal proses."""

    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "BioChemVerse API")
        self.env = os.getenv("ENV", "development")
        self.port = int(os.getenv("PORT", "8000"))
        self.database_url = os.getenv(
            "DATABASE_URL", "postgresql://postgres@localhost:5432/biochemverse"
        )
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.cors_origins = [
            origin.strip()
            for origin in os.getenv(
                "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
            ).split(",")
            if origin.strip()
        ]
        self.jwt_secret = os.getenv("JWT_SECRET", "change-me-in-production")


@lru_cache
def get_settings() -> Settings:
    return Settings()
