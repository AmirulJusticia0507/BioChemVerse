<script setup>
/**
 * Status PWA di dalam sidebar: tombol "Pasang aplikasi", petunjuk iOS,
 * pemberitahuan offline, dan tawaran muat ulang saat versi baru tersedia.
 */
import { usePwa } from '../composables/usePwa.js'
import { applyUpdate, offline, updateReady } from '../composables/usePwaState.js'

defineProps({
  collapsed: { type: Boolean, default: false },
})

const { installed, canPrompt, showIosHint, promptInstall } = usePwa()
</script>

<template>
  <!-- Versi baru siap dipakai -->
  <div
    v-if="updateReady"
    class="mb-2 rounded-lg border border-blue-500/30 bg-blue-500/10 p-2 text-[11px] leading-snug text-blue-200"
    :class="collapsed ? 'lg:hidden' : ''"
    role="status"
  >
    <p>Versi baru tersedia.</p>
    <button
      type="button"
      class="mt-1.5 w-full rounded-md bg-blue-500 px-2 py-1 font-medium text-white transition-colors hover:bg-blue-600 focus:ring-2 focus:ring-blue-400 focus:outline-none"
      @click="applyUpdate?.(true)"
    >
      Muat ulang
    </button>
  </div>

  <!-- Tombol pasang (Chromium) -->
  <button
    v-if="canPrompt"
    type="button"
    class="mb-2 flex w-full items-center gap-3 rounded-lg border border-blue-500/30 bg-blue-500/10 px-3 py-2 text-sm text-blue-200 transition-colors hover:bg-blue-500/20 focus:ring-2 focus:ring-blue-500/60 focus:outline-none"
    :class="collapsed ? 'lg:justify-center lg:px-0' : ''"
    :title="collapsed ? 'Pasang aplikasi' : undefined"
    @click="promptInstall"
  >
    <svg viewBox="0 0 24 24" class="h-5 w-5 shrink-0" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M12 4v10M8 10l4 4 4-4M5 18h14" />
    </svg>
    <span :class="collapsed ? 'lg:hidden' : ''">Pasang aplikasi</span>
  </button>

  <!-- Petunjuk iOS (Safari tidak punya event instalasi) -->
  <p
    v-else-if="showIosHint"
    class="mb-2 rounded-lg border border-slate-700 bg-slate-800/60 px-3 py-2 text-[11px] leading-snug text-slate-300"
    :class="collapsed ? 'lg:hidden' : ''"
  >
    Pasang: tekan <strong class="text-slate-100">Bagikan</strong> lalu
    <strong class="text-slate-100">Tambah ke Layar Utama</strong>.
  </p>

  <!-- Sedang offline -->
  <p
    v-if="offline"
    class="mb-2 flex items-center gap-2 rounded-lg border border-amber-500/30 bg-amber-500/10 px-3 py-2 text-[11px] leading-snug text-amber-200"
    :class="collapsed ? 'lg:hidden' : ''"
    role="status"
  >
    <span class="h-2 w-2 shrink-0 rounded-full bg-amber-400" aria-hidden="true" />
    Mode offline — konten dari cache
  </p>

  <p v-if="installed" class="sr-only">Aplikasi sudah terpasang.</p>
</template>
