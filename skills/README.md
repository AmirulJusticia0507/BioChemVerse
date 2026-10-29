# 🤖 Skills untuk Agent

Skills adalah instruksi singkat dan terfokus yang bisa dimuat agent saat tugasnya
cocok dengan deskripsi skill. Skill melengkapi peran yang sudah didefinisikan di
[AGENTS.md](../AGENTS.md) (`docs-agent`, `arch-agent`, `design-agent`).

---

## Daftar Skill Proyek

| Skill | File | Muat saat | Isi instruksi |
| --- | --- | --- | --- |
| **docs** | `skills/docs.md` | merapikan/menulis README, `docs/`, komentar API | struktur dokumen, gaya bahasa Indonesia + istilah teknis, wajib sinkron dengan kode |
| **arch** | `skills/arch.md` | menambah endpoint, tabel, modul, atau dependensi baru | aturan layering (`main.py` → `db.py`/`cache.py`), prefix `/api/v1/`, skema idempoten, update `architecture/overview.md` + `docs/openapi.json` |
| **design** | `skills/design.md` | membuat/mengubah komponen UI | gunakan token di `design/design-system.md`, tema gelap, varian komponen yang ada, checklist aksesibilitas |
| **anatomy** | `skills/anatomy.md` | menambah konten anatomi/patofisiologi | rujukan 12 sistem di `docs/anatomy.md`, istilah Latin benar, format heading & bullet |

> File skill dibuat bertahap — bila belum ada, ikuti pola template di bawah.

## Cara Agent Memakai Skill

1. Baca `AGENTS.md` (aturan wajib: task → commit → push).
2. Baca `TODO.md`, pilih task pending prioritas tertinggi.
3. **Muat skill** yang relevan dengan tugas (file `skills/<nama>.md`).
4. Kerjakan task sesuai instruksi skill + `design/design-system.md` + `architecture/overview.md`.
5. Update status di `TODO.md`, commit, push.

## Template Skill

```markdown
# Skill: <nama>

## Kapan dipakai
<Satu-dua kalimat pemicu>

## Aturan wajib
- <aturan 1>
- <aturkan 2>

## Checklist selesai
- [ ] <verifikasi 1>
- [ ] <verifikasi 2>
```

## Konvensi

- Satu file = satu skill, maksimal ~50 baris agar cepat dibaca.
- Gunakan bahasa Indonesia untuk penjelasan, istilah teknis tetap dalam bahasa Inggris.
- Setiap perubahan perilaku wajib disertai **checklist verifikasi** yang bisa dijalankan.
- Skill yang tidak terpakai 2× dalam 30 hari dihapus (hindari akumulasi).
