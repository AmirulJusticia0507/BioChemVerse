# 🏗️ Arsitektur BioChemVerse

Dokumen ini menjelaskan struktur sistem, alur data, dan keputusan arsitektur proyek.

---

## 1. Gambaran Besar

```
┌──────────────────────────────┐
│  Frontend — Vue 3 SPA (Vite) │   port 5173 (dev)
│  Tailwind CSS v4             │
└──────────────┬───────────────┘
               │  HTTP/JSON  (CORS dari env CORS_ORIGINS)
               ▼
┌──────────────────────────────┐        ┌────────────┐
│  Backend — Python FastAPI    │◀──────▶│   Redis    │   port 6379
│  port 8000                   │  cache │  (session) │
│  ├─ /health  /health/ready   │        └────────────┘
│  └─ /api/v1/...              │
└──────────────┬───────────────┘
               │  SQL (asyncpg, connection pool)
               ▼
        ┌─────────────┐
        │ PostgreSQL  │  port 5432
        │ (data utama)│
        └─────────────┘

┌──────────────────────────────┐
│  Backend — Go (stdlib)       │   port 8001
│  /health  /health/ready      │   server ringan, cek TCP ke PG & Redis
└──────────────────────────────┘
```

---

## 2. Modul Fungsional

| Modul | Nama | Isi |
| --- | --- | --- |
| 1 | **ChemSphere Engine** | Tabel periodik interaktif, visualisasi molekul 3D, sandbox reaksi |
| 2 | **ForensiLab** | Crime scene & evidence board, mini-game lab (toksikologi, TLC, serologi, DNA), feedback biokimia |
| 3 | **AnatomiMed** | 3D body dissection multi-layer, virtual patient simulator, simulator obat/patofisiologi |

Ketiga modul dikonsumsi lewat API berprefix `/api/v1/` (lihat [docs/api.md](../docs/api.md)).

---

## 3. Struktur Repositori (aktual)

```
BioChemVerse/
├── AGENTS.md                    # aturan kerja agent (wajib commit & push per task)
├── TODO.md                      # daftar task + status
├── README.md                    # visi & panduan singkat
├── .env.example                 # template konfigurasi environment
├── .gitignore
├── docker-compose.yml           # PostgreSQL 16 + Redis 7 (alternatif service lokal)
├── .github/workflows/
│   ├── ci.yml                   # build FE, smoke test BE, go vet/build
│   └── cd.yml                   # packaging artefak rilis
├── architecture/overview.md     # dokumen ini
├── design/design-system.md      # token warna, tipografi, komponen UI
├── docs/
│   ├── api.md                   # dokumentasi endpoint
│   ├── openapi.json             # snapshot spesifikasi OpenAPI
│   └── anatomy.md               # materi 12 sistem organ tubuh
├── skills/README.md             # skills untuk agent
├── backend/
│   ├── python/                  # FastAPI (API utama)
│   │   ├── main.py              # titik masuk, lifespan, routes
│   │   ├── config.py            # settings dari env/.env
│   │   ├── db.py                # pool asyncpg + bootstrap skema
│   │   ├── cache.py             # koneksi Redis (RESP2)
│   │   ├── models.py            # skema Pydantic (sumber OpenAPI)
│   │   └── schema.sql           # DDL awal (users, user_progress)
│   └── go/                      # server health-check Go (stdlib)
│       ├── main.go
│       └── go.mod
└── frontend/                    # Vue 3 + Vite + Tailwind v4 (SPA)
    └── src/
        ├── App.vue              # shell: header (nav + auth) + router-view
        ├── router/index.js      # rute: /, /modules, /login, /register, 404
        ├── api/client.js        # fetch wrapper + token JWT di localStorage
        ├── composables/useAuth.js  # state login global (tanpa Pinia)
        ├── views/               # HomeView, ModulesView, LoginView, RegisterView, NotFound
        ├── style.css            # @import "tailwindcss" + kelas .nav-link
        └── components/          # AnatomyBody.vue (ilustrasi anatomi)
```

---

## 4. Tech Stack

