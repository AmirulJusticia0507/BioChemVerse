"""Koneksi PostgreSQL (asyncpg) + bootstrap skema awal."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import timedelta
from typing import Any

import asyncpg

SCHEMA_PATH = Path(__file__).with_name("schema.sql")

_pool: asyncpg.Pool | None = None


async def _init_connection(conn: Any) -> None:
    """Codec json/jsonb: kirim & terima sebagai Python dict/list (bukan string)."""
    await conn.set_type_codec(
        "json", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
    )
    await conn.set_type_codec(
        "jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
    )


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


async def connect(database_url: str) -> asyncpg.Pool:
    """Buka connection pool dan terapkan skema dari schema.sql. Mengembalikan pool."""
    global _pool
    _pool = await asyncpg.create_pool(
        dsn=database_url, min_size=1, max_size=5, init=_init_connection
    )
    async with _pool.acquire() as conn:
        await conn.execute(SCHEMA_PATH.read_text(encoding="utf-8"))
    return _pool


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


async def create_password_reset_token(user_id: str, token_hash: str) -> None:
    """Simpan satu token reset aktif per akun; token polos tidak pernah disimpan."""
    if _pool is None:
        return
    async with _pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute("DELETE FROM password_reset_tokens WHERE user_id = $1", user_id)
            await conn.execute(
                """
                INSERT INTO password_reset_tokens (token_hash, user_id, expires_at)
                VALUES ($1, $2, now() + $3::interval)
                """,
                token_hash,
                user_id,
                timedelta(hours=1),
            )


async def delete_password_reset_token(token_hash: str) -> None:
    if _pool is not None:
        await _pool.execute("DELETE FROM password_reset_tokens WHERE token_hash = $1", token_hash)


async def consume_password_reset_token(token_hash: str, password_hash: str) -> bool:
    """Tukar token yang valid menjadi password baru sekali saja, secara atomik."""
    if _pool is None:
        return False
    async with _pool.acquire() as conn:
        async with conn.transaction():
            row = await conn.fetchrow(
                """
                DELETE FROM password_reset_tokens
                WHERE token_hash = $1 AND expires_at > now()
                RETURNING user_id
                """,
                token_hash,
            )
            if row is None:
                return False
            user_id = row["user_id"]
            await conn.execute(
                "UPDATE users SET password_hash = $1, updated_at = now() WHERE id = $2",
                password_hash,
                user_id,
            )
            await conn.execute("DELETE FROM password_reset_tokens WHERE user_id = $1", user_id)
            return True


# --- Helper tabel user_progress --------------------------------------------

_PROGRESS_COLS = "module, score, completed, updated_at"


async def list_progress(user_id: str) -> list[dict]:
    if _pool is None:
        return []
    records = await _pool.fetch(
        f"SELECT {_PROGRESS_COLS} FROM user_progress WHERE user_id = $1 ORDER BY module",
        user_id,
    )
    return [dict(record) for record in records]


async def get_progress(user_id: str, module: str) -> dict | None:
    if _pool is None:
        return None
    record = await _pool.fetchrow(
        f"SELECT {_PROGRESS_COLS} FROM user_progress WHERE user_id = $1 AND module = $2",
        user_id,
        module,
    )
    return dict(record) if record else None


async def upsert_progress(
    user_id: str,
    module: str,
    score: int | None = None,
    completed: bool | None = None,
) -> dict:
    """Insert atau update progres; field yang tidak dikirim tetap dipertahankan."""
    record = await _pool.fetchrow(
        f"""
        INSERT INTO user_progress (user_id, module, score, completed)
        VALUES ($1, $2, COALESCE($3, 0), COALESCE($4, false))
        ON CONFLICT (user_id, module) DO UPDATE
            SET score = COALESCE($3, user_progress.score),
                completed = COALESCE($4, user_progress.completed),
                updated_at = now()
        RETURNING {_PROGRESS_COLS}
        """,
        user_id,
        module,
        score,
        completed,
    )
    return dict(record)


# --- Data referensi kimia (tabel periodik) ---------------------------------

_ELEMENT_SELECT = """
    SELECT e.atomic_number, e.symbol, e.name, e.name_latin, e.atomic_mass,
           e.category_slug, e.period, e.group_no, e.description, e.uses, e.hazard,
           e.properties, c.name AS category_name
    FROM elements e
    LEFT JOIN categories c ON c.slug = e.category_slug
