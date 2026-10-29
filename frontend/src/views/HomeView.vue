<script setup>
import AnatomyBody from '../components/AnatomyBody.vue'
</script>

<template>
  <div>
    <!-- Hero -->
    <section class="mx-auto max-w-4xl px-4 py-16 text-center">
      <p
        class="mb-4 inline-flex items-center gap-2 rounded-full border border-slate-700 bg-slate-800/60 px-3 py-1 text-xs text-slate-300"
      >
        <span class="h-2 w-2 rounded-full bg-emerald-500"></span>
        Platform edukasi kimia, forensik & anatomi
      </p>
      <h1 class="text-4xl font-bold tracking-tight sm:text-5xl">BioChemVerse</h1>
      <p class="mx-auto mt-4 max-w-2xl text-slate-300">
        Simulasi reaksi kimia, gim investigasi forensik, dan anatomi 3D dalam satu ekosistem
        pembelajaran interaktif berbasis studi kasus nyata.
      </p>
      <div class="mt-8 flex flex-wrap justify-center gap-3">
        <RouterLink
          to="/modules"
          class="rounded-lg bg-blue-500 px-5 py-2.5 font-medium text-white transition-colors hover:bg-blue-600 focus:ring-2 focus:ring-blue-500/50 focus:outline-none"
        >
          Jelajahi Modul
        </RouterLink>
        <a
          href="http://localhost:8000/docs"
          target="_blank"
          rel="noopener"
          class="rounded-lg border border-slate-600 px-5 py-2.5 font-medium text-slate-200 transition-colors hover:border-slate-500 hover:bg-slate-800"
        >
          Dokumentasi API
        </a>
      </div>
    </section>

    <!-- Kerangka anatomi interaktif -->
    <section class="mx-auto max-w-5xl px-4 pb-16">
      <div class="rounded-xl border border-slate-800 bg-slate-800/40 p-6">
        <h2 class="mb-1 text-2xl font-semibold">Kerangka Anatomi Tubuh Manusia</h2>
        <p class="mb-6 text-sm text-slate-400">
          Klik bagian tubuh untuk menyorotnya — pratinjau modul AnatomiMed.
        </p>
        <AnatomyBody />
      </div>
    </section>
  </div>
</template>
