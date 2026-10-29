"""Koneksi PostgreSQL (asyncpg) + bootstrap skema awal."""

from __future__ import annotations

from pathlib import Path

import asyncpg

SCHEMA_PATH = Path(__file__).with_name("schema.sql")

_pool: asyncpg.Pool | None = None


async def ensure_database(database_url: str) -> None:
    """Buat database bila belum ada (idempoten, aman dijalankan berulang)."""
    target = database_url.rsplit("/", 1)[-1]
    admin_url = database_url.rsplit("/", 1)[0] + "/postgres"
    conn = await asyncpg.connect(admin_url)
    try:
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", target
        )
        if not exists:
            await conn.execute(f'CREATE DATABASE "{target}"')
    finally:
        await conn.close()


async def connect(database_url: str) -> None:
    """Buka connection pool dan terapkan skema dari schema.sql."""
    global _pool
    _pool = await asyncpg.create_pool(dsn=database_url, min_size=1, max_size=5)
    async with _pool.acquire() as conn:
        await conn.execute(SCHEMA_PATH.read_text(encoding="utf-8"))


async def disconnect() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


async def ping() -> bool:
    """True bila database merespons SELECT 1."""
    if _pool is None:
        return False
    try:
        return await _pool.fetchval("SELECT 1") == 1
    except asyncpg.PostgresError:
        return False


# --- Helper tabel users -----------------------------------------------------

_USER_COLS = "id, username, email, role, created_at"


async def get_user_by_username(username: str) -> dict | None:
    if _pool is None:
        return None
    record = await _pool.fetchrow(
        f"SELECT {_USER_COLS}, password_hash FROM users WHERE username = $1", username
    )
    return dict(record) if record else None


async def get_user_by_email(email: str) -> dict | None:
    if _pool is None:
        return None
    record = await _pool.fetchrow(f"SELECT {_USER_COLS} FROM users WHERE email = $1", email)
    return dict(record) if record else None


async def get_user_by_id(user_id: str) -> dict | None:
    if _pool is None:
        return None
    try:
        record = await _pool.fetchrow(f"SELECT {_USER_COLS} FROM users WHERE id = $1", user_id)
    except (asyncpg.PostgresError, ValueError):
        return None
    return dict(record) if record else None


async def create_user(username: str, email: str, password_hash: str, role: str = "student") -> dict:
    record = await _pool.fetchrow(
        f"""
        INSERT INTO users (username, email, password_hash, role)
        VALUES ($1, $2, $3, $4)
        RETURNING {_USER_COLS}
        """,
        username,
        email,
        password_hash,
        role,
    )
    return dict(record)
