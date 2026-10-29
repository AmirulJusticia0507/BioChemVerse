<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from './composables/useAuth.js'
import { sidebarWidth } from './composables/useSidebar.js'
import AppSidebar from './components/AppSidebar.vue'

const { user, isLoggedIn, logout } = useAuth()
const route = useRoute()

// Judul top bar mengikuti halaman aktif.
const titles = {
  home: 'Beranda',
  modules: 'Modul Pembelajaran',
  surgery: 'Menu Operasi',
  'periodic-table': 'Tabel Periodik',
  'element-detail': 'Detail Unsur',
  login: 'Masuk',
  register: 'Daftar',
  'not-found': 'Halaman tidak ditemukan',
}
const pageTitle = computed(() => titles[route.name] ?? 'BioChemVerse')

// Konten digeser selebar sidebar saat ini (72px rail atau 240px penuh).
const contentStyle = computed(() => ({ '--sidebar-w': `${sidebarWidth.value}px` }))
</script>

<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <AppSidebar />

    <!-- Konten: digeser selebar sidebar pada layar besar -->
    <div class="flex min-h-screen flex-col lg:pl-[var(--sidebar-w)] transition-[padding] duration-200 ease-out" :style="contentStyle">
      <header class="sticky top-0 z-30 border-b border-slate-800 bg-slate-900/85 backdrop-blur">
        <div class="flex h-14 items-center gap-3 pl-16 pr-4 sm:pl-4 lg:px-6">
          <h1 class="min-w-0 flex-1 truncate text-sm font-semibold text-slate-200 sm:text-base">
            {{ pageTitle }}
          </h1>

          <template v-if="isLoggedIn">
            <span class="hidden items-center gap-2 text-sm text-slate-400 sm:flex">
              <span class="grid h-7 w-7 place-items-center rounded-full bg-emerald-500/15 text-xs font-semibold text-emerald-300" aria-hidden="true">
                {{ user.username.slice(0, 1).toUpperCase() }}
              </span>
              {{ user.username }}
            </span>
            <button
              type="button"
              class="rounded-lg border border-slate-700 px-3 py-1.5 text-sm text-slate-200 transition-colors hover:border-slate-500 hover:bg-slate-800 focus:ring-2 focus:ring-blue-500/60 focus:outline-none"
              @click="logout"
            >
              Keluar
            </button>
          </template>

          <template v-else>
            <RouterLink
              to="/login"
              class="rounded-lg border border-slate-700 px-3 py-1.5 text-sm text-slate-200 transition-colors hover:border-slate-500 hover:bg-slate-800 focus:ring-2 focus:ring-blue-500/60 focus:outline-none"
            >
              Masuk
            </RouterLink>
            <RouterLink
              to="/register"
              class="rounded-lg bg-blue-500 px-3 py-1.5 text-sm font-medium text-white transition-colors hover:bg-blue-600 focus:ring-2 focus:ring-blue-500/60 focus:outline-none"
            >
              Daftar
            </RouterLink>
          </template>
        </div>
      </header>

      <main class="flex-1">
        <RouterView />
      </main>

      <footer class="border-t border-slate-800 px-4 py-6 text-center text-xs text-slate-500">
        BioChemVerse · ChemSphere · ForensiLab · AnatomiMed — MIT License
      </footer>
    </div>
  </div>
</template>
