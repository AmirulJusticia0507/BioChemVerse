<script setup>
import { computed, ref } from 'vue'
import { prettyFormula } from '../utils/formula.js'
import { useElements } from '../composables/useElements.js'
import {
  MOLAR_VOLUME_STP,
  balanceEquation,
  dilution,
  massFromMoles,
  molarMassOf,
  molarity,
  molesFromMass,
  molesFromParticles,
  particlesFromMoles,
  volumeFromMoles,
} from '../utils/stoichiometry.js'

const { elements, loading, error } = useElements()

const massBySymbol = computed(() => {
  const map = {}
  for (const el of elements.value) map[el.symbol] = Number(el.atomic_mass)
  return map
})
const massOf = (symbol) => massBySymbol.value[symbol] ?? null

const TABS = [
  { id: 'massa', label: 'Massa Molar' },
  { id: 'setara', label: 'Penyetara Reaksi' },
  { id: 'mol', label: 'Mol & Partikel' },
  { id: 'larutan', label: 'Larutan' },
]
const activeTab = ref('massa')

function fmt(value, digits = 4) {
  if (value === null || value === undefined || !Number.isFinite(value)) return '—'
  return value.toLocaleString('id-ID', { maximumFractionDigits: digits })
}

// --- Massa molar ------------------------------------------------------------
const molarInput = ref('H2O')
const molarResult = computed(() => {
  const formula = molarInput.value.trim()
  if (!formula) return null
  const { total, missing, breakdown } = molarMassOf(formula, massOf)
  if (missing.length) return { error: `Unsur tidak dikenali: ${missing.join(', ')}` }
  if (!breakdown.length) return { error: 'Rumus tidak dapat dibaca.' }
  return { total, breakdown }
})

// --- Penyetara reaksi -------------------------------------------------------
const equationInput = ref('Fe2O3 + CO -> Fe + CO2')
const balanceResult = computed(() => balanceEquation(equationInput.value))
const balanceExamples = [
  'H2 + O2 -> H2O',
  'CH4 + O2 -> CO2 + H2O',
  'Fe + O2 -> Fe2O3',
  'NaOH + H2SO4 -> Na2SO4 + H2O',
  'KClO3 -> KCl + O2',
]

// --- Mol, massa, partikel ---------------------------------------------------
const MOL_MODES = [
  { id: 'massa-ke-mol', label: 'Massa → mol', unit: 'gram', hint: 'Massa zat (g)' },
  { id: 'mol-ke-massa', label: 'Mol → massa', unit: 'mol', hint: 'Jumlah mol' },
  { id: 'partikel-ke-mol', label: 'Partikel → mol', unit: 'partikel', hint: 'Jumlah partikel' },
]
const molMode = ref('massa-ke-mol')
const molFormula = ref('H2O')
const molValue = ref('')
const molUnit = computed(() => MOL_MODES.find((m) => m.id === molMode.value)?.unit ?? '')
const molHint = computed(() => MOL_MODES.find((m) => m.id === molMode.value)?.hint ?? '')

const molMolarMass = computed(() => {
  const { total, missing } = molarMassOf(molFormula.value.trim(), massOf)
  if (missing.length || !total) return null
  return total
})

const molResult = computed(() => {
  const value = Number(molValue.value)
  if (!Number.isFinite(value) || value < 0) return null
  const M = molMolarMass.value
  if (!M) return null

  if (molMode.value === 'massa-ke-mol') {
    const moles = molesFromMass(value, M)
    return {
      primary: `${fmt(moles, 6)} mol`,
      rows: [
        ['Mol (n)', `${fmt(moles, 6)} mol`],
        ['Jumlah partikel', `${fmt(particlesFromMoles(moles), 4)} partikel`],
        ['Volume gas pada STP', `${fmt(volumeFromMoles(moles), 4)} L`],
      ],
    }
  }
  if (molMode.value === 'mol-ke-massa') {
    const mass = massFromMoles(value, M)
    return {
      primary: `${fmt(mass, 4)} g`,
      rows: [
        ['Massa (m)', `${fmt(mass, 4)} g`],
        ['Jumlah partikel', `${fmt(particlesFromMoles(value), 4)} partikel`],
        ['Volume gas pada STP', `${fmt(volumeFromMoles(value), 4)} L`],
      ],
    }
  }
  const moles = molesFromParticles(value)
  return {
    primary: `${fmt(moles, 8)} mol`,
    rows: [
      ['Mol (n)', `${fmt(moles, 8)} mol`],
      ['Massa (m)', `${fmt(massFromMoles(moles, M), 6)} g`],
      ['Volume gas pada STP', `${fmt(volumeFromMoles(moles), 6)} L`],
    ],
  }
})

