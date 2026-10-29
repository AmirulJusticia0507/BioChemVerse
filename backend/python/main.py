"""BioChemVerse API — titik masuk aplikasi FastAPI."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

import cache
import db
from auth import create_access_token, get_current_user, hash_password, verify_password
from config import get_settings
from models import (
    CategoryListResponse,
    CategoryOut,
    ElementListResponse,
    ElementOut,
    ErrorResponse,
    HealthResponse,
    IonListResponse,
    IonOut,
    LoginRequest,
    ModuleListResponse,
    ModuleOut,
    ProgressListResponse,
    ProgressOut,
    ProgressUpdateRequest,
    ReadinessResponse,
    RegisterRequest,
    RootResponse,
    TokenResponse,
    UserOut,
)
import seed

settings = get_settings()

TAGS_METADATA = [
    {"name": "general", "description": "Health check dan informasi dasar API."},
    {
        "name": "modules",
        "description": "Daftar modul platform BioChemVerse: ChemSphere, ForensiLab, AnatomiMed.",
    },
    {
        "name": "auth",
        "description": "Autentikasi JWT — register, login, dan profil pengguna. Sertakan `Authorization: Bearer <token>`.",
    },
    {
        "name": "progress",
        "description": "Progres belajar per modul (butuh token). Skor & status selesai per pengguna.",
    },
    {
        "name": "elements",
        "description": "Tabel periodik: 118 unsur (nama Indonesia), kategori, dan ion poliatomik.",
    },
]

MODULE_IDS = ("chemsphere", "forensilab", "anatomimed")

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
    pool = await db.connect(settings.database_url)
    await seed.ensure_seeded(pool)
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


# --- Autentikasi ------------------------------------------------------------


def _user_out(user: dict) -> dict:
    """Sesuaikan baris database dengan skema UserOut (waktu → ISO string)."""
    created = user.get("created_at")
    return {
        "id": str(user["id"]),
        "username": user["username"],
        "email": user.get("email", ""),
        "role": user.get("role", "student"),
        "created_at": created.isoformat() if hasattr(created, "isoformat") else str(created),
    }


@app.post(
    "/api/v1/auth/register",
    tags=["auth"],
    response_model=UserOut,
    status_code=201,
    responses={409: {"model": ErrorResponse, "description": "Username atau email sudah terdaftar"}},
    summary="Daftar akun baru",
)
async def register(payload: RegisterRequest):
    """Buat akun baru; password di-hash dengan bcrypt, tidak pernah disimpan polos."""
    if await db.get_user_by_username(payload.username):
        raise HTTPException(status_code=409, detail="Username sudah terdaftar")
    if await db.get_user_by_email(payload.email):
        raise HTTPException(status_code=409, detail="Email sudah terdaftar")
    user = await db.create_user(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    return _user_out(user)


@app.post(
    "/api/v1/auth/login",
    tags=["auth"],
    response_model=TokenResponse,
    responses={401: {"model": ErrorResponse, "description": "Username atau password salah"}},
    summary="Login dan dapatkan JWT",
)
async def login(payload: LoginRequest):
    """Verifikasi kredensial; kembalikan Bearer token berlaku 12 jam."""
    user = await db.get_user_by_username(payload.username)
    if user is None or not verify_password(payload.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Username atau password salah")
    token = create_access_token(str(user["id"]), user["username"])
    return {"access_token": token, "token_type": "bearer", "user": _user_out(user)}


@app.get(
    "/api/v1/auth/me",
    tags=["auth"],
    response_model=UserOut,
    responses={401: {"model": ErrorResponse, "description": "Token tidak ada, tidak valid, atau kedaluwarsa"}},
    summary="Profil pengguna aktif",
)
async def me(current_user: dict = Depends(get_current_user)):
    """Butuh header `Authorization: Bearer <token>`."""
    return _user_out(current_user)


# --- Progres modul ----------------------------------------------------------


def _progress_out(row: dict) -> dict:
    updated = row.get("updated_at")
    return {
        "module": row["module"],
        "score": row["score"],
        "completed": row["completed"],
        "updated_at": updated.isoformat() if hasattr(updated, "isoformat") else str(updated),
    }


def _validate_module(module_id: str) -> str:
    if module_id not in MODULE_IDS:
        raise HTTPException(
            status_code=400,
            detail=f"Modul tidak dikenal: '{module_id}'. Pilihan: {', '.join(MODULE_IDS)}",
        )
    return module_id


@app.get(
    "/api/v1/progress",
    tags=["progress"],
    response_model=ProgressListResponse,
    responses={401: {"model": ErrorResponse, "description": "Token tidak valid atau tidak ada"}},
    summary="Semua progres pengguna aktif",
)
async def list_progress(current_user: dict = Depends(get_current_user)):
    """Daftar progres seluruh modul milik pengguna yang sedang login."""
    rows = await db.list_progress(str(current_user["id"]))
    return {"total": len(rows), "data": [_progress_out(row) for row in rows]}


@app.get(
    "/api/v1/progress/{module_id}",
    tags=["progress"],
    response_model=ProgressOut,
    responses={
        400: {"model": ErrorResponse, "description": "Kode modul tidak dikenal"},
        401: {"model": ErrorResponse, "description": "Token tidak valid atau tidak ada"},
        404: {"model": ErrorResponse, "description": "Belum ada progres untuk modul ini"},
    },
    summary="Progres satu modul",
)
async def get_progress(module_id: str, current_user: dict = Depends(get_current_user)):
    _validate_module(module_id)
    row = await db.get_progress(str(current_user["id"]), module_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Belum ada progres untuk modul '{module_id}'")
    return _progress_out(row)


@app.put(
    "/api/v1/progress/{module_id}",
    tags=["progress"],
    response_model=ProgressOut,
    responses={
        400: {"model": ErrorResponse, "description": "Kode modul tidak dikenal"},
        401: {"model": ErrorResponse, "description": "Token tidak valid atau tidak ada"},
        422: {"model": ErrorResponse, "description": "Skor di luar rentang 0–1000000"},
    },
    summary="Buat atau perbarui progres (upsert)",
)
async def upsert_progress(
    module_id: str,
    payload: ProgressUpdateRequest,
    current_user: dict = Depends(get_current_user),
):
    """Upsert per modul. Field yang tidak dikirim dipertahankan nilainya."""
    _validate_module(module_id)
    row = await db.upsert_progress(
        user_id=str(current_user["id"]),
        module=module_id,
        score=payload.score,
        completed=payload.completed,
    )
    return _progress_out(row)


# --- Tabel periodik (ChemSphere) -------------------------------------------


def _element_out(row: dict, counts: dict[str, int] | None = None) -> dict:
    """Sesuaikan baris database dengan skema ElementOut."""
    category = None
    if row.get("category_slug"):
        category = {
            "slug": row["category_slug"],
            "name": row.get("category_name") or row["category_slug"],
            "element_count": (counts or {}).get(row["category_slug"], 0),
        }
    return {
        "atomic_number": row["atomic_number"],
        "symbol": row["symbol"],
        "name": row["name"],
        "name_latin": row.get("name_latin"),
        "atomic_mass": float(row["atomic_mass"]),
        "category": category,
        "period": row.get("period"),
        "group": row.get("group_no"),
        "description": row.get("description"),
        "uses": row.get("uses"),
        "hazard": row.get("hazard"),
        "properties": row.get("properties") or {},
    }


@app.get(
    "/api/v1/elements",
    tags=["elements"],
    response_model=ElementListResponse,
    summary="Daftar unsur (tabel periodik)",
)
async def list_elements(
    q: str | None = Query(
        None, min_length=1, max_length=100,
        description="Cari berdasarkan nama, nama Latin, simbol, atau nomor atom",
        examples=["Fe"],
    ),
    category: str | None = Query(None, description="Filter kategori (slug)", examples=["transition"]),
    period: int | None = Query(None, ge=1, le=7, description="Filter periode (1-7)"),
    block: str | None = Query(None, pattern="^[spdf]$", description="Filter blok (s/p/d/f)"),
    phase: str | None = Query(
        None, pattern="^(solid|liquid|gas|artificial)$", description="Fase pada suhu ruang"
    ),
):
    """Seluruh 118 unsur dengan filter opsional pencarian, kategori, periode, blok, dan fase."""
    rows = await db.list_elements(q=q, category=category, period=period, block=block, phase=phase)
    counts = {c["slug"]: c["element_count"] for c in await db.list_categories()}
    return {"total": len(rows), "data": [_element_out(row, counts) for row in rows]}


@app.get(
    "/api/v1/elements/{identifier}",
    tags=["elements"],
    response_model=ElementOut,
    responses={404: {"model": ErrorResponse, "description": "Unsur tidak ditemukan"}},
    summary="Detail unsur",
)
async def get_element(identifier: str):
    """Detail satu unsur berdasarkan simbol (Fe) atau nomor atom (26)."""
    row = await db.get_element(identifier)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Unsur '{identifier}' tidak ditemukan")
    counts = {c["slug"]: c["element_count"] for c in await db.list_categories()}
    return _element_out(row, counts)


@app.get(
    "/api/v1/categories",
    tags=["elements"],
    response_model=CategoryListResponse,
    summary="Daftar kategori unsur",
)
async def list_categories():
    """Sepuluh kategori tabel periodik beserta jumlah unsurnya."""
    rows = await db.list_categories()
    return {"total": len(rows), "data": rows}


@app.get(
    "/api/v1/ions",
    tags=["elements"],
    response_model=IonListResponse,
    summary="Daftar ion poliatomik",
)
async def list_ions():
    """Referensi ion poliatomik (kation & anion) beserta muatannya."""
    rows = await db.list_ions()
    return {"total": len(rows), "data": rows}
