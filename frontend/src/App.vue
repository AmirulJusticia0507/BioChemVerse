<script setup>
import { computed, onBeforeUnmount, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from './composables/useAuth.js'
import { sidebarDesktopHidden, sidebarWidth, toggleDesktopSidebar } from './composables/useSidebar.js'
import { applyUpdate, bindOnlineStatus, updateReady } from './composables/usePwaState.js'
import AppSidebar from './components/AppSidebar.vue'

const { user, isLoggedIn, logout } = useAuth()
const route = useRoute()

// Status jaringan (online/offline) untuk banner mode offline di sidebar.
let unbindOnline = null
onMounted(() => {
  unbindOnline = bindOnlineStatus()

  // Service worker hanya ada di hasil build; di `npm run dev` import ini kosong.
  if ('serviceWorker' in navigator) {
    import('virtual:pwa-register')
      .then((mod) => {
        const registerSW = mod?.registerSW ?? mod?.default
        if (typeof registerSW !== 'function') return
        applyUpdate.value = registerSW({
          immediate: true,
          onNeedRefresh: () => (updateReady.value = true),
          onOfflineReady: () => {},
        })
      })
      .catch(() => {
        /* build tanpa PWA (mis. dev) — abaikan */
      })
  }
})
onBeforeUnmount(() => unbindOnline?.())

// Top bar menampilkan brand + judul halaman aktif (breadcrumb), supaya tidak
// menduplikasi label menu yang sudah terlihat di sidebar.
const titles = {
  home: 'Beranda',
  modules: 'Modul Pembelajaran',
  surgery: 'Menu Operasi',
  'periodic-table': 'Tabel Periodik',
  'element-detail': 'Detail Unsur',
  login: 'Masuk',
  register: 'Daftar',
  'forgot-password': 'Lupa Kata Sandi',
  'reset-password': 'Atur Ulang Kata Sandi',
  about: 'Tentang',
  help: 'Bantuan',
  privacy: 'Kebijakan Privasi',
  cookies: 'Kebijakan Cookies',
  'not-found': 'Halaman tidak ditemukan',
}
const pageTitle = computed(() => titles[route.name] ?? 'BioChemVerse')

// Konten digeser selebar sidebar saat ini (72px rail atau 240px penuh).
const contentStyle = computed(() => ({ '--sidebar-w': `${sidebarWidth.value}px` }))

const footerLinks = [
  { to: '/tentang', label: 'Tentang' },
  { to: '/bantuan', label: 'Bantuan' },
  { to: '/kebijakan-privasi', label: 'Kebijakan Privasi' },
  { to: '/kebijakan-cookies', label: 'Kebijakan Cookies' },
]
</script>

<template>
  <div class="min-h-screen bg-slate-900 text-white">
    <AppSidebar />

    <!-- Konten: digeser selebar sidebar pada layar besar -->
    <div class="flex min-h-screen flex-col lg:pl-[var(--sidebar-w)] transition-[padding] duration-200 ease-out" :style="contentStyle">
      <header class="sticky top-0 z-30 border-b border-slate-800 bg-slate-900/85 backdrop-blur">
        <div class="flex h-14 items-center gap-3 pl-16 pr-4 sm:pl-4 lg:px-6">
          <button
            type="button"
            class="hidden h-9 shrink-0 items-center gap-2 rounded-lg px-2 text-sm text-slate-300 transition-colors hover:bg-slate-800 hover:text-white focus:ring-2 focus:ring-blue-500/60 focus:outline-none lg:flex"
            :aria-label="sidebarDesktopHidden ? 'Tampilkan sidebar' : 'Sembunyikan sidebar'"
            aria-controls="app-sidebar"
            :aria-expanded="!sidebarDesktopHidden"
            @click="toggleDesktopSidebar"
          >
            <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true">
              <path v-if="sidebarDesktopHidden" d="M4 5h16M4 12h16M4 19h16" />
              <path v-else d="M4 5h16M4 12h10M4 19h16M16 9l3 3-3 3" />
            </svg>
            <span>{{ sidebarDesktopHidden ? 'Tampilkan sidebar' : 'Sembunyikan sidebar' }}</span>
          </button>
          <div class="flex min-w-0 flex-1 items-center gap-2 text-sm">
            <span class="shrink-0 font-bold text-white lg:hidden">BioChemVerse</span>
            <template v-if="pageTitle !== 'Beranda'">
              <span class="shrink-0 text-slate-600 lg:hidden" aria-hidden="true">/</span>
              <span class="truncate text-slate-300" aria-current="page">{{ pageTitle }}</span>
            </template>
          </div>

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

      <footer class="border-t border-slate-800 px-4 py-8 text-center text-xs text-slate-500">
        <nav class="mb-4 flex flex-wrap items-center justify-center gap-x-5 gap-y-2" aria-label="Tautan informasi">
          <RouterLink
            v-for="link in footerLinks"
            :key="link.to"
            :to="link.to"
            class="rounded text-slate-400 transition-colors hover:text-white focus:ring-2 focus:ring-blue-500/60 focus:outline-none"
          >
            {{ link.label }}
          </RouterLink>
        </nav>
        <p>BioChemVerse · ChemSphere · ForensiLab · AnatomiMed — MIT License</p>
      </footer>
    </div>
  </div>
</template>
