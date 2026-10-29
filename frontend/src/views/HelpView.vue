<script setup>
import { computed, ref } from 'vue'
import AppDocument from '../components/AppDocument.vue'

// Daftar tanya-jawab. Sumber tunggal untuk pencarian & render.
const faq = [
  {
    q: 'Apakah BioChemVerse gratis?',
    a: 'Ya. Membaca materi, membuka tabel periodik, dan menjalankan kuis tidak memungut biaya. Membuat akun hanya diperlukan untuk menyimpan progres dan bookmark.',
  },
  {
    q: 'Kenapa progres saya tidak tersimpan?',
    a: 'Progres hanya tersimpan untuk akun yang sudah login. Pastikan kamu masuk lewat tombol Masuk, lalu cek kembali halaman Modul. Bila token kedaluwarsa, aplikasi akan mengembalikanmu ke tampilan tamu.',
  },
  {
    q: 'Halaman Operasi memuat lama atau model 3D kosong',
    a: 'Model 3D dimuat dari Sketchfab. Periksa koneksi internet, matikan pemblokir konten untuk domain sketchfab.com, atau pilih prosedur lain sementara waktu.',
  },
  {
    q: 'Apakah data anatomi di sini bisa jadi rujukan medis?',
    a: 'Tidak. Semua materi ditujukan untuk pendidikan. Untuk keluhan kesehatan, konsultasikan ke tenaga medis profesional.',
  },
  {
    q: 'Bagaimana cara keluar dari akun?',
    a: 'Tekan Keluar di bagian bawah sidebar atau di top bar. Data sesi di perangkat kamu akan dihapus.',
  },
  {
    q: 'Apakah situs ini memakai cookies pelacak?',
    a: 'Tidak. Kami hanya menyimpan token login di localStorage. Rincian ada di halaman Kebijakan Cookies.',
  },
  {
    q: 'Bolehkah materi digunakan untuk kelas?',
    a: 'Boleh untuk keperluan pembelajaran dengan menyebutkan sumbernya. Bila memakai ulang gambar atau model pihak ketiga, ikuti lisensi aslinya.',
  },
  {
    q: 'Saya menemukan data unsur yang salah atau tautan rusak',
    a: 'Laporkan lewat kanal di bawah dengan menyertakan alamat halaman dan tangkapan layar bila ada. Kami akan memeriksa dan memperbarui.',
  },
]

const query = ref('')
const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return faq
  return faq.filter((item) => `${item.q} ${item.a}`.toLowerCase().includes(q))
})

const openIndex = ref(0)
const toggle = (index) => (openIndex.value = openIndex.value === index ? -1 : index)
</script>

<template>
  <AppDocument title="Bantuan" subtitle="Panduan singkat, jawaban pertanyaan umum, dan kanal pelaporan." updated="29 Oktober 2026">
    <h2 id="mulai">Mulai cepat</h2>
    <ol>
      <li>Buka <RouterLink to="/modules">Modul</RouterLink> untuk melihat materi yang tersedia.</li>
      <li>Daftar akun agar progres, skor kuis, dan bookmark tersimpan.</li>
      <li>Jelajahi <RouterLink to="/tabel-periodik">Tabel Periodik</RouterLink> untuk detail unsur dan kuis.</li>
      <li>Buka <RouterLink to="/operasi">Operasi</RouterLink> untuk katalog prosedur dengan visual 3D.</li>
    </ol>

    <h2 id="faq">Pertanyaan umum</h2>
    <label for="faq-search" class="mb-2 block text-sm text-slate-400">Cari pertanyaan</label>
    <input
      id="faq-search"
      v-model="query"
      type="search"
      placeholder="Cari pertanyaan… misalnya “progres” atau “cookies”"
      class="mb-4 w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-200 placeholder:text-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
    />

    <p v-if="!filtered.length" class="text-sm text-slate-500">
      Tidak ada hasil untuk “{{ query }}”. Coba kata lain atau kirim pertanyaan lewat kanal di bawah.
    </p>

    <div v-else class="space-y-2">
      <div v-for="(item, index) in filtered" :key="item.q" class="overflow-hidden rounded-lg border border-slate-800">
        <button
          type="button"
          class="flex w-full items-center justify-between gap-3 bg-slate-900 px-4 py-3 text-left text-sm font-medium text-slate-200 transition-colors hover:bg-slate-800 focus:ring-2 focus:ring-blue-500/60 focus:outline-none"
          :aria-expanded="openIndex === index"
          @click="toggle(index)"
        >
          <span>{{ item.q }}</span>
          <svg
            viewBox="0 0 24 24"
            class="h-4 w-4 shrink-0 text-slate-500 transition-transform"
            :class="openIndex === index ? 'rotate-180' : ''"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            aria-hidden="true"
          >
            <path d="M6 9l6 6 6-6" />
          </svg>
        </button>
        <p v-show="openIndex === index" class="border-t border-slate-800 px-4 py-3 text-sm leading-relaxed text-slate-400">
          {{ item.a }}
        </p>
      </div>
    </div>

    <h2 id="akun">Mengelola akun</h2>
    <ul>
      <li><strong>Lupa kata sandi:</strong> pemulihan mandiri belum tersedia; ajukan reset lewat kanal pelaporan dengan menyebut username kamu.</li>
      <li><strong>Ganti username atau email:</strong> ajukan lewat kanal pelaporan.</li>
      <li><strong>Hapus akun:</strong> minta penghapusan beserta data progres dan bookmark. Penghapusan bersifat permanen.</li>
    </ul>

    <h2 id="lapor">Melaporkan masalah</h2>
    <p>Supaya cepat ditangani, sertakan:</p>
    <ul>
      <li>Alamat halaman (mis. <code>/tabel-periodik/Fe</code>).</li>
      <li>Langkah sebelum masalah muncul.</li>
      <li>Jenis peramban dan perangkat.</li>
      <li>Tangkapan layar, bila memungkinkan.</li>
    </ul>
    <p>
      Gunakan kanal pelaporan proyek: buka <strong>issue</strong> di repositori GitHub BioChemVerse, atau hubungi
      pengelola platform melalui kontak yang tercantum di repositori tersebut.
    </p>

    <h2 id="lain">Tautan bermanfaat</h2>
    <ul>
      <li><RouterLink to="/tentang">Tentang BioChemVerse</RouterLink></li>
      <li><RouterLink to="/kebijakan-privasi">Kebijakan Privasi</RouterLink></li>
      <li><RouterLink to="/kebijakan-cookies">Kebijakan Cookies</RouterLink></li>
    </ul>
  </AppDocument>
</template>
