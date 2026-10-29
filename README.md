# 🧪 BioChemVerse

> **An Interactive Ecosystem for Chemistry, Forensic Science, and 3D Human Anatomy Simulation.**

**BioChemVerse** adalah platform edukasi berbasis web yang memadukan simulasi reaksi kimia, gim investigasi forensik, dan simulasi anatomi & diagnosis pasien 3D. Project ini mengintegrasikan visualisasi molekuler interaktif, mesin simulasi biokimia, serta sistem pembelajaran berbasis studi kasus nyata.

---

## 🌟 Fitur Utama & Modul System

Platform ini terdiri dari 3 modul utama yang saling terhubung:

### 1. ⚛️ ChemSphere Engine

- **Interactive Periodic Table:** Katalog data unsur dan parameter molekuler lengkap.
- **3D Molecular Visualizer:** Render visualisasi struktur molekul dan ikatan kimia secara interaktif.
- **Chemical Reaction Sandbox:** Simulasi pencampuran senyawa kimia dengan reaksi visual *real-time*.

### 2. 🔍 ForensiLab (Gamifikasi Forensik & Bio-Kimia)

- **Interactive Crime Scene & Evidence Board:** Papan bukti berbasis *graph node* untuk menghubungkan bukti sains, alibi, dan fakta kasus.
- **Virtual Lab Mini-Games:**
  - Toksikologi & Uji Reagen Kimia (Uji Racun/Senyawa)
  - Kromatografi Lapis Tipis (TLC) & Spektroskopi
  - Serologi Darah & *DNA Fingerprinting*
- **Dynamic Feedback System:** Penjelasan mekanisme biokimia saat eksperimen gagal/berhasil.

### 3. 🩺 AnatomiMed & Virtual Patient Simulator

- **3D Body Dissection Viewer:** Eksplorasi anatomi manusia multi-layer (Kulit, Otot, Tulang, Sistem Saraf, Kardiovaskular, Organ).
- **Virtual Patient Simulator:**
  - Anamnesis (pemeriksaan keluhan pasien)
  - Pemeriksaan fisik & tanda vital (Tekanan Darah, Nadi, SpO₂, Suhu)
  - Stetoskop virtual & uji lab biokimia darah
- **Pathophysiology & Drug Simulator:** Visualisasi reaksi obat dan mekanisme penyakit pada skala organ/seluler.

---

## 🛠️ Tech Stack & Architecture

- **Frontend:** Vue 3 / React.js (Vite), Tailwind CSS
- **3D Engine:** Three.js / React Three Fiber (`.glb` / `.gltf` model)
- **Interactive Canvas:** HTML5 Canvas / Pixi.js
- **Backend Engine:** Node.js (Express / NestJS) / Python (FastAPI)
- **Database & Cache:** PostgreSQL (Case Data & Medical Rules), Redis (Session State)
- **Data Standards:** ICD-10 (Disease Codes), FMA (Foundational Model of Anatomy)

---

## 🚀 Panduan Memulai (Quick Start)

### Prasyarat

- Node.js versi >= 18.x
- PostgreSQL versi >= 14

### Instalasi & Setup

1. **Clone Repositori:**

   ```bash
   git clone https://github.com/AmirulJusticia0507/biochemverse.git
   cd biochemverse
   ```

2. **Instalasi Dependency:**

   ```bash
   npm install
   ```

3. **Konfigurasi Environment (`.env`):**

   Salin `.env.example` menjadi `.env` dan sesuaikan nilainya:

   ```env
   PORT=5000
   DATABASE_URL=postgresql://user:password@localhost:5432/biochemverse
   JWT_SECRET=your_secret_key
   ```

4. **Jalankan Mode Development:**

   ```bash
   npm run dev
   ```

   Aplikasi dapat diakses di `http://localhost:3000`.

---

## 📂 Struktur Repositori

```
biochemverse/
├── apps/
│   ├── web/                     # Frontend Vue/React Application
│   └── api/                     # Backend API & Logic Engine
├── packages/
│   ├── chemsphere-core/         # Module 1: Chemistry & Molecular Engine
│   ├── forensilab-engine/       # Module 2: Case Narrative & Evidence Graph
│   └── anatomimed-3d/           # Module 3: 3D Anatomy & Patient Simulator
└── docs/                        # Dokumentasi Sistem & API Specs
```

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah MIT License.
filePath">
C:\laragon\www\BioChemVerse\README.md