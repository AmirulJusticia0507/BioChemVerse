<script setup>
import AppDocument from '../components/AppDocument.vue'

// Empat pilar platform — sumbernya sama dengan nama modul di backend.
const pillars = [
  {
    icon: '⚗️',
    name: 'ChemSphere',
    text: 'Tabel periodik 118 unsur, detail sifat & ion, halaman Bandingkan unsur, serta kuis unsur.',
  },
  {
    icon: '🔍',
    name: 'ForensiLab',
    text: 'Gim investigasi forensik: membaca jejak, mengumpulkan bukti, dan menyusun kesimpulan.',
  },
  {
    icon: '🩺',
    name: 'AnatomiMed',
    text: 'Kerangka anatomi interaktif, model 3D pria dan wanita, serta katalog prosedur bedah.',
  },
]

const stack = [
  { label: 'Frontend', value: 'Vue 3, Vue Router, TailwindCSS, Three.js' },
  { label: 'Backend', value: 'Python FastAPI + layanan Golang' },
  { label: 'Data', value: 'PostgreSQL, Redis' },
  { label: 'Dokumentasi API', value: 'OpenAPI / Swagger' },
]
</script>

<template>
  <AppDocument title="Tentang BioChemVerse" subtitle="Platform edukasi kimia, forensik, dan anatomi dalam satu tempat." updated="29 Oktober 2026">
    <h2>Misi</h2>
    <p>
      Belajar sains sering terasa terpecah: rumus di satu buku, anatomi di atlas, investigasi forensik di tayangan
      televisi. BioChemVerse menyatukannya dalam satu antarmuka interaktif supaya pelajar bisa melihat hubungan
      antara reaksi kimia, bukti forensik, dan tubuh manusia.
    </p>

    <h2>Empat pilar</h2>
    <ul>
      <li v-for="pillar in pillars" :key="pillar.name">
        <strong>{{ pillar.icon }} {{ pillar.name }}</strong> — {{ pillar.text }}
      </li>
    </ul>

    <h2>Apa yang bisa dilakukan di sini</h2>
    <ul>
      <li><strong>Modul</strong> — materi, skor, dan progres yang tersimpan pada akunmu.</li>
      <li><strong>Operasi</strong> — katalog prosedur bedah beserta visual tata letak 3D.</li>
      <li><strong>Tabel Periodik</strong> — jelajahi unsur, simpan favorit, dan uji pemahaman lewat kuis.</li>
    </ul>

    <h2>Teknologi</h2>
    <table>
      <tbody>
        <tr v-for="row in stack" :key="row.label">
          <th scope="row">{{ row.label }}</th>
          <td>{{ row.value }}</td>
        </tr>
      </tbody>
    </table>

    <h2>Keterbukaan</h2>
    <p>
      Situs ini bersifat edukatif dan <strong>bukan pengganti diagnosis tenaga medis</strong>. Materi anatomi dan
      prosedur bedah disajikan untuk pemahaman konsep, bukan panduan tindakan klinis. Untuk keluhan kesehatan,
      selalu konsultasikan ke profesional.
    </p>

    <h2>Lisensi</h2>
    <p>
      Kode proyek dirilis dengan lisensi MIT. Model 3D pihak ketiga tunduk pada lisensinya masing-masing (misalnya
      CC BY di Sketchfab) dan dihormati sesuai ketentuan atribusinya.
    </p>

    <h2>Butuh bantuan?</h2>
    <p>
      Lihat halaman <RouterLink to="/bantuan">Bantuan</RouterLink>, atau baca
      <RouterLink to="/kebijakan-privasi">Kebijakan Privasi</RouterLink> dan
      <RouterLink to="/kebijakan-cookies">Kebijakan Cookies</RouterLink>.
    </p>
  </AppDocument>
</template>
