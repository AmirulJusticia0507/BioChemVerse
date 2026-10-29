<script setup>
import { useAuth } from './composables/useAuth.js'

const { user, isLoggedIn, logout } = useAuth()
</script>

<template>
  <div class="flex min-h-screen flex-col bg-slate-900 text-white">
    <header class="sticky top-0 z-10 border-b border-slate-800 bg-slate-900/90 backdrop-blur">
      <div class="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
        <RouterLink to="/" class="flex items-center gap-2 text-lg font-bold">
          <span class="rounded-lg bg-blue-500/15 px-2 py-1">🧪</span>
          BioChemVerse
        </RouterLink>

        <nav class="flex items-center gap-1 text-sm">
          <RouterLink to="/" class="nav-link">Beranda</RouterLink>
          <RouterLink to="/modules" class="nav-link">Modul</RouterLink>
          <RouterLink to="/operasi" class="nav-link">Operasi</RouterLink>
          <RouterLink to="/tabel-periodik" class="nav-link">Tabel Periodik</RouterLink>
          <RouterLink to="/bandingkan" class="nav-link">Bandingkan</RouterLink>
          <RouterLink to="/belajar" class="nav-link">Belajar</RouterLink>
          <RouterLink to="/kalkulator" class="nav-link">Kalkulator</RouterLink>
          <RouterLink to="/kuis" class="nav-link">Kuis</RouterLink>

          <template v-if="isLoggedIn">
            <span class="ml-2 hidden text-slate-400 sm:inline">
              Halo, <span class="font-medium text-emerald-400">{{ user.username }}</span>
            </span>
            <button
              type="button"
              class="ml-1 rounded-lg border border-slate-600 px-3 py-2 text-slate-200 transition-colors hover:border-slate-500 hover:bg-slate-800"
              @click="logout"
            >
              Keluar
            </button>
          </template>

          <template v-else>
            <RouterLink
              to="/login"
              class="ml-2 rounded-lg bg-blue-500 px-3 py-2 font-medium text-white transition-colors hover:bg-blue-600"
            >
              Masuk
            </RouterLink>
            <RouterLink
              to="/register"
              class="rounded-lg border border-slate-600 px-3 py-2 text-slate-200 transition-colors hover:border-slate-500 hover:bg-slate-800"
            >
              Daftar
            </RouterLink>
          </template>
        </nav>
      </div>
    </header>

    <main class="flex-1">
      <RouterView />
    </main>

    <footer class="border-t border-slate-800 px-4 py-6 text-center text-xs text-slate-500">
      BioChemVerse · ChemSphere · ForensiLab · AnatomiMed — MIT License
    </footer>
  </div>
</template>
