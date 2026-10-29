<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api/client.js'
import { isActinide, isFBlock, isLanthanide, styleForCategory } from '../data/categories.js'

const router = useRouter()

const elements = ref([])
const categories = ref([])
const ions = ref([])
const loading = ref(true)
const error = ref('')

// Filter (disaring di sisi klien agar tabel tetap utuh & responsif)
const search = ref('')
const categoryFilter = ref('')
const blockFilter = ref('')
const phaseFilter = ref('')

const GROUPS = Array.from({ length: 18 }, (_, i) => i + 1)
const PERIODS = Array.from({ length: 7 }, (_, i) => i + 1)
const BLOCKS = ['s', 'p', 'd', 'f']
const PHASES = ['Solid', 'Liquid', 'Gas', 'Artificial']

const mainElements = computed(() => elements.value.filter((el) => !isFBlock(el)))
const lanthanides = computed(() => elements.value.filter((el) => isLanthanide(el.atomic_number)))
const actinides = computed(() => elements.value.filter((el) => isActinide(el.atomic_number)))

const legend = computed(() =>
  categories.value.map((c) => ({ ...styleForCategory(c.slug), slug: c.slug, count: c.element_count })),
)

const matchedCount = computed(() => elements.value.filter((el) => matches(el)).length)
const hasFilter = computed(
  () => search.value.trim() || categoryFilter.value || blockFilter.value || phaseFilter.value,
)

function matches(el) {
  const q = search.value.trim().toLowerCase()
  if (q) {
    const hit =
      el.name.toLowerCase().includes(q) ||
      (el.name_latin ?? '').toLowerCase().includes(q) ||
      el.symbol.toLowerCase() === q ||
      el.symbol.toLowerCase().startsWith(q) ||
      String(el.atomic_number) === q
    if (!hit) return false
  }
  if (categoryFilter.value && el.category?.slug !== categoryFilter.value) return false
  if (blockFilter.value && el.properties?.block !== blockFilter.value) return false
  if (phaseFilter.value && el.properties?.phase !== phaseFilter.value) return false
  return true
}

function tileClass(el) {
  const style = styleForCategory(el.category?.slug)
  return matches(el)
    ? `${style.bg} ${style.text} border ${style.border}`
    : 'border border-slate-800 bg-slate-800/30 text-slate-600 opacity-40'
}

function openElement(el) {
  router.push(`/tabel-periodik/${el.symbol}`)
}

function resetFilters() {
  search.value = ''
  categoryFilter.value = ''
  blockFilter.value = ''
  phaseFilter.value = ''
}

