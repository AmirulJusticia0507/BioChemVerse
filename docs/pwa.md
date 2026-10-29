# PWA — BioChemVerse

Aplikasi web BioChemVerse dapat dipasang (installable) dan tetap bisa dibuka saat
jaringan putus (offline-ready) menggunakan service worker Workbox.

## Ringkasan

| Aspek | Implementasi |
| --- | --- |
| Plugin | `vite-plugin-pwa` v2 (`generateSW`) |
| Strategi update | `registerType: 'prompt'` — pengguna memilih kapan memuat ulang |
| Tampilan | `display: standalone`, `orientation: portrait-primary` |
| Warna | `theme_color`/`background_color` = `#0f172a` |
| Bahasa | `lang: id` |

## Berkas utama

- `frontend/vite.config.js` — manifest + konfigurasi Workbox.
- `frontend/index.html` — meta PWA (`theme-color`, `apple-mobile-web-app-*`, `apple-touch-icon`).
- `frontend/src/composables/usePwa.js` — penangkapan `beforeinstallprompt`, tombol pasang, deteksi iOS.
- `frontend/src/composables/usePwaState.js` — status online/offline dan kesiapan update.
- `frontend/src/components/PwaStatus.vue` — UI status di sidebar.
- `frontend/src/App.vue` — registrasi service worker (`virtual:pwa-register`) dan listener jaringan.
- `frontend/public/icons/` — ikon 192/512, maskable 512, apple-touch-icon, dan sumber `app-icon.svg`.
- `frontend/scripts/gen-pwa-icons.mjs` — generator PNG dari `app-icon.svg`.

Membuat ulang ikon setelah mengubah `app-icon.svg`:

```bash
cd frontend
node scripts/gen-pwa-icons.mjs
```

## Strategi caching

| Permintaan | Handler | Catatan |
| --- | --- | --- |
| Navigasi (HTML) | Precache + `navigateFallback: /index.html` | Router menentukan halaman; rute dalam seperti `/tabel-periodik` tetap jalan offline. |
| Aset build (JS/CSS/SVG/PNG/font) | Precache saat install | ~33 entri (±1 MB); berkas > 3 MB tidak diprecache. |
| Aset statis lintas-origin (`script`/`style`/`font`/`image`) | `CacheFirst` (`bcv-assets`, 200 entri, 30 hari) | Mempercepat pemuatan ulang. |
| `/api/*` | `NetworkOnly` | Data pengguna (progres, kuis, auth) **tidak pernah** dari cache. |

Model 3D berukuran besar sengaja tidak diprecache agar instalasi tetap ringan.

## Alur instalasi

1. **Chromium/Android** — event `beforeinstallprompt` ditangkap (dan `preventDefault`
   dipanggil untuk mematikan mini-infobar bawaan). Tombol **Pasang aplikasi** muncul di
   sidebar; klik memanggil `prompt()` lalu membaca `userChoice`. Tombol hilang setelah
   dipilih/ditutup atau ketika muncul `appinstalled`.
2. **iOS/Safari** — tidak ada event instalasi, jadi ditampilkan petunjuk manual:
   **Bagikan → Tambah ke Layar Utama**.
3. **Sudah terpasang** (`display-mode: standalone`) — tombol dan petunjuk disembunyikan.

> Catatan teknis: nama event disimpan di konstanta `INSTALL_EVENT` dan `prompt()` disimpan
> sebagai fungsi terpisah. Minifier dapat menulis ulang literal yang memuat nama global
> `window` (mis. di dalam `typeof window !== 'undefined'`), yang pernah merusak nama event.

## Alur update

1. Service worker baru terpasang dan menunggu (`waiting`).
2. `registerSW({ onNeedRefresh })` menyalakan `updateReady`, sehingga sidebar menampilkan
   kartu **Versi baru tersedia** — aplikasi tidak di-reload paksa.
3. Tombol **Muat ulang** memanggil `applyUpdate(true)`, service worker baru aktif, halaman dimuat ulang.

## Status offline

- Badge **Mode offline — konten dari cache** muncul saat event `offline` dan hilang saat `online`.
- Nilai awal diambil dari `navigator.onLine` saat halaman dibuka.

## Menguji

```bash
cd frontend
npm run build
npm run preview      # PWA hanya aktif di hasil build, bukan npm run dev
```

1. Buka `http://127.0.0.1:4173/`, tunggu beberapa detik, lalu reload → aplikasi dikendalikan service worker.
2. DevTools → *Application* → *Manifest* tidak boleh menampilkan error; *Service Workers* berstatus `activated`.
3. DevTools → *Network* → centang **Offline**, lalu buka `/tabel-periodik` → halaman tetap tampil dan badge offline muncul.
4. Untuk update: build ulang, muat ulang tab di browser biasa → kartu "Versi baru tersedia" muncul.

## Deployment

- Wajib **HTTPS** (kecuali `localhost`).
- Server harus menyajikan `sw.js` dan `manifest.webmanifest` tanpa cache panjang, dan
  mengarahkan semua rute SPA (`/tabel-periodik`, dll.) ke `index.html`.
