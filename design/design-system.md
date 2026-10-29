# 🎨 Design System — BioChemVerse

Satu sumber kebenaran untuk warna, tipografi, komponen, dan gaya visual.
Dijaga oleh **design-agent** (lihat [AGENTS.md](../AGENTS.md)).

---

## 1. Warna

| Token | Hex | Tailwind | Penggunaan |
| --- | --- | --- | --- |
| Primary | `#3B82F6` | `blue-500` | tombol utama, link, fokus, aksen terpilih |
| Secondary | `#10B981` | `emerald-500` | status sukses, hasil uji benar |
| Accent | `#F59E0B` | `amber-500` | sorotan, badge peringatan, highlight data |
| Danger | `#EF4444` | `red-500` | error, reaksi gagal, status bahaya |
| Background | `#0F172A` | `slate-900` | latar utama (tema gelap) |
| Surface | `#1E293B` | `slate-800` | kartu, panel, modal |
| Text | `#FFFFFF` | `white` | teks utama |
| Text muted | `#CBD5E1` | `slate-300` | teks sekunder, deskripsi |

**Aturan:**

- Maksimal **3 warna** dalam satu layar (selain netral).
- `Danger` hanya untuk kegagalan/error — jangan untuk dekorasi.
- Warna status selalu **ditemani ikon/teks**, jangan warna saja (aksesibilitas).

## 2. Tipografi

- **Font:** `Inter, system-ui, sans-serif`
- **Base size:** `16px`, line-height default Tailwind (`1.5`)

| Skala | Kelas Tailwind | Penggunaan |
| --- | --- | --- |
| 36px | `text-4xl font-bold` | judul halaman (hero) |
| 24px | `text-2xl font-semibold` | judul bagian |
| 18px | `text-lg` | judul kartu |
| 16px | `text-base` | isi/paragraf |
| 14px | `text-sm` | label, metadata, caption |

## 3. Tema

- Proyek memakai **tema gelap** (`bg-slate-900`), teks terang.
- Tailwind CSS v4: token didefinisikan lewat `@theme` di `frontend/src/style.css`, kelas dipakai langsung di template.
- Mode terang (nanti) harus memakai palet yang sama — cukup ganti token `--color-*`.

## 4. Komponen Inti

Semua komponen dibuat sekali lalu dipakai ulang (`frontend/src/components/`):

| Komponen | Varian wajib | Catatan |
| --- | --- | --- |
| **Button** | `primary`, `secondary`, `danger`, `ghost` | tinggi 40px, radius `rounded-lg`, fokus `ring-2 ring-blue-500` |
| **Card** | default, `interactive` | `bg-slate-800 rounded-xl p-6`, hover: `ring-1 ring-slate-600` |
| **Modal** | small, large | backdrop `bg-black/60`, tutup dengan ESC & klik luar |
| **Input** | default, `error` | label wajib di atas input; error tampilkan teks merah + ikon |
| **Badge** | `success`, `warning`, `danger`, `info` | pill `rounded-full px-2 py-0.5 text-xs` |

### Contoh: Button (Tailwind)

```html
<!-- primary -->
<button class="rounded-lg bg-blue-500 px-4 py-2 font-medium text-white hover:bg-blue-600 focus:ring-2 focus:ring-blue-500/50">
  Mulai
</button>

<!-- danger -->
<button class="rounded-lg bg-red-500 px-4 py-2 font-medium text-white hover:bg-red-600">
  Hapus
</button>
```

## 5. Ikon & Aset

- Berkas ikon: `frontend/public/icons.svg` (sprite SVG), favicon: `frontend/public/favicon.svg`.
- Ilustrasi/aset: `frontend/src/assets/`.
- Ikon selalu **dua ukuran**: 16px (inline teks) dan 20px (toolbar/tombol).

## 6. Ilustrasi Anatomi & Sains

- Anatomi: siluet tubuh proporsi ±7,5 kepala (`fill` gradien `slate-900`→`slate-700`) dengan organ dalam berwarna lembut (paru `sky-500`, jantung `red-600`, hati `orange-600`, lambung `rose-500`, usus `amber-500`, ginjal `violet-500`, panggul `teal-400`) — lihat `AnatomyBody.vue`.
- Bedah 3D (`/operasi`): skematik-realistis, bukan fotorealistik — kulit `#C0856A` (MeshPhysical), organ: hati `#7F2D24`, empedu `#1D6B3F`, apendiks `#A8453A`, usus `#B0614F`, lambung `#C26F6A`, ginjal `#8F4747`. Instrumen `#CBD5E1` (metalness 0.9), keran gas `sky-400`, lensa `amber-200` ber-emissive.
- Tersedia dua tampilan lewat toggle segmented (`Pria` default, `Wanita`). Tampilan wanita memakai siluet bahu sempit/pinggang/panggul lebar dan menambah organ khusus: payudara `pink-500` dan reproduksi wanita `fuchsia-500`. Organ khusus wanita tidak dirender pada tampilan pria, dan panel keterangannya memakai `itemsWanita` bila ada.
- Saat dipilih, satu bagian memakai isian aksen `fill-blue-500/60` dengan garis `blue-100`; organ dalam digambar di atas bagian luar agar klik tidak tertutup.
- Setiap bagian interaktif SVG wajib `role="button"` + `tabindex="0"` + `aria-label` + `aria-pressed`.
- Molekul: ikatan `stroke-slate-400`, atom mengikuti warna CPK (O = merah, N = biru, C = abu gelap).
- Lab/forensik: gunakan `Accent` untuk area yang sedang aktif bereaksi.

## 7. Aksesibilitas

- Kontras teks minimum **4.5:1** (WCAG AA).
- Semua tombol ikon butuh `aria-label`.
- Elemen interaktif SVG (mis. bagian tubuh) harus bisa diakses keyboard (`tabindex` + handler `Enter/Space`).
- Animasi menghormati `prefers-reduced-motion`.

## 8. Checklist Review (design-agent)

- [ ] Warna memakai token di atas, bukan warna hardcoded baru.
- [ ] Tipografi memakai skala yang terdaftar.
- [ ] Komponen memakai varian yang sudah ada (tidak duplikat).
- [ ] Status selalu punya label/ikon, bukan warna saja.
- [ ] Kondisi loading, empty, dan error ada.