async function load() {
  try {
    const [elRes, catRes, ionRes] = await Promise.all([
      api('/api/v1/elements', { auth: false }),
      api('/api/v1/categories', { auth: false }),
      api('/api/v1/ions', { auth: false }),
    ])
    elements.value = elRes.data
    categories.value = catRes.data
    ions.value = ionRes.data
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <section class="mx-auto max-w-6xl px-4 py-10">
    <div class="flex flex-wrap items-end justify-between gap-3">
      <div>
        <h1 class="text-3xl font-bold">Tabel Periodik</h1>
        <p class="mt-2 text-slate-400">
          118 unsur dalam Bahasa Indonesia — klik kartu untuk detail lengkap.
        </p>
      </div>
      <p class="text-xs text-slate-500">
        <template v-if="!loading && elements.length">
          <span class="font-medium text-slate-300">{{ matchedCount }}</span> /
          {{ elements.length }} unsur cocok
        </template>
        <template v-else>Memuat…</template>
      </p>
    </div>

    <!-- Filter -->
    <div class="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      <label class="block">
        <span class="mb-1 block text-xs text-slate-400">Pencarian</span>
        <input
          v-model="search"
          type="search"
          placeholder="Nama, simbol, atau nomor atom…"
          class="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
        />
      </label>

      <label class="block">
        <span class="mb-1 block text-xs text-slate-400">Kategori</span>
        <select
          v-model="categoryFilter"
          class="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
        >
          <option value="">Semua kategori</option>
          <option v-for="c in categories" :key="c.slug" :value="c.slug">
            {{ c.name }} ({{ c.element_count }})
          </option>
        </select>
      </label>

      <label class="block">
        <span class="mb-1 block text-xs text-slate-400">Blok</span>
        <select
          v-model="blockFilter"
          class="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
        >
          <option value="">Semua blok</option>
          <option v-for="b in BLOCKS" :key="b" :value="b">Blok {{ b }}</option>
        </select>
      </label>

      <label class="block">
        <span class="mb-1 block text-xs text-slate-400">Fase (suhu ruang)</span>
        <select
          v-model="phaseFilter"
          class="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
        >
          <option value="">Semua fase</option>
          <option v-for="p in PHASES" :key="p" :value="p">{{ p }}</option>
        </select>
      </label>
    </div>

    <p v-if="hasFilter" class="mt-3 text-xs text-slate-500">
      Kartu yang tidak cocok ditampilkan redup.
      <button type="button" class="ml-1 text-blue-400 hover:underline" @click="resetFilters">
        Atur ulang filter
      </button>
    </p>

    <p v-if="loading" class="mt-10 animate-pulse text-slate-400">Memuat tabel periodik…</p>

    <p
      v-else-if="error"
      class="mt-10 rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-red-300"
    >
      {{ error }}
    </p>

    <template v-else>
      <!-- Grid utama: 18 golongan × 7 periode (kolom 1 = nomor periode) -->
      <div class="mt-6 overflow-x-auto pb-2">
        <div
          class="grid min-w-[920px] gap-1.5"
          style="grid-template-columns: 18px repeat(18, minmax(0, 1fr))"
          role="list"
          aria-label="Tabel periodik unsur"
        >
          <!-- Nomor golongan -->
          <div
            v-for="g in GROUPS"
            :key="`g-${g}`"
            class="pb-1 text-center text-[10px] text-slate-500"
            :style="{ gridColumn: g + 1, gridRow: 1 }"
          >
            {{ g }}
          </div>
          <!-- Nomor periode -->
          <div
            v-for="p in PERIODS"
            :key="`p-${p}`"
            class="flex items-center justify-center text-[10px] text-slate-500"
            :style="{ gridColumn: 1, gridRow: p + 1 }"
          >
            {{ p }}
          </div>

          <div
            v-for="el in mainElements"
            :key="el.symbol"
            class="aspect-square cursor-pointer rounded-md p-1 transition-transform hover:scale-105 hover:shadow-md focus-within:ring-2 focus-within:ring-blue-400/60"
            :class="tileClass(el)"
            :style="{ gridColumn: el.group + 1, gridRow: el.period + 1 }"
            role="listitem"
            :tabindex="0"
            :aria-label="`${el.name} (${el.symbol}) nomor atom ${el.atomic_number}`"
            @click="openElement(el)"
            @keydown.enter="openElement(el)"
          >
            <div class="text-[9px] leading-tight opacity-70">{{ el.atomic_number }}</div>
            <div class="text-center text-sm font-bold sm:text-base">{{ el.symbol }}</div>
            <div class="truncate text-center text-[8px] leading-tight opacity-80">
              {{ el.name }}
            </div>
          </div>

          <!-- Slot placeholder blok f -->
          <a
            v-if="lanthanides.length"
            href="#lantanida"
            class="flex aspect-square items-center justify-center rounded-md border border-dashed border-pink-500/40 bg-pink-500/10 text-[9px] font-bold text-pink-400 no-underline"
            :style="{ gridColumn: 4, gridRow: 7 }"
          >
            57–71
          </a>
          <a
            v-if="actinides.length"
            href="#aktinida"
            class="flex aspect-square items-center justify-center rounded-md border border-dashed border-rose-500/40 bg-rose-500/10 text-[9px] font-bold text-rose-400 no-underline"
            :style="{ gridColumn: 4, gridRow: 8 }"
          >
            89–103
          </a>
        </div>

        <!-- Blok f (lantanida & aktinida) -->
        <div v-if="lanthanides.length || actinides.length" class="mt-3 min-w-[920px] space-y-2">
          <div v-if="lanthanides.length" id="lantanida" class="scroll-mt-24">
            <p
              class="mb-1 text-[10px] font-bold tracking-widest text-pink-400 uppercase"
              style="padding-left: calc(18px + (100% - 18px) / 18 * 2)"
            >
              Lantanida
            </p>
            <div
              class="grid gap-1.5"
              style="grid-template-columns: 18px repeat(18, minmax(0, 1fr))"
            >
              <div
                v-for="(el, i) in lanthanides"
                :key="el.symbol"
                class="aspect-square cursor-pointer rounded-md p-1 transition-transform hover:scale-105"
                :class="tileClass(el)"
                :style="{ gridColumn: i + 4 }"
                role="listitem"
                :tabindex="0"
                @click="openElement(el)"
                @keydown.enter="openElement(el)"
              >
                <div class="text-[9px] leading-tight opacity-70">{{ el.atomic_number }}</div>
                <div class="text-center text-sm font-bold">{{ el.symbol }}</div>
                <div class="truncate text-center text-[8px] leading-tight opacity-80">
                  {{ el.name }}
                </div>
              </div>
            </div>
          </div>

          <div v-if="actinides.length" id="aktinida" class="scroll-mt-24">
            <p
              class="mb-1 text-[10px] font-bold tracking-widest text-rose-400 uppercase"
              style="padding-left: calc(18px + (100% - 18px) / 18 * 2)"
            >
              Aktinida
            </p>
            <div
              class="grid gap-1.5"
              style="grid-template-columns: 18px repeat(18, minmax(0, 1fr))"
            >
              <div
                v-for="(el, i) in actinides"
                :key="el.symbol"
                class="aspect-square cursor-pointer rounded-md p-1 transition-transform hover:scale-105"
                :class="tileClass(el)"
                :style="{ gridColumn: i + 4 }"
                role="listitem"
                :tabindex="0"
                @click="openElement(el)"
                @keydown.enter="openElement(el)"
              >
                <div class="text-[9px] leading-tight opacity-70">{{ el.atomic_number }}</div>
                <div class="text-center text-sm font-bold">{{ el.symbol }}</div>
                <div class="truncate text-center text-[8px] leading-tight opacity-80">
                  {{ el.name }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Legenda kategori -->
      <div class="mt-6 flex flex-wrap gap-x-4 gap-y-2 text-xs text-slate-400">
        <span v-for="item in legend" :key="item.slug" class="flex items-center gap-1.5">
          <span class="h-2.5 w-2.5 rounded-sm" :class="item.dot"></span>
          {{ item.label }}
          <span class="text-slate-600">({{ item.count }})</span>
        </span>
      </div>

      <!-- Ion poliatomik -->
      <div v-if="ions.length" class="mt-10">
        <h2 class="text-xl font-semibold">Ion Poliatomik</h2>
        <p class="mt-1 text-sm text-slate-400">{{ ions.length }} ion penting untuk dihafal.</p>
        <div class="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <article
            v-for="ion in ions"
            :key="ion.name"
            class="rounded-lg border border-slate-800 bg-slate-800/40 p-3"
          >
            <div class="flex items-baseline justify-between gap-2">
              <h3 class="font-medium text-slate-200">{{ ion.name }}</h3>
              <span class="font-mono text-sm text-emerald-400">{{ ion.formula }}</span>
            </div>
            <p class="mt-1 text-xs leading-relaxed text-slate-400">{{ ion.description }}</p>
          </article>
        </div>
      </div>
    </template>
  </section>
</template>
