# 📖 Dokumentasi API — BioChemVerse

Dokumen ini ringkasan dari spesifikasi **OpenAPI 3** yang dihasilkan otomatis oleh FastAPI.

| Sumber | Lokasi |
| --- | --- |
| Swagger UI (interaktif) | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |
| Spesifikasi OpenAPI (JSON) | `http://localhost:8000/openapi.json` |
| Snapshot spec (ter-commit) | [`docs/openapi.json`](./openapi.json) |

---

## Menjalankan API

```bash
cd backend/python
pip install -r requirements.txt
uvicorn main:app --reload          # http://localhost:8000
```

Konfigurasi dibaca dari environment / file `.env` (salin dari `.env.example` di root).

---

## Endpoint

| Method | Path | Tag | Deskripsi | Success | Error |
| --- | --- | --- | --- | --- | --- |
| GET | `/` | general | Info dasar API (nama, versi, lokasi docs) | 200 | — |
| GET | `/health` | general | Liveness check — status proses | 200 | — |
| GET | `/health/ready` | general | Readiness check — koneksi PostgreSQL & Redis | 200 | 503 |
| GET | `/api/v1/modules` | modules | Daftar modul platform + fiturnya | 200 | — |

### 1. `GET /` — Info API

```bash
curl http://localhost:8000/
```

```json
{
  "name": "BioChemVerse API",
  "version": "0.1.0",
  "docs": "/docs",
  "openapi": "/openapi.json"
}
```

### 2. `GET /health` — Liveness

```bash
curl http://localhost:8000/health
```

```json
{ "status": "ok" }
```

### 3. `GET /health/ready` — Readiness (PostgreSQL + Redis)

Sukses (200):

```bash
curl http://localhost:8000/health/ready
```

```json
{
  "status": "ready",
  "postgres": "ok",
  "redis": "ok",
  "environment": "development"
}
```

Gagal (503) ketika salah satu dependency mati:

```json
{
  "detail": {
    "status": "degraded",
    "postgres": "ok",
    "redis": "down"
  }
}
```

### 4. `GET /api/v1/modules` — Modul Platform

```bash
curl http://localhost:8000/api/v1/modules
```

```json
{
  "total": 3,
  "data": [
    {
      "id": "chemsphere",
      "name": "ChemSphere Engine",
      "description": "Mesin kimia interaktif: tabel periodik, visualisasi molekul 3D, dan sandbox reaksi.",
      "features": [
        "Interactive Periodic Table",
        "3D Molecular Visualizer",
        "Chemical Reaction Sandbox"
      ]
    },
    {
      "id": "forensilab",
      "name": "ForensiLab",
      "description": "Gamifikasi forensik dan biokimia berbasis studi kasus.",
      "features": [
        "Interactive Crime Scene & Evidence Board",
        "Virtual Lab Mini-Games (toksikologi, TLC, spektroskopi, serologi, DNA fingerprinting)",
        "Dynamic Feedback System"
      ]
    },
    {
      "id": "anatomimed",
      "name": "AnatomiMed & Virtual Patient Simulator",
      "description": "Penjelajahan anatomi 3D berlapis dan simulasi diagnosis pasien virtual.",
      "features": [
        "3D Body Dissection Viewer",
        "Virtual Patient Simulator (anamnesis, pemeriksaan fisik, uji lab)",
        "Pathophysiology & Drug Simulator"
      ]
    }
  ]
}
```

---

## Konvensi

- **Base URL:** `http://localhost:8000`
- **Format:** JSON, UTF-8
- **CORS:** izin dibaca dari `CORS_ORIGINS` (default `http://localhost:5173`, `http://localhost:3000`)
- **Kode status:** `200` sukses · `503` dependency tidak siap · `404` path tidak ditemukan · `422` body/parameter tidak valid
- **Skema error standar:** `{"detail": "..."}`

## Regenerasi Snapshot Spec

Jalankan setelah mengubah endpoint agar `docs/openapi.json` selalu sinkron:

```bash
cd backend/python
python -c "import json; from main import app; open(r'../../docs/openapi.json','w',encoding='utf-8').write(json.dumps(app.openapi(), indent=2, ensure_ascii=False))"
```
