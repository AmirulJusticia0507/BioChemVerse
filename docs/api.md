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
| POST | `/api/v1/auth/register` | auth | Daftar akun baru (bcrypt) | 201 | 409 |
| POST | `/api/v1/auth/login` | auth | Login → JWT Bearer (12 jam) | 200 | 401 |
| GET | `/api/v1/auth/me` | auth | Profil pengguna aktif (butuh token) | 200 | 401 |
| GET | `/api/v1/progress` | progress | Semua progres modul pengguna aktif | 200 | 401 |
| GET | `/api/v1/progress/{module}` | progress | Progres satu modul | 200 | 400/401/404 |
| PUT | `/api/v1/progress/{module}` | progress | Upsert progres (score/completed) | 200 | 400/401/422 |

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

## Autentikasi (JWT)

Semua endpoint tag `auth` memakai body JSON (bukan form).

### `POST /api/v1/auth/register` → 201

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"student1","email":"siswa@contoh.com","password":"rahasia123"}'
```

```json
{
  "id": "…uuid…",
  "username": "student1",
  "email": "siswa@contoh.com",
  "role": "student",
  "created_at": "2026-10-29T10:00:00+00:00"
}
```

`409 Conflict` bila username/email sudah terdaftar · `422` bila password < 8 karakter.

### `POST /api/v1/auth/login` → 200

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"student1","password":"rahasia123"}'
```

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9…",
  "token_type": "bearer",
  "user": { "id": "…uuid…", "username": "student1", "email": "…", "role": "student", "created_at": "…" }
}
```

`401 Unauthorized` bila kredensial salah.

### `GET /api/v1/auth/me` → 200

```bash
curl http://localhost:8000/api/v1/auth/me -H "Authorization: Bearer <access_token>"
```

`401` bila token tidak ada, tidak valid, palsu, atau kedaluwarsa.

> **Token:** HS256, berlaku **12 jam**, `sub` = UUID pengguna. `JWT_SECRET` wajib ≥ 32 karakter.

---

## Progres Modul (JWT)

Modul yang valid: `chemsphere`, `forensilab`, `anatomimed`.

### `GET /api/v1/progress` → 200

```bash
curl http://localhost:8000/api/v1/progress -H "Authorization: Bearer <token>"
```

```json
{
  "total": 2,
  "data": [
    { "module": "chemsphere", "score": 50, "completed": true, "updated_at": "2026-10-29T03:01:11+00:00" },
    { "module": "forensilab", "score": 90, "completed": true, "updated_at": "2026-10-29T03:01:11+00:00" }
  ]
}
```

### `PUT /api/v1/progress/{module}` → 200 (upsert)

```bash
curl -X PUT http://localhost:8000/api/v1/progress/chemsphere \
  -H "Authorization: Bearer <token>" -H "Content-Type: application/json" \
  -d '{"score": 50}'
```

```json
{ "module": "chemsphere", "score": 50, "completed": false, "updated_at": "2026-10-29T03:01:11+00:00" }
```

Field yang **tidak dikirim dipertahankan** (mis. kirim `{"completed": true}` saja → `score` tetap).

### `GET /api/v1/progress/{module}` → 200 / 404

`404` bila pengguna belum pernah menyimpan progres modul tersebut.
`400` bila kode modul tidak dikenal · `422` bila `score` di luar `0–1000000`.

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
