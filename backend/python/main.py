"""BioChemVerse API — titik masuk aplikasi FastAPI."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import cache
import db
from config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Siapkan koneksi database & Redis saat startup, tutup saat shutdown."""
    await db.ensure_database(settings.database_url)
    await db.connect(settings.database_url)
    await cache.connect(settings.redis_url)
    yield
    await cache.disconnect()
    await db.disconnect()


app = FastAPI(
    title=settings.app_name,
    description=(
        "API untuk platform edukasi BioChemVerse: ChemSphere (kimia), "
        "ForensiLab (forensik), dan AnatomiMed (anatomi & simulasi pasien)."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["general"])
async def root():
    """Informasi dasar API."""
    return {
        "name": settings.app_name,
        "version": app.version,
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.get("/health", tags=["general"], summary="Liveness check")
async def health():
    """Status proses aplikasi (tidak mengecek dependency)."""
    return {"status": "ok"}


@app.get("/health/ready", tags=["general"], summary="Readiness check")
async def readiness():
    """Cek koneksi PostgreSQL dan Redis; 503 bila salah satu tidak siap."""
    db_ok = await db.ping()
    redis_ok = await cache.ping()
    if not (db_ok and redis_ok):
        raise HTTPException(
            status_code=503,
            detail={
                "status": "degraded",
                "postgres": "ok" if db_ok else "down",
                "redis": "ok" if redis_ok else "down",
            },
        )
    return {
        "status": "ready",
        "postgres": "ok",
        "redis": "ok",
        "environment": settings.env,
    }
