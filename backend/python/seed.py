"""Seed data referensi kimia (unsur, kategori, ion) — idempoten.

Sumber data: backend/python/data/*.json (dihasilkan oleh
scripts/import-chemsphere-data.mjs dari proyek ChemSphere).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import asyncpg
import bcrypt

DATA_DIR = Path(__file__).with_name("data")
EXPECTED_ELEMENTS = 118


def _load(name: str) -> list[dict]:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


async def ensure_seeded(pool: asyncpg.Pool) -> bool:
    """Isi tabel referensi bila masih kosong. Mengembalikan True bila seed berjalan."""
    count = await pool.fetchval("SELECT count(*) FROM elements")
    if count and count >= EXPECTED_ELEMENTS:
        return False

    categories = _load("categories.json")
    elements = _load("elements.json")
    ions = _load("ions.json")

    async with pool.acquire() as conn, conn.transaction():
        for category in categories:
            await conn.execute(
                """
                INSERT INTO categories (slug, name) VALUES ($1, $2)
                ON CONFLICT (slug) DO UPDATE SET name = EXCLUDED.name
                """,
                category["slug"],
                category["name"],
            )

        for element in elements:
            await conn.execute(
                """
                INSERT INTO elements
                    (atomic_number, symbol, name, name_latin, atomic_mass, category_slug,
                     period, group_no, description, uses, hazard, properties)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12::jsonb)
                ON CONFLICT (atomic_number) DO UPDATE SET
                    symbol = EXCLUDED.symbol,
                    name = EXCLUDED.name,
                    name_latin = EXCLUDED.name_latin,
                    atomic_mass = EXCLUDED.atomic_mass,
                    category_slug = EXCLUDED.category_slug,
                    period = EXCLUDED.period,
                    group_no = EXCLUDED.group_no,
                    description = EXCLUDED.description,
                    uses = EXCLUDED.uses,
                    hazard = EXCLUDED.hazard,
                    properties = EXCLUDED.properties
                """,
                element["atomic_number"],
                element["symbol"],
                element["name"],
                element["name_latin"],
                element["atomic_mass"],
                element["category"],
                element["period"],
                element["group"],
                element["description"],
                element["uses"],
                element["hazard"],
                element["properties"],
            )

        for ion in ions:
            await conn.execute(
                """
                INSERT INTO polyatomic_ions (name, formula, charge, description)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (name) DO UPDATE SET
                    formula = EXCLUDED.formula,
                    charge = EXCLUDED.charge,
                    description = EXCLUDED.description
                """,
                ion["name"],
                ion["formula"],
                ion["charge"],
                ion["description"],
            )

    return True


async def ensure_development_users(pool: asyncpg.Pool) -> None:
    """Buat akun lokal yang aman dipakai untuk demo; jangan pernah panggil di produksi."""
    accounts = (
        (
            os.getenv("SEED_ADMIN_USERNAME", "admin"),
            os.getenv("SEED_ADMIN_EMAIL", "admin@biochemverse.local"),
            os.getenv("SEED_ADMIN_PASSWORD", "Admin123!"),
            "admin",
        ),
        (
            os.getenv("SEED_USER_USERNAME", "demo"),
            os.getenv("SEED_USER_EMAIL", "demo@biochemverse.local"),
            os.getenv("SEED_USER_PASSWORD", "Demo123!"),
            "student",
        ),
    )
    async with pool.acquire() as conn:
        for username, email, password, role in accounts:
            password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            await conn.execute(
                """
                INSERT INTO users (username, email, password_hash, role)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (username) DO NOTHING
                """,
                username,
                email,
                password_hash,
                role,
            )
