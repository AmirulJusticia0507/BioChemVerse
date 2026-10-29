<script setup>
/**
 * Kerangka halaman dokumen statis (Tentang, Bantuan, Kebijakan Privasi, Kebijakan Cookies).
 * Menjaga tipografi & jarak konten panjang tetap seragam di semua halaman legal/dukungan.
 */
import { ref } from 'vue'

defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  updated: { type: String, default: '' },
})

// Daftar section dipakai untuk daftar isi (anchor cepat).
const sections = ref([])

defineExpose({ sections })
</script>

<template>
  <article class="mx-auto max-w-3xl px-4 py-10 sm:py-14">
    <header class="border-b border-slate-800 pb-6">
      <h1 class="text-2xl font-bold sm:text-3xl">{{ title }}</h1>
      <p v-if="subtitle" class="mt-2 text-slate-400">{{ subtitle }}</p>
      <p v-if="updated" class="mt-3 text-xs text-slate-500">Terakhir diperbarui: {{ updated }}</p>
    </header>

    <div class="doc mt-8">
      <slot />
    </div>
  </article>
</template>

<style scoped>
/* Tipografi konten dokumen: anak komponen boleh memakai tag HTML polos. */
.doc :deep(h2) {
  margin-top: 2.25rem;
  margin-bottom: 0.75rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: rgb(226 232 240);
  scroll-margin-top: 5rem;
}

.doc :deep(h3) {
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: rgb(226 232 240);
}

.doc :deep(p) {
  margin-bottom: 0.875rem;
  line-height: 1.75;
  color: rgb(148 163 184);
}

.doc :deep(ul),
.doc :deep(ol) {
  margin-bottom: 0.875rem;
  padding-left: 1.25rem;
  line-height: 1.75;
  color: rgb(148 163 184);
}

.doc :deep(ul) {
  list-style: disc;
}

.doc :deep(ol) {
  list-style: decimal;
}

.doc :deep(li) {
  margin-bottom: 0.375rem;
}

.doc :deep(strong) {
  color: rgb(203 213 225);
  font-weight: 600;
}

.doc :deep(a) {
  color: rgb(147 197 253);
  text-decoration: underline;
  text-underline-offset: 2px;
}

.doc :deep(a:hover) {
  color: rgb(191 219 254);
}

.doc :deep(code) {
  padding: 0.1rem 0.35rem;
  border-radius: 0.25rem;
  background: rgb(30 41 59);
  font-size: 0.85em;
  color: rgb(203 213 225);
}

.doc :deep(table) {
  width: 100%;
  margin-bottom: 1rem;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.doc :deep(th),
.doc :deep(td) {
  padding: 0.5rem 0.75rem;
  border: 1px solid rgb(30 41 59);
  text-align: left;
  vertical-align: top;
}

.doc :deep(th) {
  background: rgb(15 23 42);
  color: rgb(226 232 240);
  font-weight: 600;
}

/* Tabel lebar di layar sempit: geser di dalam wadah, bukan melebarkan halaman. */
.doc :deep(.table-scroll) {
  margin-bottom: 1rem;
  overflow-x: auto;
}

.doc :deep(.table-scroll table) {
  min-width: 34rem;
  margin-bottom: 0;
}
</style>
