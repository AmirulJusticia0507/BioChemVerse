<script setup>
import { onMounted, ref } from 'vue'
import { api } from '../api/client.js'

const modules = ref([])
const loading = ref(true)
const error = ref('')

const ICONS = {
  chemsphere: '⚗️',
  forensilab: '🔍',
  anatomimed: '🩺',
}

onMounted(async () => {
  try {
    const res = await api('/api/v1/modules', { auth: false })
    modules.value = res.data
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="mx-auto max-w-6xl px-4 py-12">
    <h1 class="text-3xl font-bold">Modul Pembelajaran</h1>
    <p class="mt-2 text-slate-400">
      Tiga modul utama BioChemVerse yang saling terhubung.
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
        <h2 class="text-lg font-semibold">{{ mod.name }}</h2>
        <p class="mt-2 flex-1 text-sm text-slate-400">{{ mod.description }}</p>
        <ul class="mt-4 space-y-1.5 text-sm text-slate-300">
          <li v-for="feature in mod.features" :key="feature" class="flex gap-2">
            <span class="text-emerald-500">✓</span>
            <span>{{ feature }}</span>
          </li>
        </ul>
      </article>
    </div>
  </section>
</template>