// --- Larutan ----------------------------------------------------------------
const SOLUTION_MODES = [
  { id: 'molaritas', label: 'Molaritas (M = n/V)' },
  { id: 'massa-molaritas', label: 'Massa → molaritas' },
  { id: 'pengenceran', label: 'Pengenceran (M₁V₁ = M₂V₂)' },
]
const solutionMode = ref('molaritas')
const solutionForm = ref({
  moles: '',
  volume: '',
  mass: '',
  molarMass: '',
  m1: '',
  v1: '',
  m2: '',
  v2: '',
})

const solutionResult = computed(() => {
  const form = solutionForm.value

  if (solutionMode.value === 'molaritas') {
    const moles = Number(form.moles)
    const volume = Number(form.volume)
    if (!Number.isFinite(moles) || !Number.isFinite(volume) || volume <= 0) return null
    const M = molarity(moles, volume)
    return { primary: `${fmt(M, 4)} M`, rows: [['Konsentrasi', `${fmt(M, 4)} mol/L`]] }
  }

  if (solutionMode.value === 'massa-molaritas') {
    const mass = Number(form.mass)
    const volume = Number(form.volume)
    const mm = Number(form.molarMass)
    if (![mass, volume, mm].every((v) => Number.isFinite(v)) || volume <= 0 || mm <= 0) return null
    const moles = molesFromMass(mass, mm)
    const M = molarity(moles, volume)
    return {
      primary: `${fmt(M, 4)} M`,
      rows: [
        ['Mol zat terlarut', `${fmt(moles, 6)} mol`],
        ['Konsentrasi', `${fmt(M, 4)} mol/L`],
      ],
    }
  }

  const parse = (value) => (value === '' || value === null ? null : Number(value))
  const result = dilution({
    m1: parse(form.m1),
    v1: parse(form.v1),
    m2: parse(form.m2),
    v2: parse(form.v2),
  })
  if (result.error) return { error: result.error }
  return {
    primary: fmt(result.value, 4),
    rows: [
      ['Nilai yang dihitung', result.solvedFor],
      ['Hasil', fmt(result.value, 4)],
    ],
  }
})

const CONSTANTS = [
  ['Bilangan Avogadro', '6,022 × 10²³ partikel/mol'],
  ['Volume molar gas (STP)', `${MOLAR_VOLUME_STP} L/mol`],
]
</script>

