<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../api/client.js'
import { useAuth } from '../composables/useAuth.js'
import { useBookmarks } from '../composables/useBookmarks.js'
import { styleForCategory } from '../data/categories.js'

const route = useRoute()
const { isLoggedIn, logout } = useAuth()
const { isBookmarked, busy, load: loadBookmarks, toggle } = useBookmarks()

const element = ref(null)
const loading = ref(true)
const error = ref('')
const bookmarkError = ref('')

const style = computed(() => styleForCategory(element.value?.category?.slug))
const bookmarked = computed(() =>
  element.value ? isBookmarked(element.value.atomic_number) : false,
)
const bookmarkBusy = computed(() =>
  element.value ? busy.value.has(element.value.atomic_number) : false,
)

async function onToggleBookmark() {
  if (!element.value) return
  bookmarkError.value = ''
  try {
    await toggle(element.value)
  } catch (e) {
    if (e.status === 401) {
      logout()
      bookmarkError.value = 'Sesi berakhir — silakan masuk kembali untuk menyimpan bookmark.'
    } else {
      bookmarkError.value = e.message
    }
  }
}

/** Konversi Kelvin → Celsius (properti disimpan dalam Kelvin). */
function toCelsius(kelvin) {
  return typeof kelvin === 'number' ? Math.round((kelvin - 273.15) * 100) / 100 : null
}

function fmt(value, digits = 2) {
  if (value === null || value === undefined || value === '') return null
  if (typeof value !== 'number') return String(value)
  return value.toLocaleString('id-ID', { maximumFractionDigits: digits })
}

/** Deret properti (label, nilai, satuan) — dilewati bila nilainya kosong. */
const propertyRows = computed(() => {
  const el = element.value
  if (!el) return []
  const p = el.properties ?? {}
  const rows = []
  const push = (label, value, unit) => {
    if (value === null || value === undefined || value === '') return
    rows.push({ label, value, unit })
  }

  push('Massa atom', fmt(el.atomic_mass, 4), 'u')
  push('Periode', el.period, '')
  push('Golongan', el.group, '')
  push('Blok', p.block ? `Blok ${p.block}` : null, '')
  push('Fase (suhu ruang)', p.phase, '')
  if (typeof p.melt === 'number') push('Titik leleh', `${fmt(p.melt)} K`, `(${fmt(toCelsius(p.melt))} °C)`)
  if (typeof p.boil === 'number') push('Titik didih', `${fmt(p.boil)} K`, `(${fmt(toCelsius(p.boil))} °C)`)
  push('Massa jenis', fmt(p.density, 4), 'g/cm³')
  push('Elektronegativitas', fmt(p.electronegativity, 2), 'Pauling')
  push('Energi ionisasi', fmt(p.ionization, 1), 'kJ/mol')
  push('Jari-jari atom', fmt(p.atomicRadius, 0), 'pm')
  push('Jari-jari kovalen', fmt(p.covalentRadius, 0), 'pm')
  push('Kalor molar', fmt(p.molarHeat, 2), 'J/(mol·K)')
  push('Bilangan oksidasi', p.oxidationStates, '')
  push('Tampilan', p.appearance, '')
  push('Ditemukan oleh', p.discoveredBy, '')
  push('Diberi nama oleh', p.namedBy, '')
  if (typeof p.yearDiscovered === 'number') {
    push('Tahun ditemukan', p.yearDiscovered < 0 ? `${Math.abs(p.yearDiscovered)} SM` : p.yearDiscovered, '')
  }
  return rows
})

