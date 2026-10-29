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
