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
| POST | `/api/v1/auth/forgot-password` | auth | Kirim tautan reset tanpa membocorkan status email | 202 | — |
| POST | `/api/v1/auth/reset-password` | auth | Atur password baru dengan token sekali pakai (1 jam) | 200 | 400 |
| POST | `/api/v1/auth/login` | auth | Login → JWT Bearer (12 jam) | 200 | 401 |
| GET | `/api/v1/auth/me` | auth | Profil pengguna aktif (butuh token) | 200 | 401 |
| GET | `/api/v1/progress` | progress | Semua progres modul pengguna aktif | 200 | 401 |
| GET | `/api/v1/progress/{module}` | progress | Progres satu modul | 200 | 400/401/404 |
| PUT | `/api/v1/progress/{module}` | progress | Upsert progres (score/completed) | 200 | 400/401/422 |
| GET | `/api/v1/elements` | elements | Daftar 118 unsur + filter (q/kategori/periode/blok/fase) | 200 | 422 |
| GET | `/api/v1/elements/{simbol\|nomor}` | elements | Detail satu unsur (mis. `Fe` atau `26`) | 200 | 404 |
| GET | `/api/v1/categories` | elements | 10 kategori tabel periodik + jumlah unsur | 200 | — |
| GET | `/api/v1/ions` | elements | 30 ion poliatomik (rumus & muatan) | 200 | — |
| POST | `/api/v1/quiz/start` | quiz | Bangkitkan soal kuis (kunci disimpan server-side) | 200 | 400/401/422/503 |
| POST | `/api/v1/quiz/submit` | quiz | Nilai jawaban + simpan percobaan (sesi sekali pakai) | 200 | 400/401/403/404 |
| GET | `/api/v1/quiz/attempts` | quiz | Riwayat percobaan kuis (`limit` 1–100) | 200 | 401 |
| GET | `/api/v1/bookmarks` | bookmarks | Daftar unsur yang dibookmark | 200 | 401 |
| POST | `/api/v1/bookmarks` | bookmarks | Tambah bookmark unsur | 201 | 401/409/422 |
| DELETE | `/api/v1/bookmarks/{nomor}` | bookmarks | Hapus bookmark berdasarkan nomor atom | 204 | 401/404 |

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

## Tabel Periodik (ChemSphere)

Data referensi 118 unsur (nama Indonesia), 10 kategori, dan 30 ion poliatomik.
Di-seed otomatis saat startup dari `backend/python/data/*.json`.

### `GET /api/v1/elements` → 200

Parameter query (semua opsional, boleh dikombinasikan):

| Param | Tipe | Contoh | Keterangan |
| --- | --- | --- | --- |
| `q` | string | `Fe` / `26` | Nama, nama Latin, simbol, atau nomor atom |
| `category` | string | `transition` | Slug kategori |
| `period` | int 1-7 | `4` | Periode |
| `block` | `s\|p\|d\|f` | `d` | Blok elektron |
| `phase` | `solid\|liquid\|gas\|artificial` | `solid` | Fase pada suhu ruang |

```bash
curl "http://localhost:8000/api/v1/elements?q=Fe"
```

```json
{
  "total": 2,
  "data": [
    {
      "atomic_number": 26,
      "symbol": "Fe",
      "name": "Besi",
      "name_latin": "Ferrum",
      "atomic_mass": 55.845,
      "category": { "slug": "transition", "name": "Logam Transisi", "element_count": 38 },
      "period": 4,
      "group": 8,
      "description": "Logam transisi paling banyak digunakan; inti Bumi sebagian besar tersusun dari besi.",
      "uses": "Konstruksi, baja, kendaraan, dan hemoglobin.",
      "hazard": "Umumnya aman; kelebihan zat besi dapat merusak organ.",
      "properties": { "melt": 1811, "boil": 3134, "block": "d", "phase": "Solid", "shells": [2, 8, 14, 2] }
    }
  ]
}
```

### `GET /api/v1/elements/{simbol|nomor}` → 200 / 404

```bash
curl http://localhost:8000/api/v1/elements/Fe   # atau /api/v1/elements/26
```

404 bila unsur tidak dikenal: `{ "detail": "Unsur 'Xx' tidak ditemukan" }`.

### `GET /api/v1/categories` → 200

```bash
curl http://localhost:8000/api/v1/categories
```

