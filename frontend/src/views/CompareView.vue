<script setup>
import { computed, ref } from 'vue'
import { useElements } from '../composables/useElements.js'
import { styleForCategory } from '../data/categories.js'

const { elements, loading, error } = useElements()

const MAX = 4
const selected = ref([]) // daftar simbol

const FIELDS = [
  { label: 'Nomor atom', get: (el) => el.atomic_number },
  { label: 'Massa atom', get: (el) => el.atomic_mass, unit: 'u' },
  { label: 'Kategori', get: (el) => el.category?.name },
  { label: 'Golongan', get: (el) => el.group },
  { label: 'Periode', get: (el) => el.period },
  { label: 'Blok', get: (el) => el.properties?.block?.toUpperCase() },
  { label: 'Fase', get: (el) => el.properties?.phase },
  { label: 'Elektronegativitas', get: (el) => el.properties?.electronegativity, unit: 'Pauling' },
  { label: 'Titik leleh', get: (el) => el.properties?.melt, unit: 'K' },
  { label: 'Titik didih', get: (el) => el.properties?.boil, unit: 'K' },
  { label: 'Massa jenis', get: (el) => el.properties?.density, unit: 'g/cm³' },
  { label: 'Jari-jari atom', get: (el) => el.properties?.atomicRadius, unit: 'pm' },
  { label: 'Cangkang elektron', get: (el) => el.properties?.shells?.join(', ') },
]

const compared = computed(() =>
  selected.value.map((symbol) => elements.value.find((el) => el.symbol === symbol)).filter(Boolean),
)

function isSelected(el) {
  return selected.value.includes(el.symbol)
}

function toggle(el) {
  if (isSelected(el)) {
    selected.value = selected.value.filter((s) => s !== el.symbol)
  } else if (selected.value.length < MAX) {
    selected.value = [...selected.value, el.symbol]
  }
}

function clear() {
  selected.value = []
}
</script>

<template>
  <section class="mx-auto max-w-6xl px-4 py-10">
    <h1 class="text-3xl font-bold">Bandingkan Unsur</h1>
    <p class="mt-2 text-slate-400">
      Pilih sampai {{ MAX }} unsur untuk membandingkan sifat dasarnya berdampingan.
    </p>

    <p v-if="loading" class="mt-8 animate-pulse text-slate-400">Memuat unsur…</p>
    <p
      v-else-if="error"
      class="mt-8 rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-red-300"
    >
      {{ error }}
    </p>

    <template v-else>
      <div class="mt-6 flex flex-wrap items-center justify-between gap-2">
        <p class="text-sm text-slate-400">
          Dipilih <span class="font-medium text-slate-200">{{ selected.length }}</span> / {{ MAX }}
        </p>
        <button
          v-if="selected.length"
          type="button"
          class="rounded-lg border border-slate-600 px-3 py-1.5 text-sm text-slate-200 transition-colors hover:border-slate-500 hover:bg-slate-800"
          @click="clear"
        >
          Kosongkan pilihan
        </button>
      </div>

      <!-- Pemilih unsur -->
      <div class="mt-3 grid max-h-80 gap-2 overflow-y-auto rounded-xl border border-slate-800 p-3 sm:grid-cols-3 lg:grid-cols-4">
        <button
          v-for="el in elements"
          :key="el.symbol"
          type="button"
          class="rounded-lg border px-3 py-2 text-left text-sm transition-colors"
          :class="
            isSelected(el)
              ? 'border-blue-500 bg-blue-500/20 text-white'
              : 'border-slate-700 bg-slate-800/40 text-slate-300 hover:border-slate-500'
          "
          :disabled="selected.length >= MAX && !isSelected(el)"
          :aria-pressed="isSelected(el)"
          @click="toggle(el)"
        >
          <span class="font-bold">{{ el.symbol }}</span> — {{ el.name }}
          <span class="ml-1 text-xs text-slate-500">{{ el.atomic_number }}</span>
        </button>
      </div>

      <p v-if="!compared.length" class="mt-8 text-sm text-slate-500">
        Pilih minimal satu unsur di atas.
      </p>

      <!-- Tabel perbandingan -->
      <div v-else class="mt-6 overflow-x-auto rounded-xl border border-slate-800">
        <table class="w-full min-w-[520px] text-left text-sm">
          <thead class="bg-slate-800/60">
            <tr>
              <th scope="col" class="p-4 text-slate-400">Sifat</th>
              <th v-for="el in compared" :key="el.symbol" scope="col" class="p-4">
                <RouterLink
                  :to="`/tabel-periodik/${el.symbol}`"
                  class="font-bold hover:underline"
                  :class="styleForCategory(el.category?.slug).text"
                >
                  {{ el.symbol }}
                </RouterLink>
                <span class="ml-1 font-normal text-slate-400">{{ el.name }}</span>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="field in FIELDS"
              :key="field.label"
              class="border-t border-slate-800"
            >
              <th scope="row" class="p-4 font-normal text-slate-400">{{ field.label }}</th>
              <td v-for="el in compared" :key="el.symbol" class="p-4 font-medium text-slate-200">
                <template v-if="field.get(el) !== null && field.get(el) !== undefined">
                  {{ field.get(el) }}<span v-if="field.unit" class="ml-1 text-xs font-normal text-slate-500">{{ field.unit }}</span>
                </template>
                <span v-else class="text-slate-600">—</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </section>
</template>
