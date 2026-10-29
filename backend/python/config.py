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
        self.jwt_secret = os.getenv(
            "JWT_SECRET",
            "dev-only-secret-ganti-dengan-string-acak-minimal-32-karakter",
        )
        self.frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")
        self.resend_api_key = os.getenv("RESEND_API_KEY", "")
        self.email_from = os.getenv("EMAIL_FROM", "")
        if len(self.jwt_secret) < 32:
            raise ValueError("JWT_SECRET minimal 32 karakter (RFC 7518 untuk HS256)")

    @property
    def is_development(self) -> bool:
        """True bila berjalan di mode development (bukan production/staging)."""
        return self.env not in {"production", "staging"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