```json
{
  "total": 10,
  "data": [{ "slug": "alkali", "name": "Logam Alkali", "element_count": 6 }]
}
```

### `GET /api/v1/ions` → 200

```bash
curl http://localhost:8000/api/v1/ions
```

```json
{
  "total": 30,
  "data": [{ "name": "Amonium", "formula": "NH₄⁺", "charge": "+1", "description": "Kation poliatomik ..." }]
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

## Kuis Unsur

Soal **dibangkitkan di server** dari data 118 unsur — kunci jawaban **tidak pernah** dikirim
sebelum dinilai. Kunci disimpan di Redis (`quiz:<id>`, TTL 1 jam) dan **sekali pakai**:
submit kedua untuk `quiz_id` yang sama → `404`.

**Topik:** `simbol` · `nomor-atom` · `kategori` · `golongan-periode` · `campuran`
**Jumlah soal:** `1`–`30` (default `10`).

### `POST /api/v1/quiz/start` → 200

```bash
curl -X POST http://localhost:8000/api/v1/quiz/start \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"topic": "campuran", "count": 3}'
```

```json
{
  "quiz_id": "kq3v0YQ2bX...",
  "topic": "campuran",
  "questions": [
    {
      "id": "0",
      "question": "Unsur Kripton (Kr) termasuk kategori apa?",
      "options": ["Lantanida", "Logam Transisi", "Gas Mulia", "Metaloid"]
    }
  ]
}
```

`400` topik tidak dikenal · `503` data unsur kurang/Redis mati.

### `POST /api/v1/quiz/submit` → 200

```bash
curl -X POST http://localhost:8000/api/v1/quiz/submit \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"quiz_id": "kq3v0YQ2bX...", "answers": ["Gas Mulia"], "duration_sec": 42}'
```

```json
{
  "attempt_id": 1,
  "topic": "campuran",
  "total": 3,
  "correct": 1,
  "score": 33,
  "results": [
    { "index": 0, "correct": "Gas Mulia", "given": "Gas Mulia", "is_correct": true }
  ]
}
```

`score` = persentase bulat (`correct / total * 100`).
`400` jumlah jawaban ≠ jumlah soal · `403` sesi milik pengguna lain · `404` sesi tidak ada/kedaluwarsa.

### `GET /api/v1/quiz/attempts?limit=10` → 200

```json
{
  "total": 1,
  "data": [
    { "id": 1, "topic": "campuran", "total": 3, "correct": 1, "score": 33,
      "duration_sec": 42, "created_at": "2026-10-29T04:53:00+00:00" }
  ]
}
```

---

## Bookmark Unsur

Semua endpoint butuh token.

### `POST /api/v1/bookmarks` → 201

```bash
curl -X POST http://localhost:8000/api/v1/bookmarks \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"atomic_number": 26, "note": "Logam transisi"}'
```

```json
{ "atomic_number": 26, "symbol": "Fe", "name": "Besi", "note": "Logam transisi",
  "created_at": "2026-10-29T04:53:00+00:00" }
```

`409` sudah dibookmark · `422` `atomic_number` di luar `1–118`.

### `GET /api/v1/bookmarks` → 200

```json
{ "total": 2, "data": [ { "atomic_number": 8, "symbol": "O", "name": "Oksigen", "note": null, "created_at": "…" } ] }
```

### `DELETE /api/v1/bookmarks/{nomor}` → 204

`404` bila bookmark tidak ada.

---

- **Base URL:** `http://localhost:8000`
- **Format:** JSON, UTF-8
- **CORS:** izin dibaca dari `CORS_ORIGINS` (default `http://localhost:5173`, `http://localhost:3000`). Mode development (`ENV` selain `production`/`staging`) juga mengizinkan semua origin `http://localhost:<port apa pun>` & `http://127.0.0.1:<port>` — misal Vite yang pindah ke `:5174`.
- **Kode status:** `200` sukses · `503` dependency tidak siap · `404` path tidak ditemukan · `422` body/parameter tidak valid
- **Skema error standar:** `{"detail": "..."}`

## Regenerasi Snapshot Spec

Jalankan setelah mengubah endpoint agar `docs/openapi.json` selalu sinkron:

```bash
cd backend/python
python -c "import json; from main import app; open(r'../../docs/openapi.json','w',encoding='utf-8').write(json.dumps(app.openapi(), indent=2, ensure_ascii=False))"
```
