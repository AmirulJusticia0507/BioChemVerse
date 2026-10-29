<script setup>
import { onMounted, ref, watch } from 'vue'
import { api } from '../api/client.js'
import { useAuth } from '../composables/useAuth.js'

const { isLoggedIn, logout } = useAuth()

const modules = ref([])
const loading = ref(true)
const error = ref('')
const progress = ref({}) // module id -> { score, completed, updated_at }
const actionError = ref('')

const ICONS = {
  chemsphere: '⚗️',
  forensilab: '🔍',
  anatomimed: '🩺',
}

function pct(score) {
  return `${Math.min(100, Math.max(0, score))}%`
}

async function loadModules() {
  try {
    const res = await api('/api/v1/modules', { auth: false })
    modules.value = res.data
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function loadProgress() {
  if (!isLoggedIn.value) {
    progress.value = {}
    return
  }
  try {
    const res = await api('/api/v1/progress')
    progress.value = Object.fromEntries(res.data.map((row) => [row.module, row]))
  } catch (e) {
    if (e.status === 401) logout() // token kedaluwarsa → kembalikan ke UI tamu
    else actionError.value = e.message
  }
}

async function saveProgress(moduleId, body) {
  actionError.value = ''
  try {
    const updated = await api(`/api/v1/progress/${moduleId}`, { method: 'PUT', body })
    progress.value = { ...progress.value, [moduleId]: updated }
  } catch (e) {
    if (e.status === 401) logout()
    else actionError.value = e.message
  }
}

function bumpScore(moduleId) {
  const current = progress.value[moduleId]?.score ?? 0
  return saveProgress(moduleId, { score: Math.min(100, current + 25) })
}

function markComplete(moduleId) {
  return saveProgress(moduleId, { completed: true })
}

onMounted(loadModules)
watch(isLoggedIn, loadProgress, { immediate: true })
</script>

<template>
  <section class="mx-auto max-w-6xl px-4 py-12">
    <div class="flex flex-wrap items-end justify-between gap-3">
      <div>
        <h1 class="text-3xl font-bold">Modul Pembelajaran</h1>
        <p class="mt-2 text-slate-400">Tiga modul utama BioChemVerse yang saling terhubung.</p>
      </div>
      <p v-if="isLoggedIn" class="text-xs text-slate-500">
        Progres tersimpan otomatis ke akunmu.
      </p>
      <p v-else class="text-xs text-slate-500">
        <RouterLink to="/login?next=/modules" class="text-blue-400 hover:underline">Masuk</RouterLink>
        untuk menyimpan progres.
      </p>
    </div>

    <p
      v-if="actionError"
      class="mt-4 rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-2 text-sm text-red-300"
    >
      {{ actionError }}
    </p>

    <p v-if="loading" class="mt-8 animate-pulse text-slate-400">Memuat modul…</p>

    <p v-else-if="error" class="mt-8 rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-red-300">
      {{ error }}
    </p>

    <div v-else class="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <article
        v-for="mod in modules"
        :key="mod.id"
        class="flex flex-col rounded-xl border border-slate-800 bg-slate-800/40 p-6 transition-colors hover:border-slate-600"
      >
        <div class="mb-3 flex items-center justify-between">
          <span class="text-3xl">{{ ICONS[mod.id] ?? '📘' }}</span>
          <span class="rounded-full bg-blue-500/15 px-2 py-0.5 text-xs text-blue-400">
            {{ mod.id }}
          </span>
        </div>

        <div class="flex items-start justify-between gap-2">
          <h2 class="text-lg font-semibold">{{ mod.name }}</h2>
          <span
            v-if="progress[mod.id]?.completed"
            class="shrink-0 rounded-full bg-emerald-500/15 px-2 py-0.5 text-xs text-emerald-400"
          >
            ✓ Selesai
          </span>
        </div>

        <p class="mt-2 flex-1 text-sm text-slate-400">{{ mod.description }}</p>
        <ul class="mt-4 space-y-1.5 text-sm text-slate-300">
          <li v-for="feature in mod.features" :key="feature" class="flex gap-2">
            <span class="text-emerald-500">✓</span>
            <span>{{ feature }}</span>
          </li>
        </ul>

        <!-- Progres (hanya saat login) -->
        <div v-if="isLoggedIn" class="mt-4 border-t border-slate-700/60 pt-4">
          <div class="flex items-center justify-between text-xs text-slate-400">
            <span>Progres</span>
            <span>{{ progress[mod.id]?.score ?? 0 }}/100</span>
          </div>
          <div class="mt-1.5 h-2 overflow-hidden rounded-full bg-slate-700">
            <div
              class="h-full rounded-full bg-blue-500 transition-all duration-500"
              :style="{ width: pct(progress[mod.id]?.score ?? 0) }"
            ></div>
          </div>
          <div class="mt-3 flex gap-2">
            <button
              type="button"
              class="flex-1 rounded-lg bg-blue-500 px-3 py-1.5 text-sm font-medium text-white transition-colors hover:bg-blue-600 focus:ring-2 focus:ring-blue-500/50 focus:outline-none disabled:opacity-50"
              :disabled="(progress[mod.id]?.score ?? 0) >= 100"
              @click="bumpScore(mod.id)"
            >
              +25 poin
            </button>
            <button
              type="button"
              class="flex-1 rounded-lg border border-slate-600 px-3 py-1.5 text-sm text-slate-200 transition-colors hover:border-emerald-500 hover:text-emerald-400 disabled:opacity-50"
              :disabled="progress[mod.id]?.completed"
              @click="markComplete(mod.id)"
            >
              Tandai selesai
            </button>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>