| Lapisan | Teknologi | Alasan |
| --- | --- | --- |
| Frontend | Vue 3.5 + Vite 8 + Tailwind CSS 4 | ringan, HMR cepat, utility-first styling |
| 3D (rencana) | Three.js / React Three Fiber, model `.glb` | render anatomi & molekul |
| API | Python FastAPI + Uvicorn | async native, OpenAPI otomatis |
| Akses DB | asyncpg (connection pool) | PostgreSQL async tercepat di ekosistem Python |
| Cache/state | redis-py (asyncio, RESP2) | kompatibel Redis lama & baru |
| Server sekunder | Go (stdlib `net/http`) | health/readiness ringan, tanpa dependensi |
| Data | PostgreSQL 16, Redis 7 | case data & medical rules; session state |
| Standar data | ICD-10, FMA | kode penyakit & anatomi |
| CI/CD | GitHub Actions | build, smoke test, packaging artefak |

---

## 5. Alur Request Tipikal

1. Browser memuat SPA hasil build Vite (dev: `http://localhost:5173`).
2. SPA memanggil API `http://localhost:8000/api/v1/...` (CORS diizinkan via `CORS_ORIGINS`).
3. FastAPI memvalidasi request dengan model Pydantic → query asyncpg ke PostgreSQL.
4. Hasil disimpan di Redis (cache/sesi) bila mempercepat respons.
5. Respon JSON dikembalikan; skema OpenAPI selalu sinkron dengan kode.

**Startup (lifespan):** `ensure_database()` → buat DB bila belum ada → buat pool → eksekusi `schema.sql` (idempoten) → sambungkan Redis.

**Readiness:** `GET /health/ready` mengembalikan `503 degraded` bila PostgreSQL atau Redis tidak merespons.

---

## 6. Basis Data

Didefinisikan di [`backend/python/schema.sql`](../backend/python/schema.sql):

- **users** — `id (uuid)`, `username`, `email`, `password_hash`, `role`, timestamps
- **user_progress** — progres belajar per modul (`chemsphere` / `forensilab` / `anatomimed`), `score`, `completed`, unique `(user_id, module)`

---

## 7. Environment

Semua konfigurasi lewat environment / file `.env` (salin dari `.env.example`):

| Variabel | Default | Fungsi |
| --- | --- | --- |
| `PORT` | `8000` | port API Python (Go: `8001`) |
| `DATABASE_URL` | `postgresql://postgres@localhost:5432/biochemverse` | koneksi PostgreSQL |
| `REDIS_URL` | `redis://localhost:6379/0` | koneksi Redis |
| `CORS_ORIGINS` | `http://localhost:5173,http://localhost:3000` | origin yang diizinkan |
| `JWT_SECRET` | *(wajib diganti)* | tanda tangan token JWT |
| `ENV` | `development` | environment aktif |

---

## 8. Keputusan Arsitektur

- **Satu API utama (FastAPI)** — dokumentasi OpenAPI otomatis, tim satu bahasa untuk logika bisnis.
- **Go terpisah & tanpa dependensi** — dipakai untuk health/readiness ringan dan eksperimen performa, bukan logika bisnis.
- **Skema idempoten saat startup** — `schema.sql` seluruhnya `IF NOT EXISTS`, aman dijalankan berulang di CI.
- **Service lokal maupun Docker** — `docker-compose.yml` disediakan, tetapi bila service lokal (Laragon) sudah jalan, pakai itu.
- **RESP2 untuk Redis** — agar kompatibel dengan Redis 3.x milik instalasi lokal.

---

## 9. Peta Jalan

| Fase | Isi | Status |
| --- | --- | --- |
| 0 | Scaffolding FE/BE, materi anatomi | ✅ selesai |
| 1 | PostgreSQL + Redis, OpenAPI, CI/CD, Tailwind aktif | ✅ selesai |
| 2 | Router Vue, autentikasi JWT, endpoint CRUD modul | ✅ selesai |
| 3 | ChemSphere: tabel periodik + visualisasi molekul 3D | ⏳ berikutnya |
| 4 | ForensiLab: evidence graph + mini-game lab | ⏳ |
| 5 | AnatomiMed: viewer 3D multi-layer + simulasi pasien | ⏳ |
