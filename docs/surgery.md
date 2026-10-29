# Operasi (Ruang Bedah Edukatif) — AnatomiMed

Menu **Operasi** (`/operasi`) di frontend mengajarkan prosedur bedah beserta visual 3D tata letaknya.
Halaman ini murni frontend (tanpa endpoint baru) dan bersifat **edukatif**, bukan panduan klinis.

## Struktur berkas

| Berkas | Isi |
| --- | --- |
| `frontend/src/views/SurgeryView.vue` | Halaman: daftar prosedur, detail, langkah, risiko, visual 3D |
| `frontend/src/data/surgery.js` | Data 5 prosedur (ringkasan, tujuan, peralatan, langkah, risiko, perbandingan) |
| `frontend/src/three/surgeryPresets.js` | Preset 3D per prosedur: organ, port/trokar, instrumen, posisi kamera |
| `frontend/src/three/surgeryScenes.js` | Pembangun scene Three.js: dinding perut, organ, trokar, laparoskop, instrumen |
| `frontend/src/components/surgery/SurgeryViewer.vue` | Canvas WebGL: orbit, zoom, reset kamera, putar otomatis |

## Daftar prosedur

| ID | Prosedur | Pendekatan | Inti materi |
| --- | --- | --- | --- |
| `laparoskopi` | Laparoskopi | Minimal invasif | Prinsip umum: insufflasi CO₂, 3–5 port, eksplorasi & tindakan |
| `apendektomi` | Apendektomi | Terbuka (McBurney) & laparoskopi | Perbandingan dua teknik, ligasi mesoapendiks, endobag |
| `kolesistektomi` | Kolesistektomi | Laparoskopi (standar) | Critical view of safety, klip duktus & arteri sistika |
| `herniorafi` | Herniorafi Inguinalis | Terbuka (Lichtenstein) & TAPP/TEP | Penempatan mesh tanpa tegangan, hindari saraf |
| `seksio` | Seksio Sesarea | Laparotomi transperitoneal | Pfannenstiel, insisi uterus, lahirkan bayi & plasenta |

## Cara kerja visual 3D

1. Setiap prosedur di `surgery.js` punya properti `scene` → kunci ke `surgeryScenes` di `surgeryPresets.js`.
2. `buildSurgeryScene(preset)` menyusun:
   - **Dinding perut**: setengah bola (kubah) dengan tepi iris terbuka + rongga gelap di dalamnya.
   - **Organ** sesuai preset: `liver`, `gallbladder`, `appendix`, `bowel`, `stomach`, `uterus`, `mesh`, `fascia`.
   - **Port**: `trocar` (tabung logam + keran gas) atau `scope` (laparoskop dengan lensa bercahaya).
   - **Instrumen**: grasper atau hook, masuk miring dari tepi dinding.
3. `SurgeryViewer.vue` merender dengan `OrbitControls`; kamera diatur dari `preset.camera`
   (posisi miring ke dalam rongga perut, meniru sudut laparoskop).

### Konvensi koordinat

`x` = kanan pasien, `y` = kranial, `z` = anterior, satuan "dm". Contoh port umbilikus:
`[0, -0.6, 2.0]` dengan rotasi `[0.35, 0, 0]` — instrumen masuk dari depan-bawah ke dalam rongga.

### Menambah prosedur baru

1. Tambah entri di `surgeryProcedures` (`frontend/src/data/surgery.js`) dengan `scene: '<id>'`.
2. Tambah preset di `surgeryScenes` (`frontend/src/three/surgeryPresets.js`).
3. Bila perlu organ baru, tambah builder di `surgeryScenes.js` lalu daftarkan di `organLayer()`.

## Catatan lisensi & etika

- Semua geometri 3D dibuat di kode dengan Three.js — tanpa aset model pihak ketiga.
- Visual bersifat **skematik-realistis** (bukan fotorealistik, bukan citra pasien).
- Konten wajib memuat peringatan "materi edukatif, bukan panduan klinis".
