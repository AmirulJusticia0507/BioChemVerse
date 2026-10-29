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
