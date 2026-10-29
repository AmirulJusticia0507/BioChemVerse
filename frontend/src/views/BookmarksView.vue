<script setup>
import { onBeforeUnmount, onMounted, watch } from 'vue'
import { useAuth } from '../composables/useAuth.js'
import { useBookmarks } from '../composables/useBookmarks.js'
import { styleForCategory } from '../data/categories.js'

const { isLoggedIn, logout } = useAuth()
const { items, loading, busy, error, load, remove, reset } = useBookmarks()

async function refresh(force = true) {
  if (!isLoggedIn.value) return
  try {
    await load(force)
  } catch (e) {
    if (e.status === 401) logout()
  }
}

async function drop(atomicNumber) {
  try {
    await remove(atomicNumber)
  } catch (e) {
    if (e.status === 401) logout()
  }
}

onMounted(() => refresh(false))
watch(isLoggedIn, (loggedIn) => {
  if (loggedIn) refresh()
  else reset()
})
</script>

<template>
  <section class="mx-auto max-w-4xl px-4 py-10">
    <div class="flex flex-wrap items-end justify-between gap-3">
      <div>
        <h1 class="text-3xl font-bold">Bookmark Unsur</h1>
        <p class="mt-2 text-slate-400">Unsur yang kamu simpan dari halaman detail unsur.</p>
      </div>
      <p v-if="isLoggedIn" class="text-xs text-slate-500">{{ items.length }} unsur tersimpan</p>
    </div>

    <!-- Wajib login -->
    <div
      v-if="!isLoggedIn"
      class="mt-8 rounded-xl border border-slate-800 bg-slate-800/40 p-6 text-center"
    >
      <p class="text-slate-300">Masuk untuk melihat bookmark unsur milikmu.</p>
      <div class="mt-4 flex justify-center gap-2">
        <RouterLink
          to="/login?next=/bookmark"
          class="rounded-lg bg-blue-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-600"
        >
          Masuk
        </RouterLink>
        <RouterLink
          to="/tabel-periodik"
          class="rounded-lg border border-slate-600 px-4 py-2 text-sm text-slate-200 transition-colors hover:border-slate-500 hover:bg-slate-800"
        >
          Jelajahi tabel periodik
        </RouterLink>
      </div>
    </div>

    <template v-else>
      <p
        v-if="error"
        class="mt-6 rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-300"
      >
        {{ error }}
      </p>

      <p v-if="loading && !items.length" class="mt-8 animate-pulse text-slate-400">Memuat bookmark…</p>

      <div v-else-if="!items.length" class="mt-8 rounded-xl border border-dashed border-slate-700 p-8 text-center">
        <p class="text-slate-300">Belum ada unsur yang dibookmark.</p>
        <RouterLink
          to="/tabel-periodik"
          class="mt-3 inline-block text-sm text-blue-400 hover:underline"
        >
          Buka Tabel Periodik →
        </RouterLink>
      </div>

      <ul v-else class="mt-6 space-y-2">
        <li
          v-for="row in items"
          :key="row.atomic_number"
          class="flex flex-wrap items-center gap-3 rounded-xl border border-slate-800 bg-slate-800/40 p-4"
        >
          <span
            class="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg border text-lg font-bold"
            :class="[
              styleForCategory(row.category_slug).bg,
              styleForCategory(row.category_slug).border,
              styleForCategory(row.category_slug).text,
            ]"
          >
            {{ row.symbol }}
          </span>

          <div class="min-w-40 flex-1">
            <RouterLink
              :to="`/tabel-periodik/${row.symbol}`"
              class="font-semibold text-slate-100 hover:underline"
            >
              {{ row.name }}
            </RouterLink>
            <p class="text-xs text-slate-500">
              Nomor atom {{ row.atomic_number }}
              <span v-if="row.note"> · {{ row.note }}</span>
            </p>
          </div>

          <button
            type="button"
            class="rounded-lg border border-slate-600 px-3 py-1.5 text-sm text-slate-200 transition-colors hover:border-red-500 hover:text-red-400 disabled:opacity-50"
            :disabled="busy.has(row.atomic_number)"
            @click="drop(row.atomic_number)"
          >
            {{ busy.has(row.atomic_number) ? 'Menghapus…' : 'Hapus' }}
          </button>
        </li>
      </ul>
    </template>
  </section>
</template>
