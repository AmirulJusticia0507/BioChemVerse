<script setup>
import AppDocument from '../components/AppDocument.vue'
</script>

<template>
  <AppDocument
    title="Kebijakan Cookies"
    subtitle="Situs ini tidak memakai cookies pelacakan. Berikut penjelasan lengkapnya."
    updated="29 Oktober 2026"
  >
    <p>
      Cookies adalah berkas kecil yang disimpan peramban. Kebijakan ini menjelaskan penggunaan cookies dan
      teknologi penyimpanan serupa di BioChemVerse.
    </p>

    <h2>1. Ringkasan</h2>
    <p>
      <strong>Kami tidak memasang cookies iklan atau cookies pelacakan pihak ketiga.</strong> Satu-satunya data
      yang disimpan di perangkat kamu adalah penyimpanan lokal yang wajib agar kamu tetap login.
    </p>

    <h2>2. Penyimpanan lokal yang kami pakai</h2>
    <div class="table-scroll">
    <table>
      <thead>
        <tr>
          <th>Kunci</th>
          <th>Jenis</th>
          <th>Isi</th>
          <th>Masa berlaku</th>
          <th>Sifat</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>bcv_token</code></td>
          <td>localStorage</td>
          <td>Token akses JWT untuk permintaan API</td>
          <td>Sampai logout atau token kedaluwarsa</td>
          <td>Wajib</td>
        </tr>
        <tr>
          <td><code>bcv_user</code></td>
          <td>localStorage</td>
          <td>Profil ringkas (username) untuk tampilan header</td>
          <td>Sampai logout</td>
          <td>Wajib</td>
        </tr>
      </tbody>
    </table>
    </div>
    <p>
      Keduanya <strong>bukan cookies</strong> dan tidak dikirim otomatis pada setiap permintaan; aplikasi
      membacanya lewat JavaScript untuk melampirkan header <code>Authorization</code> ke API.
    </p>

    <h2>3. Cookies dari pihak ketiga</h2>
    <p>
      Halaman yang menyematkan konten Sketchfab (model 3D di menu Operasi) dapat memuat sumber dari domain
      <code>sketchfab.com</code>. Domain tersebut dapat memasang cookies sesuai kebijakan privasinya sendiri,
      terutama bila kamu login ke Sketchfab. Kami tidak mengendalikan cookies tersebut.
    </p>

    <h2>4. Apa yang tidak kami gunakan</h2>
    <ul>
      <li>Cookies iklan atau retargeting.</li>
      <li>Piksel pelacak media sosial.</li>
      <li>Alat analitik pihak ketiga (Google Analytics, Hotjar, dan sejenisnya).</li>
    </ul>

    <h2>5. Mengelola data di perangkat kamu</h2>
    <ul>
      <li><strong>Cara termudah:</strong> tekan <strong>Keluar</strong> di sidebar atau top bar.</li>
      <li>
        <strong>Lewat peramban:</strong> buka pengaturan situs → hapus data untuk domain BioChemVerse. Kamu akan
        keluar dari sesi saat ini.
      </li>
      <li>Menghapus data tidak menghapus akun; progres dan bookmark tetap tersimpan di server.</li>
    </ul>

    <h2>6. Perubahan kebijakan</h2>
    <p>
      Bila kelak kami menambahkan cookies lainnya, halaman ini akan diperbarui dan kamu akan diminta
      persetujuannya terlebih dahulu untuk cookies non-wajib.
    </p>

    <h2>7. Tautan terkait</h2>
    <p>
      Baca juga <RouterLink to="/kebijakan-privasi">Kebijakan Privasi</RouterLink> atau ajukan pertanyaan melalui
      <RouterLink to="/bantuan">Bantuan</RouterLink>.
    </p>
  </AppDocument>
</template>
