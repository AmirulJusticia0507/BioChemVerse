<script setup>
import { computed, ref } from 'vue'
import { useElements } from '../composables/useElements.js'

const { elements, loading, error } = useElements()

const index = ref(0)
const flipped = ref(false)

const card = computed(() => elements.value[index.value] ?? null)

/** Top 10 unsur dengan elektronegativitas tertinggi. */
const trend = computed(() =>
  [...elements.value]
    .filter((el) => el.properties?.electronegativity != null)
    .sort((a, b) => b.properties.electronegativity - a.properties.electronegativity)
    .slice(0, 10),
)

/** Tabel kelarutan ringkas (aturan umum garam). */
const SOLUBILITY = [
  { rule: 'Nitrat, asetat, amonium', result: 'Larut', ok: true },
  { rule: 'Klorida', result: 'Larut, kecuali Ag⁺, Pb²⁺, Hg₂²⁺', ok: true },
  { rule: 'Sulfat', result: 'Larut, kecuali Ba²⁺, Pb²⁺, Sr²⁺', ok: true },
  { rule: 'Karbonat, fosfat, hidroksida', result: 'Umumnya tak larut, kecuali alkali & amonium', ok: true },
  { rule: 'Sulfida', result: 'Umumnya tak larut, kecuali alkali & amonium', ok: false },
]

function next(step = 1) {
  if (!elements.value.length) return
  index.value = (index.value + step + elements.value.length) % elements.value.length
  flipped.value = false
}
</script>

<template>
  <section class="mx-auto max-w-6xl px-4 py-10">
    <h1 class="text-3xl font-bold">Ruang Belajar</h1>
    <p class="mt-2 text-slate-400">
      Flashcard unsur, tren elektronegativitas, dan aturan kelarutan garam.
    </p>

    <p v-if="loading" class="mt-8 animate-pulse text-slate-400">Memuat materi…</p>
    <p
      v-else-if="error"
      class="mt-8 rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-red-300"
    >
      {{ error }}
    </p>

    <template v-else-if="card">
      <div class="mt-6 grid gap-6 lg:grid-cols-2">
        <!-- Flashcard -->
        <div class="rounded-xl border border-slate-800 bg-slate-800/40 p-6">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-semibold">Flashcard</h2>
            <span class="text-xs text-slate-500">
              {{ index + 1 }} / {{ elements.length }}
            </span>
          </div>

          <button
            type="button"
            class="mt-4 w-full rounded-xl border border-slate-700 bg-slate-900 px-6 py-12 text-center transition-colors hover:border-blue-500/60 focus:ring-2 focus:ring-blue-500/50 focus:outline-none"
            :aria-label="flipped ? `Balik kartu: ${card.symbol}` : `Balik kartu: ${card.name}`"
            @click="flipped = !flipped"
          >
            <strong class="block text-6xl font-bold text-white">
              {{ flipped ? card.name : card.symbol }}
            </strong>
            <span class="mt-4 block text-sm text-slate-400">
              {{ flipped ? `${card.atomic_number} · ${card.atomic_mass} u` : 'Klik untuk melihat jawaban' }}
            </span>
          </button>

          <div class="mt-4 flex gap-2">
            <button
              type="button"
              class="rounded-lg border border-slate-600 px-3 py-2 text-sm text-slate-200 transition-colors hover:border-slate-500 hover:bg-slate-800"
              @click="next(-1)"
            >
              ← Sebelumnya
            </button>
            <button
              type="button"
              class="flex-1 rounded-lg bg-blue-500 px-3 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-600"
              @click="next(1)"
            >
              Berikutnya →
            </button>
          </div>
        </div>

        <!-- Tren elektronegativitas -->
        <div class="rounded-xl border border-slate-800 bg-slate-800/40 p-6">
          <h2 class="text-lg font-semibold">Tren Elektronegativitas</h2>
          <p class="mt-1 text-xs text-slate-500">10 unsur dengan nilai tertinggi (skala Pauling)</p>
          <ol class="mt-4 space-y-1.5 text-sm">
            <li
              v-for="(el, i) in trend"
              :key="el.symbol"
              class="flex items-center gap-3 border-b border-slate-800 pb-1.5 last:border-0"
            >
              <span class="w-5 text-right text-xs text-slate-500">{{ i + 1 }}</span>
              <RouterLink
                :to="`/tabel-periodik/${el.symbol}`"
                class="flex-1 text-slate-300 hover:underline"
              >
                <span class="font-semibold">{{ el.symbol }}</span> — {{ el.name }}
              </RouterLink>
              <span class="font-mono text-emerald-400">
                {{ el.properties.electronegativity }}
              </span>
            </li>
          </ol>
        </div>
      </div>

      <!-- Tabel kelarutan -->
      <div class="mt-6 rounded-xl border border-slate-800 bg-slate-800/40 p-6">
        <h2 class="text-lg font-semibold">Tabel Kelarutan Ringkas</h2>
        <p class="mt-1 text-xs text-slate-500">
          Kelarutan garam dalam air pada suhu ruang (aturan umum).
        </p>
        <table class="mt-4 w-full text-left text-sm">
          <tbody>
            <tr v-for="row in SOLUBILITY" :key="row.rule" class="border-b border-slate-800 last:border-0">
              <th scope="row" class="w-1/3 py-2 pr-4 font-medium text-slate-300">
                {{ row.rule }}
              </th>
              <td class="py-2" :class="row.ok ? 'text-emerald-400' : 'text-amber-400'">
                {{ row.result }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </section>
</template>
