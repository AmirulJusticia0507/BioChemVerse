"""Koneksi Redis (redis.asyncio) untuk cache & state sesi."""

from __future__ import annotations

import redis.asyncio as aioredis

_client: aioredis.Redis | None = None


async def connect(redis_url: str) -> None:
    global _client
    # protocol=2 (RESP2): kompatibel dengan Redis lama yang belum punya perintah HELLO
    _client = aioredis.from_url(redis_url, decode_responses=True, protocol=2)


async def disconnect() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


async def ping() -> bool:
    """True bila Redis merespons PING."""
    if _client is None:
        return False
    try:
        return (await _client.ping()) is True
    except aioredis.RedisError:
        return False


# --- Penyimpanan jawaban kuis (TTL 1 jam) -----------------------------------

async def store_quiz(payload: dict, ttl_seconds: int = 3600) -> bool:
    """Simpan kunci jawaban kuis di Redis dengan TTL."""
    import json

    if _client is None:
        return False
    try:
        await _client.set(
            f"quiz:{payload['quiz_id']}", json.dumps(payload), ex=ttl_seconds
        )
        return True
    except aioredis.RedisError:
        return False


async def take_quiz(quiz_id: str) -> dict | None:
    """Ambil sekaligus hapus sesi kuis (sekali pakai)."""
    import json

    if _client is None:
        return None
    try:
        raw = await _client.get(f"quiz:{quiz_id}")
        if raw is None:
            return None
        await _client.delete(f"quiz:{quiz_id}")
        return json.loads(raw)
    except aioredis.RedisError:
        return None