async function load(symbol) {
  loading.value = true
  error.value = ''
  element.value = null
  try {
    element.value = await api(`/api/v1/elements/${encodeURIComponent(symbol)}`, { auth: false })
    document.title = `${element.value.name} (${element.value.symbol}) · BioChemVerse`
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(() => load(route.params.symbol))
watch(isLoggedIn, (loggedIn) => {
  if (!loggedIn || !element.value) return
  loadBookmarks().catch((e) => {
    if (e.status === 401) logout()
  })
})
watch(
  () => route.params.symbol,
  (symbol) => {
    if (symbol) load(symbol)
  },
)
</script>

<template>
  <section class="mx-auto max-w-5xl px-4 py-10">
    <RouterLink to="/tabel-periodik" class="text-sm text-blue-400 hover:underline">
      ← Kembali ke Tabel Periodik
    </RouterLink>

    <p v-if="loading" class="mt-10 animate-pulse text-slate-400">Memuat detail unsur…</p>

    <div
      v-else-if="error"
      class="mt-10 rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-red-300"
    >
      <p>{{ error }}</p>
      <RouterLink to="/tabel-periodik" class="mt-2 inline-block text-blue-400 hover:underline">
        Kembali ke tabel periodik
      </RouterLink>
    </div>

    <template v-else-if="element">
      <!-- Kepala: kartu unsur besar -->
      <div class="mt-6 flex flex-wrap items-start gap-6">
        <div
          class="flex h-32 w-32 shrink-0 flex-col justify-between rounded-2xl border p-3"
          :class="[style.bg, style.border, style.text]"
        >
          <div class="flex items-start justify-between text-xs opacity-80">
            <span>{{ element.atomic_number }}</span>
            <span>{{ element.atomic_mass }}</span>
          </div>
          <div class="text-center text-5xl font-bold">{{ element.symbol }}</div>
          <div class="text-center text-xs font-medium opacity-90">{{ element.name }}</div>
        </div>

        <div class="min-w-52 flex-1">
          <div class="flex flex-wrap items-center gap-2">
            <h1 class="text-3xl font-bold">{{ element.name }}</h1>
            <span
              v-if="element.category"
              class="rounded-full border px-2.5 py-0.5 text-xs"
              :class="[style.bg, style.border, style.text]"
            >
              {{ element.category.name }}
            </span>
          </div>
          <p v-if="element.name_latin" class="mt-1 text-sm text-slate-400">
            Nama Latin: <span class="italic">{{ element.name_latin }}</span>
          </p>
          <p class="mt-1 text-sm text-slate-400">
            Periode {{ element.period }} · Golongan {{ element.group }}
          </p>
          <p class="mt-4 text-sm leading-relaxed text-slate-300">{{ element.description }}</p>

          <!-- Bookmark -->
          <div class="mt-4">
            <button
              v-if="isLoggedIn"
              type="button"
              class="inline-flex items-center gap-2 rounded-lg border px-3 py-1.5 text-sm transition-colors disabled:opacity-50"
              :class="
                bookmarked
                  ? 'border-amber-500/60 bg-amber-500/10 text-amber-300'
                  : 'border-slate-600 text-slate-200 hover:border-amber-500/60 hover:text-amber-300'
              "
              :aria-pressed="bookmarked"
              :disabled="bookmarkBusy"
              @click="onToggleBookmark"
            >
              <span>{{ bookmarked ? '★' : '☆' }}</span>
              {{ bookmarkBusy ? 'Menyimpan…' : bookmarked ? 'Tersimpan di bookmark' : 'Simpan ke bookmark' }}
            </button>
            <RouterLink
              v-else
              :to="`/login?next=/tabel-periodik/${element.symbol}`"
              class="text-sm text-blue-400 hover:underline"
            >
              Masuk untuk menyimpan unsur ini ke bookmark
            </RouterLink>
            <p v-if="bookmarkError" class="mt-2 text-sm text-red-400">{{ bookmarkError }}</p>
          </div>
        </div>
      </div>

      <!-- Peringatan bahaya -->
      <p
        v-if="element.hazard"
        class="mt-6 rounded-lg border border-amber-500/40 bg-amber-500/10 px-4 py-3 text-sm text-amber-300"
      >
        ⚠️ {{ element.hazard }}
      </p>

      <div class="mt-6 grid gap-6 lg:grid-cols-2">
        <!-- Properti -->
        <div class="rounded-xl border border-slate-800 bg-slate-800/40 p-5">
          <h2 class="text-lg font-semibold">Properti Fisika &amp; Kimia</h2>
          <dl class="mt-3 divide-y divide-slate-800 text-sm">
            <div
              v-for="row in propertyRows"
              :key="row.label"
              class="flex items-baseline justify-between gap-4 py-2"
            >
              <dt class="text-slate-400">{{ row.label }}</dt>
              <dd class="text-right font-medium text-slate-200">
                {{ row.value }}
                <span v-if="row.unit" class="ml-1 text-xs font-normal text-slate-500">
                  {{ row.unit }}
                </span>
              </dd>
            </div>
          </dl>
        </div>

        <div class="space-y-6">
          <!-- Kegunaan -->
          <div
            v-if="element.uses"
            class="rounded-xl border border-slate-800 bg-slate-800/40 p-5"
          >
            <h2 class="text-lg font-semibold">Kegunaan</h2>
            <p class="mt-2 text-sm leading-relaxed text-slate-300">{{ element.uses }}</p>
          </div>

          <!-- Cangkang elektron -->
          <div
            v-if="element.properties?.shells?.length"
            class="rounded-xl border border-slate-800 bg-slate-800/40 p-5"
          >
            <h2 class="text-lg font-semibold">Cangkang Elektron</h2>
            <div class="mt-3 flex flex-wrap gap-2">
              <span
                v-for="(count, i) in element.properties.shells"
                :key="i"
                class="rounded-lg border border-slate-700 bg-slate-900 px-3 py-1.5 text-sm text-slate-300"
              >
                <span class="text-slate-500">C{{ i + 1 }}:</span> {{ count }} e⁻
              </span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </section>
</template>
