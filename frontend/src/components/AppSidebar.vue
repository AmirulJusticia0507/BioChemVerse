<script setup>
import { onBeforeUnmount, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '../composables/useAuth.js'
import { sidebarCollapsed, sidebarMobileOpen } from '../composables/useSidebar.js'

const { user, isLoggedIn, logout } = useAuth()
const route = useRoute()

const collapsed = sidebarCollapsed
const mobileOpen = sidebarMobileOpen

const groups = [
  {
    title: 'Jelajahi',
    items: [
      { to: '/', label: 'Beranda', icon: 'M3 11.5 12 4l9 7.5M5.5 10v9h13v-9', exact: true },
      { to: '/modules', label: 'Modul', icon: 'M4 5h7v14H4zM13 5h7v14h-7z' },
      { to: '/operasi', label: 'Operasi', icon: 'M12 4v16M4 12h16' },
      { to: '/tabel-periodik', label: 'Tabel Periodik', icon: 'M4 4h4v4H4zM10 4h4v4h-4zM16 4h4v4h-4zM4 10h4v4H4zM10 10h4v4h-4zM16 10h4v4h-4zM4 16h4v4H4zM10 16h4v4h-4z' },
    ],
  },
]

const closeMobile = () => (mobileOpen.value = false)
const toggleCollapsed = () => (collapsed.value = !collapsed.value)

// Tutup drawer setiap kali pindah halaman.
watch(() => route.fullPath, closeMobile)

// Scroll halaman dikunci selama drawer mobile terbuka.
watch(mobileOpen, (open) => {
  document.body.style.overflow = open ? 'hidden' : ''
})

const onKeydown = (event) => {
  if (event.key === 'Escape') closeMobile()
}
window.addEventListener('keydown', onKeydown)

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = ''
})
</script>

