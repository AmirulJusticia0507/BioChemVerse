<script setup>
</script>

<template>
  <section class="mx-auto flex max-w-2xl flex-col items-center px-4 py-24 text-center">
    <p class="text-6xl font-bold text-blue-500">404</p>
    <h1 class="mt-4 text-2xl font-semibold">Halaman tidak ditemukan</h1>
    <p class="mt-2 text-slate-400">
      Halaman yang kamu tuju tidak ada atau sudah dipindahkan.
    </p>
    <RouterLink
      to="/"
      class="mt-8 rounded-lg bg-blue-500 px-5 py-2.5 font-medium text-white transition-colors hover:bg-blue-600"
    >
      Kembali ke Beranda
    </RouterLink>
  </section>
</template>