"""


async def list_elements(
    q: str | None = None,
    category: str | None = None,
    period: int | None = None,
    block: str | None = None,
    phase: str | None = None,
) -> list[dict]:
    """Semua unsur dengan filter opsional (pencarian, kategori, periode, blok, fase)."""
    if _pool is None:
        return []

    clauses: list[str] = []
    params: list[object] = []

    def add(fragment: str, value: object) -> str:
        params.append(value)
        return fragment.replace("?", f"${len(params)}")

    if q:
        like = f"%{q}%"
        params.extend([like, like, like])
        first, second, third = f"${len(params) - 2}", f"${len(params) - 1}", f"${len(params)}"
        condition = (
            f"(e.name ILIKE {first} OR e.name_latin ILIKE {second} OR e.symbol ILIKE {third}"
        )
        if q.isdigit():
            params.append(int(q))
            condition += f" OR e.atomic_number = ${len(params)}"
        clauses.append(condition + ")")
    if category:
        clauses.append(add("e.category_slug = ?", category))
    if period:
        clauses.append(add("e.period = ?", period))
    if block:
        clauses.append(add("e.properties->>'block' = ?", block.lower()))
    if phase:
        clauses.append(add("e.properties->>'phase' = ?", phase.capitalize()))

    where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
    records = await _pool.fetch(_ELEMENT_SELECT + where + " ORDER BY e.atomic_number", *params)
    return [dict(record) for record in records]


async def get_element(identifier: str) -> dict | None:
    """Cari unsur berdasarkan simbol (mis. 'Fe') atau nomor atom (mis. '26')."""
    if _pool is None:
        return None
    if identifier.isdigit():
        record = await _pool.fetchrow(
            _ELEMENT_SELECT + " WHERE e.atomic_number = $1", int(identifier)
        )
    else:
        record = await _pool.fetchrow(
            _ELEMENT_SELECT + " WHERE lower(e.symbol) = lower($1)", identifier.strip()
        )
    return dict(record) if record else None


async def list_categories() -> list[dict]:
    if _pool is None:
        return []
    records = await _pool.fetch(
        """
        SELECT c.slug, c.name, count(e.atomic_number) AS element_count
        FROM categories c
        LEFT JOIN elements e ON e.category_slug = c.slug
        GROUP BY c.slug, c.name
        ORDER BY min(e.atomic_number)
        """
    )
    return [dict(record) for record in records]


async def list_ions() -> list[dict]:
    if _pool is None:
        return []
    records = await _pool.fetch(
        "SELECT name, formula, charge, description FROM polyatomic_ions ORDER BY name"
    )
    return [dict(record) for record in records]


# --- Kuis unsur -------------------------------------------------------------

_ATTEMPT_COLS = "id, topic, total, correct, score, duration_sec, created_at"


async def all_elements_for_quiz() -> list[dict]:
    """Data minimal unsur untuk membangkitkan soal kuis."""
    if _pool is None:
        return []
    records = await _pool.fetch(
        """
        SELECT e.atomic_number, e.symbol, e.name, e.period, e.group_no,
               c.name AS category_name
        FROM elements e
        LEFT JOIN categories c ON c.slug = e.category_slug
        ORDER BY e.atomic_number
        """
    )
    return [dict(record) for record in records]


async def create_quiz_attempt(
    user_id: str, topic: str, total: int, correct: int, score: int, duration_sec: int | None
) -> dict:
    record = await _pool.fetchrow(
        f"""
        INSERT INTO quiz_attempts (user_id, topic, total, correct, score, duration_sec)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING {_ATTEMPT_COLS}
        """,
        user_id,
        topic,
        total,
        correct,
        score,
        duration_sec,
    )
    return dict(record)


async def list_quiz_attempts(user_id: str, limit: int = 20) -> list[dict]:
    records = await _pool.fetch(
        f"""
        SELECT {_ATTEMPT_COLS} FROM quiz_attempts
        WHERE user_id = $1 ORDER BY created_at DESC LIMIT $2
        """,
        user_id,
        limit,
    )
    return [dict(record) for record in records]


# --- Bookmark unsur ---------------------------------------------------------

_BOOKMARK_SELECT = """
    SELECT b.atomic_number, b.note, b.created_at,
           e.symbol, e.name, e.category_slug
    FROM bookmarks b
    JOIN elements e ON e.atomic_number = b.atomic_number
"""


async def list_bookmarks(user_id: str) -> list[dict]:
    records = await _pool.fetch(
        _BOOKMARK_SELECT + " WHERE b.user_id = $1 ORDER BY b.created_at DESC", user_id
    )
    return [dict(record) for record in records]


async def add_bookmark(user_id: str, atomic_number: int, note: str | None) -> dict | None:
    """Tambah bookmark; None bila unsur tidak ada atau sudah dibookmark (409 di route)."""
    exists = await _pool.fetchval("SELECT 1 FROM elements WHERE atomic_number = $1", atomic_number)
    if not exists:
        return None
    record = await _pool.fetchrow(
        """
        INSERT INTO bookmarks (user_id, atomic_number, note)
        VALUES ($1, $2, $3)
        ON CONFLICT (user_id, atomic_number) DO NOTHING
        RETURNING atomic_number
        """,
        user_id,
        atomic_number,
        note,
    )
    if record is None:
        raise LookupError("sudah dibookmark")
    row = await _pool.fetchrow(
        _BOOKMARK_SELECT + " WHERE b.user_id = $1 AND b.atomic_number = $2",
        user_id,
        atomic_number,
    )
    return dict(row)


async def delete_bookmark(user_id: str, atomic_number: int) -> bool:
    result = await _pool.execute(
        "DELETE FROM bookmarks WHERE user_id = $1 AND atomic_number = $2",
        user_id,
        atomic_number,
    )
    return result.split()[-1] != "0"