<template>
  <!-- Tombol buka sidebar (mobile) -->
  <button
    type="button"
    class="fixed left-4 top-3 z-40 inline-flex h-10 w-10 items-center justify-center rounded-lg border border-slate-700 bg-slate-900/90 text-slate-200 backdrop-blur transition-colors hover:bg-slate-800 focus:ring-2 focus:ring-blue-500/60 focus:outline-none lg:hidden"
    aria-label="Buka menu navigasi"
    :aria-expanded="mobileOpen"
    aria-controls="app-sidebar"
    @click="mobileOpen = true"
  >
    <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
      <path d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  </button>

  <!-- Latar gelap di belakang drawer (mobile) -->
  <div
    v-if="mobileOpen"
    class="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden"
    aria-hidden="true"
    @click="closeMobile"
  />

  <!-- Sidebar -->
  <aside
    id="app-sidebar"
    class="fixed inset-y-0 left-0 z-50 flex flex-col border-r border-slate-800 bg-slate-900 transition-[width,transform] duration-200 ease-out"
    :class="[
      collapsed ? 'lg:w-[72px]' : 'lg:w-60',
      mobileOpen ? 'w-64 translate-x-0' : 'w-64 -translate-x-full lg:translate-x-0',
    ]"
    :aria-label="'Navigasi utama'"
  >
    <!-- Logo + tombol tutup (mobile) -->
    <div class="flex h-16 shrink-0 items-center gap-2 border-b border-slate-800 px-3">
      <RouterLink
        to="/"
        class="flex min-w-0 flex-1 items-center gap-2 text-base font-bold"
        :class="collapsed ? 'lg:justify-center' : ''"
        :title="collapsed ? 'BioChemVerse' : undefined"
      >
        <span class="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-blue-500/15 text-lg" aria-hidden="true">🧪</span>
        <span class="truncate" :class="collapsed ? 'lg:hidden' : ''">BioChemVerse</span>
      </RouterLink>
      <button
        type="button"
        class="grid h-9 w-9 place-items-center rounded-lg text-slate-400 hover:bg-slate-800 hover:text-white focus:ring-2 focus:ring-blue-500/60 focus:outline-none lg:hidden"
        aria-label="Tutup menu"
        @click="closeMobile"
      >
        <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
          <path d="M6 6l12 12M18 6L6 18" />
        </svg>
      </button>
    </div>

    <!-- Daftar menu -->
    <nav class="flex-1 overflow-y-auto px-2 py-4" aria-label="Daftar menu">
      <template v-for="group in groups" :key="group.title">
        <p
          class="px-3 pb-2 text-[11px] font-semibold uppercase tracking-wider text-slate-500"
          :class="collapsed ? 'lg:text-center lg:text-[10px]' : ''"
        >
          {{ collapsed ? '···' : group.title }}
        </p>
        <ul class="space-y-1">
          <li v-for="item in group.items" :key="item.to">
            <RouterLink
              :to="item.to"
              class="group flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-slate-300 transition-colors hover:bg-slate-800 hover:text-white focus:ring-2 focus:ring-blue-500/60 focus:outline-none"
              :class="collapsed ? 'lg:justify-center lg:px-0' : ''"
              :active-class="item.exact ? '' : 'bg-blue-500/15 font-medium text-blue-300'"
              :exact-active-class="item.exact ? 'bg-blue-500/15 font-medium text-blue-300' : ''"
              :title="collapsed ? item.label : undefined"
            >
              <svg
                viewBox="0 0 24 24"
                class="h-5 w-5 shrink-0"
                fill="none"
                stroke="currentColor"
                stroke-width="1.7"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <path :d="item.icon" />
              </svg>
              <span class="truncate" :class="collapsed ? 'lg:hidden' : ''">{{ item.label }}</span>
            </RouterLink>
          </li>
        </ul>
      </template>
    </nav>

    <!-- Akun + toggle desktop -->
    <div class="shrink-0 border-t border-slate-800 p-2">
      <template v-if="isLoggedIn">
        <div class="flex items-center gap-2 rounded-lg px-2 py-2" :class="collapsed ? 'lg:justify-center lg:px-0' : ''">
          <span
            class="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-emerald-500/15 text-sm font-semibold text-emerald-300"
            aria-hidden="true"
          >{{ user.username.slice(0, 1).toUpperCase() }}</span>
          <div class="min-w-0 flex-1" :class="collapsed ? 'lg:hidden' : ''">
            <p class="truncate text-sm font-medium text-white">{{ user.username }}</p>
            <p class="text-[11px] text-slate-500">Masuk</p>
          </div>
        </div>
        <button
          type="button"
          class="mt-1 flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-slate-300 transition-colors hover:bg-slate-800 hover:text-white focus:ring-2 focus:ring-blue-500/60 focus:outline-none"
          :class="collapsed ? 'lg:justify-center lg:px-0' : ''"
          :title="collapsed ? 'Keluar' : undefined"
          @click="logout"
        >
          <svg viewBox="0 0 24 24" class="h-5 w-5 shrink-0" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true">
            <path d="M15 4h3a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-3M10 8l-4 4 4 4M6 12h9" />
          </svg>
          <span :class="collapsed ? 'lg:hidden' : ''">Keluar</span>
        </button>
      </template>

      <div v-else class="space-y-2" :class="collapsed ? 'lg:space-y-1' : ''">
        <RouterLink
          to="/login"
          class="flex items-center justify-center gap-2 rounded-lg bg-blue-500 px-3 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-600 focus:ring-2 focus:ring-blue-500/60 focus:outline-none"
          :title="collapsed ? 'Masuk' : undefined"
        >
          <span class="truncate" :class="collapsed ? 'lg:hidden' : ''">Masuk</span>
          <span v-if="collapsed" class="hidden lg:inline" aria-hidden="true">→</span>
        </RouterLink>
        <RouterLink
          to="/register"
          class="flex items-center justify-center rounded-lg border border-slate-600 px-3 py-2 text-sm text-slate-200 transition-colors hover:border-slate-500 hover:bg-slate-800 focus:ring-2 focus:ring-blue-500/60 focus:outline-none"
          :title="collapsed ? 'Daftar' : undefined"
        >
          <span class="truncate" :class="collapsed ? 'lg:hidden' : ''">Daftar</span>
          <span v-if="collapsed" class="hidden lg:inline" aria-hidden="true">✚</span>
        </RouterLink>
      </div>

      <!-- Toggle collapse (desktop) -->
      <button
        type="button"
        class="mt-2 hidden w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-slate-400 transition-colors hover:bg-slate-800 hover:text-white focus:ring-2 focus:ring-blue-500/60 focus:outline-none lg:flex"
        :class="collapsed ? 'lg:justify-center lg:px-0' : ''"
        :aria-expanded="!collapsed"
        aria-controls="app-sidebar"
        :aria-label="collapsed ? 'Lebarkan sidebar' : 'Ciutkan sidebar'"
        @click="toggleCollapsed"
      >
        <svg
          viewBox="0 0 24 24"
          class="h-5 w-5 shrink-0 transition-transform"
          :class="collapsed ? 'rotate-180' : ''"
          fill="none"
          stroke="currentColor"
          stroke-width="1.7"
          stroke-linecap="round"
          aria-hidden="true"
        >
          <path d="M11 7l-5 5 5 5M18 7l-5 5 5 5" />
        </svg>
        <span :class="collapsed ? 'lg:hidden' : ''">Ciutkan</span>
      </button>
    </div>
  </aside>
</template>