<template>
  <section class="mx-auto max-w-5xl px-4 py-10">
    <h1 class="text-3xl font-bold">Kalkulator Stoikiometri</h1>
    <p class="mt-2 text-slate-400">
      Massa molar, penyetaraan reaksi, konversi mol, dan perhitungan larutan — data massa atom dari
      tabel periodik.
    </p>

    <p v-if="loading" class="mt-8 animate-pulse text-slate-400">Memuat data unsur…</p>
    <p
      v-else-if="error"
      class="mt-8 rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-red-300"
    >
      {{ error }}
    </p>

    <template v-else>
      <!-- Tab -->
      <div class="mt-6 flex flex-wrap gap-2" role="tablist">
        <button
          v-for="tab in TABS"
          :key="tab.id"
          type="button"
          role="tab"
          :aria-selected="activeTab === tab.id"
          class="rounded-lg px-3 py-2 text-sm transition-colors"
          :class="
            activeTab === tab.id
              ? 'bg-blue-500 font-medium text-white'
              : 'border border-slate-700 text-slate-300 hover:border-slate-500 hover:bg-slate-800'
          "
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Massa molar -->
      <div v-if="activeTab === 'massa'" class="mt-6 rounded-xl border border-slate-800 bg-slate-800/40 p-6">
        <label class="block">
          <span class="mb-1 block text-xs text-slate-400">Rumus kimia (mendukung tanda kurung)</span>
          <input
            v-model="molarInput"
            type="text"
            placeholder="mis. Al2(SO4)3"
            class="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 font-mono text-white placeholder:text-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
          />
        </label>

        <p v-if="molarResult?.error" class="mt-4 text-sm text-amber-400">{{ molarResult.error }}</p>

        <div v-else-if="molarResult" class="mt-4">
          <p class="text-sm text-slate-400">
            Massa molar
            <span class="font-mono text-slate-200">{{ prettyFormula(molarInput.trim()) }}</span>
          </p>
          <p class="mt-1 text-3xl font-bold text-emerald-400">
            {{ fmt(molarResult.total, 4) }}
            <span class="text-base font-normal text-slate-400">g/mol</span>
          </p>

          <table class="mt-4 w-full text-left text-sm">
            <thead>
              <tr class="border-b border-slate-700 text-slate-400">
                <th class="py-2">Unsur</th>
                <th class="py-2 text-right">Jumlah atom</th>
                <th class="py-2 text-right">Massa atom (u)</th>
                <th class="py-2 text-right">Subtotal (g/mol)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in molarResult.breakdown" :key="row.symbol" class="border-b border-slate-800">
                <td class="py-2 font-medium text-slate-200">{{ row.symbol }}</td>
                <td class="py-2 text-right text-slate-300">{{ row.count }}</td>
                <td class="py-2 text-right text-slate-300">{{ fmt(row.mass, 4) }}</td>
                <td class="py-2 text-right text-slate-200">{{ fmt(row.subtotal, 4) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Penyetara reaksi -->
      <div v-else-if="activeTab === 'setara'" class="mt-6 rounded-xl border border-slate-800 bg-slate-800/40 p-6">
        <label class="block">
          <span class="mb-1 block text-xs text-slate-400">
            Persamaan reaksi (gunakan <code class="text-slate-300">-&gt;</code> atau
            <code class="text-slate-300">→</code>)
          </span>
          <input
            v-model="equationInput"
            type="text"
            class="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 font-mono text-white placeholder:text-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
          />
        </label>

        <p v-if="!balanceResult.ok" class="mt-4 text-sm text-amber-400">
          {{ balanceResult.error }}
        </p>
        <p v-else class="mt-4 rounded-lg bg-slate-900 px-4 py-3 font-mono text-lg text-emerald-400">
          {{ balanceResult.balanced }}
        </p>

        <div class="mt-4 flex flex-wrap gap-2">
          <button
            v-for="example in balanceExamples"
            :key="example"
            type="button"
            class="rounded-lg border border-slate-700 px-2.5 py-1 text-xs text-slate-300 transition-colors hover:border-slate-500 hover:bg-slate-800"
            @click="equationInput = example"
          >
            {{ example }}
          </button>
        </div>
      </div>

      <!-- Mol & partikel -->
      <div v-else-if="activeTab === 'mol'" class="mt-6 rounded-xl border border-slate-800 bg-slate-800/40 p-6">
        <div class="grid gap-4 sm:grid-cols-2">
          <label class="block">
            <span class="mb-1 block text-xs text-slate-400">Rumus kimia</span>
            <input
              v-model="molFormula"
              type="text"
              class="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 font-mono text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
            />
          </label>
          <label class="block">
            <span class="mb-1 block text-xs text-slate-400">Konversi</span>
            <select
              v-model="molMode"
              class="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
            >
              <option v-for="mode in MOL_MODES" :key="mode.id" :value="mode.id">
                {{ mode.label }}
              </option>
            </select>
          </label>
        </div>

        <label class="mt-4 block">
          <span class="mb-1 block text-xs text-slate-400">{{ molHint }}</span>
          <input
            v-model="molValue"
            type="number"
            min="0"
            step="any"
            class="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
          />
        </label>

        <p v-if="!molMolarMass" class="mt-4 text-sm text-amber-400">
          Rumus tidak dikenali — periksa kembali simbol unsurnya.
        </p>
        <div v-else-if="molResult" class="mt-4">
          <p class="text-xs text-slate-500">
            Massa molar (Mᵣ) = <span class="text-slate-300">{{ fmt(molMolarMass, 4) }}</span> g/mol
          </p>
          <p class="mt-1 text-3xl font-bold text-emerald-400">{{ molResult.primary }}</p>
          <dl class="mt-3 divide-y divide-slate-800 text-sm">
            <div v-for="[label, value] in molResult.rows" :key="label" class="flex justify-between py-2">
              <dt class="text-slate-400">{{ label }}</dt>
              <dd class="font-medium text-slate-200">{{ value }}</dd>
            </div>
          </dl>
        </div>
      </div>

      <!-- Larutan -->
      <div v-else class="mt-6 rounded-xl border border-slate-800 bg-slate-800/40 p-6">
        <label class="block">
          <span class="mb-1 block text-xs text-slate-400">Jenis perhitungan</span>
          <select
            v-model="solutionMode"
            class="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
          >
            <option v-for="mode in SOLUTION_MODES" :key="mode.id" :value="mode.id">
              {{ mode.label }}
            </option>
          </select>
        </label>

        <div class="mt-4 grid gap-4 sm:grid-cols-2">
          <template v-if="solutionMode === 'molaritas'">
            <label class="block">
              <span class="mb-1 block text-xs text-slate-400">Mol zat terlarut (mol)</span>
              <input v-model="solutionForm.moles" type="number" step="any" class="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-white focus:border-blue-500 focus:outline-none" />
            </label>
            <label class="block">
              <span class="mb-1 block text-xs text-slate-400">Volume larutan (L)</span>
              <input v-model="solutionForm.volume" type="number" step="any" class="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-white focus:border-blue-500 focus:outline-none" />
            </label>
          </template>

          <template v-else-if="solutionMode === 'massa-molaritas'">
            <label class="block">
              <span class="mb-1 block text-xs text-slate-400">Massa zat (g)</span>
              <input v-model="solutionForm.mass" type="number" step="any" class="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-white focus:border-blue-500 focus:outline-none" />
            </label>
            <label class="block">
              <span class="mb-1 block text-xs text-slate-400">Massa molar (g/mol)</span>
              <input v-model="solutionForm.molarMass" type="number" step="any" class="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-white focus:border-blue-500 focus:outline-none" />
            </label>
            <label class="block">
              <span class="mb-1 block text-xs text-slate-400">Volume larutan (L)</span>
              <input v-model="solutionForm.volume" type="number" step="any" class="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-white focus:border-blue-500 focus:outline-none" />
            </label>
          </template>

          <template v-else>
            <label class="block">
              <span class="mb-1 block text-xs text-slate-400">M₁ (M) — kosongkan untuk dihitung</span>
              <input v-model="solutionForm.m1" type="number" step="any" class="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-white focus:border-blue-500 focus:outline-none" />
            </label>
            <label class="block">
              <span class="mb-1 block text-xs text-slate-400">V₁ (L)</span>
              <input v-model="solutionForm.v1" type="number" step="any" class="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-white focus:border-blue-500 focus:outline-none" />
            </label>
            <label class="block">
              <span class="mb-1 block text-xs text-slate-400">M₂ (M)</span>
              <input v-model="solutionForm.m2" type="number" step="any" class="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-white focus:border-blue-500 focus:outline-none" />
            </label>
            <label class="block">
              <span class="mb-1 block text-xs text-slate-400">V₂ (L)</span>
              <input v-model="solutionForm.v2" type="number" step="any" class="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-white focus:border-blue-500 focus:outline-none" />
            </label>
          </template>
        </div>

        <p v-if="solutionResult?.error" class="mt-4 text-sm text-amber-400">
          {{ solutionResult.error }}
        </p>
        <div v-else-if="solutionResult" class="mt-4">
          <p class="text-3xl font-bold text-emerald-400">{{ solutionResult.primary }}</p>
          <dl class="mt-3 divide-y divide-slate-800 text-sm">
            <div v-for="[label, value] in solutionResult.rows" :key="label" class="flex justify-between py-2">
              <dt class="text-slate-400">{{ label }}</dt>
              <dd class="font-medium text-slate-200">{{ value }}</dd>
            </div>
          </dl>
        </div>
      </div>

      <!-- Konstanta -->
      <div class="mt-6 flex flex-wrap gap-x-6 gap-y-2 text-xs text-slate-500">
        <span v-for="[label, value] in CONSTANTS" :key="label">
          <span class="text-slate-400">{{ label }}:</span> {{ value }}
        </span>
      </div>
    </template>
  </section>
</template>
