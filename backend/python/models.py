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
