<script setup>
import AppDocument from '../components/AppDocument.vue'
</script>

<template>
  <AppDocument title="Kebijakan Privasi" subtitle="Bagaimana BioChemVerse mengumpulkan, memakai, dan menyimpan data kamu." updated="29 Oktober 2026">
    <p>
      BioChemVerse adalah platform edukasi kimia, forensik, dan anatomi. Kebijakan ini menjelaskan data apa
      yang kami proses saat kamu memakai situs ini, untuk apa data tersebut dipakai, dan pilihan yang kamu miliki.
    </p>

    <h2>1. Data yang kami kumpulkan</h2>
    <h3>a. Data akun</h3>
    <p>Saat mendaftar kamu memberikan data berikut, yang disimpan di server kami:</p>
    <ul>
      <li><strong>Username</strong> — ditampilkan di antarmuka.</li>
      <li><strong>Alamat email</strong> — untuk identifikasi akun.</li>
      <li>
        <strong>Kata sandi</strong> — disimpan sebagai hash, tidak pernah sebagai teks biasa. Kami tidak dapat
        membaca kata sandi kamu.
      </li>
    </ul>
    <h3>b. Data penggunaan</h3>
    <ul>
      <li><strong>Progres modul</strong> (skor dan status selesai) untuk akun yang login.</li>
      <li><strong>Jawaban kuis</strong> dan percobaan yang kamu kirim.</li>
      <li><strong>Bookmark unsur</strong> pada Tabel Periodik.</li>
    </ul>
    <h3>c. Data yang disimpan di perangkat kamu</h3>
    <p>
      Token login dan profil ringkas disimpan di <code>localStorage</code> peramban dengan kunci
      <code>bcv_token</code> dan <code>bcv_user</code>. Data ini tidak dikirim ke pihak ketiga dan hilang saat
      kamu menekan <strong>Keluar</strong>. Rincian selengkapnya ada di halaman
      <RouterLink to="/kebijakan-cookies">Kebijakan Cookies</RouterLink>.
    </p>
    <h3>d. Yang tidak kami kumpulkan</h3>
    <p>Kami tidak memakai alat analitik pihak ketiga, tidak menampilkan iklan, dan tidak menjual data ke siapa pun.</p>

    <h2>2. Tujuan pemrosesan</h2>
    <ul>
      <li>Menjalankan autentikasi dan menjaga sesi login.</li>
      <li>Menyimpan progres belajar agar bisa dilanjutkan lain waktu.</li>
      <li>Menampilkan hasil kuis dan daftar bookmark milikmu.</li>
      <li>Menjaga keamanan layanan dan menelusuri gangguan teknis.</li>
    </ul>

    <h2>3. Dasar pemrosesan</h2>
    <p>
      Data akun dan progres diproses atas dasar <strong>persetujuan</strong> dan <strong>pelaksanaan layanan</strong>
      yang kamu minta saat mendaftar. Kamu dapat menarik persetujuan kapan saja dengan menghapus akun.
    </p>

    <h2>4. Penyimpanan dan keamanan</h2>
    <ul>
      <li>Data disimpan di basis data milik proyek; akses dibatasi untuk keperluan operasional.</li>
      <li>Kata sandi di-hash sebelum disimpan ke basis data.</li>
      <li>Komunikasi dengan API memakai token Bearer berumur terbatas.</li>
      <li>
        Tidak ada sistem yang sepenuhnya bebas risiko. Bila terjadi insiden yang berdampak pada data kamu,
        kami akan mengumumkannya di situs ini.
      </li>
    </ul>

    <h2>5. Pihak ketiga</h2>
    <p>
      Beberapa halaman (misalnya menu Operasi) menyematkan model 3D dari <strong>Sketchfab</strong>. Saat konten
      tersebut dimuat, peramban kamu terhubung langsung ke server Sketchfab sehingga mereka dapat melihat alamat
      IP dan informasi perangkat sesuai kebijakan privasi mereka sendiri.
    </p>

    <h2>6. Hak kamu</h2>
    <ul>
      <li><strong>Akses</strong> — melihat data profil dan progres yang tersimpan.</li>
      <li><strong>Perbaikan</strong> — memperbarui username atau email.</li>
      <li><strong>Penghapusan</strong> — meminta penghapusan akun beserta data terkait.</li>
    </ul>
    <p>
      Ajukan permintaan melalui halaman <RouterLink to="/bantuan">Bantuan</RouterLink>. Kami akan menindaklanjuti
      dalam waktu yang wajar.
    </p>

    <h2>7. Anak di bawah umur</h2>
    <p>
      Platform ini ditujukan untuk pelajar dan pendidik. Bila kamu berusia di bawah 13 tahun, gunakan dengan
      pendampingan orang tua atau guru.
    </p>

    <h2>8. Perubahan kebijakan</h2>
    <p>
      Kebijakan ini dapat diperbarui sewaktu-waktu. Tanggal pembaruan terbaru selalu dicantumkan di bagian atas
      halaman.
    </p>

    <h2>9. Kontak</h2>
    <p>
      Pertanyaan seputar privasi dapat disampaikan melalui halaman <RouterLink to="/bantuan">Bantuan</RouterLink>.
    </p>
  </AppDocument>
</template>
