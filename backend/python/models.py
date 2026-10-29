"""Skema respons Pydantic — jadi sumber dokumentasi OpenAPI/Swagger."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    name: str = Field(..., examples=["BioChemVerse API"], description="Nama API")
    version: str = Field(..., examples=["0.1.0"], description="Versi API")
    docs: str = Field(..., examples=["/docs"], description="URL Swagger UI")
    openapi: str = Field(..., examples=["/openapi.json"], description="URL spec OpenAPI")


class HealthResponse(BaseModel):
    status: str = Field(..., examples=["ok"], description="'ok' selama proses berjalan")


class ReadinessResponse(BaseModel):
    status: str = Field(..., examples=["ready"], description="'ready' bila semua dependency siap")
    postgres: str = Field(..., examples=["ok"], description="Status koneksi PostgreSQL")
    redis: str = Field(..., examples=["ok"], description="Status koneksi Redis")
    environment: str = Field(..., examples=["development"], description="Environment aktif (ENV)")


class ErrorDetail(BaseModel):
    status: str | None = Field(None, examples=["degraded"])
    postgres: str | None = Field(None, examples=["down"])
    redis: str | None = Field(None, examples=["ok"])


class ErrorResponse(BaseModel):
    detail: str | ErrorDetail = Field(
        ..., description="Keterangan kesalahan; memuat 'degraded' saat readiness gagal"
    )


class ModuleOut(BaseModel):
    id: str = Field(..., examples=["chemsphere"], description="Kode modul")
    name: str = Field(..., examples=["ChemSphere Engine"], description="Nama modul")
    description: str = Field(..., description="Ringkasan fungsi modul")
    features: list[str] = Field(..., description="Daftar fitur utama modul")


class ModuleListResponse(BaseModel):
    total: int = Field(..., examples=[3], description="Jumlah modul")
    data: list[ModuleOut]


# --- Autentikasi ------------------------------------------------------------


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=64, examples=["student1"], description="Username unik")
    email: str = Field(..., min_length=5, max_length=255, examples=["siswa@contoh.com"], description="Email unik")
    password: str = Field(..., min_length=8, max_length=128, description="Password, minimal 8 karakter")


class LoginRequest(BaseModel):
    username: str = Field(..., examples=["student1"], description="Username")
    password: str = Field(..., description="Password")


class UserOut(BaseModel):
    id: str = Field(..., description="UUID pengguna")
    username: str
    email: str
    role: str = Field(..., examples=["student"], description="Peran pengguna")
    created_at: str = Field(..., description="Waktu pembuatan akun (ISO-8601)")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT Bearer token")
    token_type: str = Field("bearer", examples=["bearer"])
    user: UserOut = Field(..., description="Profil pengguna yang berhasil login")


class PasswordResetRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=255, examples=["siswa@contoh.com"])


class PasswordResetConfirmRequest(BaseModel):
    token: str = Field(..., min_length=32, max_length=512)
    password: str = Field(..., min_length=8, max_length=128)


# --- Progres modul ----------------------------------------------------------


class ProgressOut(BaseModel):
    module: str = Field(..., examples=["chemsphere"], description="Kode modul (chemsphere|forensilab|anatomimed)")
    score: int = Field(..., ge=0, examples=[80], description="Skor kumulatif modul")
    completed: bool = Field(..., examples=[False], description="Modul sudah diselesaikan")
    updated_at: str = Field(..., description="Terakhir diperbarui (ISO-8601)")


class ProgressListResponse(BaseModel):
    total: int = Field(..., examples=[2], description="Jumlah modul yang punya progres")
    data: list[ProgressOut]


class ProgressUpdateRequest(BaseModel):
    score: int | None = Field(None, ge=0, le=1_000_000, description="Skor baru; kosongkan agar tetap")
    completed: bool | None = Field(None, description="Status selesai; kosongkan agar tetap")


# --- Tabel periodik (ChemSphere) -------------------------------------------


class CategoryOut(BaseModel):
    slug: str = Field(..., examples=["transition"], description="Kode kategori")
    name: str = Field(..., examples=["Logam Transisi"], description="Nama kategori (Indonesia)")
    element_count: int = Field(..., examples=[38], description="Jumlah unsur dalam kategori")


class CategoryListResponse(BaseModel):
    total: int
    data: list[CategoryOut]


class ElementOut(BaseModel):
    atomic_number: int = Field(..., examples=[26], description="Nomor atom")
    symbol: str = Field(..., examples=["Fe"], description="Simbol unsur")
    name: str = Field(..., examples=["Besi"], description="Nama Indonesia")
    name_latin: str | None = Field(None, examples=["Ferrum"], description="Nama Latin")
    atomic_mass: float = Field(..., examples=[55.845], description="Massa atom (u)")
    category: CategoryOut | None = Field(None, description="Kategori unsur")
    period: int | None = Field(None, examples=[4], description="Periode")
    group: int | None = Field(None, examples=[8], description="Golongan")
    description: str | None = Field(None, description="Deskripsi singkat (Indonesia)")
    uses: str | None = Field(None, description="Kegunaan utama")
    hazard: str | None = Field(None, description="Peringatan bahaya")
    properties: dict = Field(
        ...,
        description=(
            "Properti fisika/kimia: melt (K), boil (K), density, electronegativity, "
            "ionization, atomicRadius, covalentRadius, molarHeat, phase, block, "
            "shells, oxidationStates, appearance, discoveredBy, namedBy, yearDiscovered"
        ),
    )


class ElementListResponse(BaseModel):
    total: int = Field(..., examples=[118])
    data: list[ElementOut]


class IonOut(BaseModel):
    name: str = Field(..., examples=["Amonium"])
    formula: str = Field(..., examples=["NH₄⁺"], description="Rumus ion")
    charge: str | None = Field(None, examples=["+1"], description="Muatan")
    description: str | None = Field(None, description="Penjelasan (Indonesia)")


class IonListResponse(BaseModel):
    total: int = Field(..., examples=[30])
    data: list[IonOut]


# --- Kuis unsur -------------------------------------------------------------


class QuizStartRequest(BaseModel):
    topic: str = Field("campuran", examples=["simbol"], description="Topik: simbol|nomor-atom|kategori|golongan-periode|campuran")
    count: int = Field(10, ge=1, le=30, description="Jumlah soal (1-30)")


class QuizQuestionOut(BaseModel):
    id: str = Field(..., examples=["0"])
    question: str = Field(..., examples=["Apa simbol kimia untuk Besi?"])
    options: list[str] = Field(..., examples=[["Fe", "F", "Fr", "Fm"]])


class QuizStartResponse(BaseModel):
    quiz_id: str = Field(..., description="Token sesi kuis (berlaku 1 jam, sekali pakai)")
    topic: str
    questions: list[QuizQuestionOut] = Field(..., description="Soal tanpa kunci jawaban")


class QuizSubmitRequest(BaseModel):
    quiz_id: str = Field(..., description="quiz_id dari /quiz/start")
    answers: list[str] = Field(..., description="Jawaban berurutan sesuai soal")
    duration_sec: int | None = Field(None, ge=0, le=86_400, description="Durasi pengerjaan (detik)")


class QuizResultItem(BaseModel):
    index: int
    correct: str = Field(..., description="Jawaban benar")
    given: str | None = Field(None, description="Jawaban pengguna")
    is_correct: bool


class QuizSubmitResponse(BaseModel):
    attempt_id: int
    topic: str
    total: int
    correct: int
    score: int = Field(..., description="Persentase benar (0-100)")
    results: list[QuizResultItem]


class QuizAttemptOut(BaseModel):
    id: int
    topic: str
    total: int
    correct: int
    score: int
    duration_sec: int | None = None
    created_at: datetime


class QuizAttemptListResponse(BaseModel):
    total: int
    data: list[QuizAttemptOut]


# --- Bookmark unsur ---------------------------------------------------------


class BookmarkCreateRequest(BaseModel):
    atomic_number: int = Field(..., ge=1, le=118, examples=[26])
    note: str | None = Field(None, max_length=255, description="Catatan singkat (opsional)")


class BookmarkOut(BaseModel):
    atomic_number: int
    symbol: str
    name: str
    category_slug: str | None = None
    note: str | None = None
    created_at: datetime


class BookmarkListResponse(BaseModel):
    total: int
    data: list[BookmarkOut]
