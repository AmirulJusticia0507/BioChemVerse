"""BioChemVerse API — titik masuk aplikasi FastAPI."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import cache
import db
from config import get_settings
from models import (
    ErrorResponse,
    HealthResponse,
    ModuleListResponse,
    ModuleOut,
    ReadinessResponse,
    RootResponse,
)

settings = get_settings()

TAGS_METADATA = [
    {"name": "general", "description": "Health check dan informasi dasar API."},
    {
        "name": "modules",
        "description": "Daftar modul platform BioChemVerse: ChemSphere, ForensiLab, AnatomiMed.",
    },
]

MODULES = [
    ModuleOut(
        id="chemsphere",
        name="ChemSphere Engine",
        description="Mesin kimia interaktif: tabel periodik, visualisasi molekul 3D, dan sandbox reaksi.",
        features=[
            "Interactive Periodic Table",
            "3D Molecular Visualizer",
            "Chemical Reaction Sandbox",
        ],
    ),
    ModuleOut(
        id="forensilab",
        name="ForensiLab",
        description="Gamifikasi forensik dan biokimia berbasis studi kasus.",
        features=[
            "Interactive Crime Scene & Evidence Board",
            "Virtual Lab Mini-Games (toksikologi, TLC, spektroskopi, serologi, DNA fingerprinting)",
            "Dynamic Feedback System",
        ],
    ),
    ModuleOut(
        id="anatomimed",
        name="AnatomiMed & Virtual Patient Simulator",
        description="Penjelajahan anatomi 3D berlapis dan simulasi diagnosis pasien virtual.",
        features=[
            "3D Body Dissection Viewer",
            "Virtual Patient Simulator (anamnesis, pemeriksaan fisik, uji lab)",
            "Pathophysiology & Drug Simulator",
        ],
    ),
]


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
    openapi_tags=TAGS_METADATA,
    contact={"name": "BioChemVerse", "url": "https://github.com/AmirulJusticia0507/BioChemVerse"},
    license_info={"name": "MIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["general"], response_model=RootResponse, summary="Info API")
async def root():
    """Informasi dasar API: nama, versi, dan lokasi dokumentasi."""
    return {
        "name": settings.app_name,
        "version": app.version,
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.get(
    "/health",
    tags=["general"],
    response_model=HealthResponse,
    summary="Liveness check",
)
async def health():
    """Status proses aplikasi (tidak mengecek dependency)."""
    return {"status": "ok"}


@app.get(
    "/health/ready",
    tags=["general"],
    response_model=ReadinessResponse,
    responses={503: {"model": ErrorResponse, "description": "PostgreSQL dan/atau Redis tidak siap"}},
    summary="Readiness check",
)
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


@app.get(
    "/api/v1/modules",
    tags=["modules"],
    response_model=ModuleListResponse,
    summary="Daftar modul platform",
)
async def list_modules():
    """Semua modul utama BioChemVerse beserta fiturnya."""
    return {"total": len(MODULES), "data": MODULES}
