"""Skema respons Pydantic — jadi sumber dokumentasi OpenAPI/Swagger."""

from __future__ import annotations

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
