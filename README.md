# 🧪 BioChemVerse

> **An Interactive Ecosystem for Chemistry, Forensic Science, and 3D Human Anatomy Simulation.**

**BioChemVerse** adalah platform edukasi berbasis web yang memadukan simulasi reaksi kimia, gim investigasi forensik, dan simulasi anatomi & diagnosis pasien 3D. Project ini mengintegrasikan visualisasi molekuler interaktif, mesin simulasi biokimia, serta sistem pembelajaran berbasis studi kasus nyata.

---

## 🌟 Fitur Utama & Modul Sistem

Platform ini terdiri dari 3 modul utama yang saling terhubung:

### 1. ⚛️ ChemSphere Engine

- **Interactive Periodic Table:** Katalog data unsur dan parameter molekuler lengkap.
- **3D Molecular Visualizer:** Render visualisasi struktur molekul dan ikatan kimia secara interaktif.
- **Chemical Reaction Sandbox:** Simulasi pencampuran senyawa kimia dengan reaksi visual *real-time*.

### 2. 🔍 ForensiLab (Gamifikasi Forensik & Bio-Kimia)

- **Interactive Crime Scene & Evidence Board:** Papan bukti berbasis *graph node* untuk menghubungkan bukti sains, alibi, dan fakta kasus.
- **Virtual Lab Mini-Games:** Toksikologi & uji reagen, Kromatografi Lapis Tipis (TLC) & spektroskopi, serologi darah & *DNA fingerprinting*.
- **Dynamic Feedback System:** Penjelasan mekanisme biokimia saat eksperimen gagal/berhasil.

### 3. 🩺 AnatomiMed & Virtual Patient Simulator

- **3D Body Dissection Viewer:** Eksplorasi anatomi manusia multi-layer (kulit, otot, tulang, sistem saraf, kardiovaskular, organ).
- **Virtual Patient Simulator:** Anamnesis, pemeriksaan fisik & tanda vital, stetoskop virtual & uji lab biokimia darah.
- **Pathophysiology & Drug Simulator:** Visualisasi reaksi obat dan mekanisme penyakit pada skala organ/seluler.

---

## 🛠️ Tech Stack

| Lapisan | Teknologi |
| --- | --- |
| Frontend | Vue 3 + Vite + Tailwind CSS 4 (`frontend/`) |
| Backend utama | Python FastAPI + Uvicorn, asyncpg (PostgreSQL), redis-py (`backend/python/`) |
| Backend sekunder | Go stdlib `net/http` — health/readiness (`backend/go/`) |
| Database & Cache | PostgreSQL 16, Redis 7 |
| Infrastruktur lokal | Service lokal (mis. Laragon) **atau** `docker-compose.yml` |
| CI/CD | GitHub Actions (`.github/workflows/`) |
| Data standards | ICD-10 (kode penyakit), FMA (anatomi) |

> Detail arsitektur: [`architecture/overview.md`](architecture/overview.md) ·
> Design system: [`design/design-system.md`](design/design-system.md) ·
> Dokumentasi API: [`docs/api.md`](docs/api.md) ·
> Materi anatomi: [`docs/anatomy.md`](docs/anatomy.md)

---

## 🚀 Panduan Memulai (Quick Start)

### Prasyarat

- Node.js ≥ 18
- Python ≥ 3.11
- PostgreSQL ≥ 14 **dan** Redis (service lokal) — atau Docker untuk `docker-compose.yml`
- (Opsional) Go ≥ 1.22 untuk server health-check Go

### 1. Clone Repositori

```bash
git clone https://github.com/AmirulJusticia0507/biochemverse.git
cd biochemverse
```

### 2. Konfigurasi Environment

```bash
cp .env.example .env      # Windows: copy .env.example .env
```

Sesuaikan `DATABASE_URL`, `REDIS_URL`, `CORS_ORIGINS`, dan `JWT_SECRET`.

### 3. Jalankan Infrastruktur

Pakai **salah satu**:

```bash
# Opsi A — service lokal sudah berjalan (mis. Laragon): biarkan saja
# Opsi B — Docker
docker compose up -d
```

Database `biochemverse` dibuat otomatis saat API pertama kali start.

### 4. Jalankan Backend (port 8000)

```bash
cd backend/python
pip install -r requirements.txt
uvicorn main:app --reload
```

- Swagger UI: <http://localhost:8000/docs>
- Readiness: <http://localhost:8000/health/ready>

### 5. Jalankan Frontend (port 5173)

```bash
cd frontend
npm install
npm run dev
```

Aplikasi terbuka di `http://localhost:5173`.

### 6. (Opsional) Server Go — health check (port 8001)

```bash
cd backend/go
go run .
```

---

## 📂 Struktur Repositori

```
biochemverse/
├── frontend/                 # Vue 3 + Vite + Tailwind (SPA)
│   └── src/                  # App.vue, components/, assets/
├── backend/
│   ├── python/               # FastAPI — API utama + schema.sql
│   └── go/                   # Server health/readiness Go
├── architecture/             # Dokumentasi arsitektur
├── design/                   # Design system
├── docs/                     # API docs, OpenAPI snapshot, materi anatomi
├── skills/                   # Skills untuk agent
├── .github/workflows/        # CI (build + smoke test) & CD (packaging)
├── docker-compose.yml        # PostgreSQL + Redis
├── AGENTS.md                 # Aturan kerja agent
└── TODO.md                   # Status task
```

---

## ✅ Status

| Area | Status |
| --- | --- |
| Scaffolding frontend & backend | ✅ |
| PostgreSQL + Redis (koneksi, skema, readiness) | ✅ |
| Dokumentasi API (OpenAPI/Swagger) | ✅ |
| CI/CD (GitHub Actions) | ✅ |
| Auth JWT, router Vue, endpoint modul | ⏳ |
| ChemSphere / ForensiLab / AnatomiMed (fitur inti) | ⏳ |

Lihat [`TODO.md`](TODO.md) untuk daftar task terkini.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah MIT License.
