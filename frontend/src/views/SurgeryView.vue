<script setup>
import { computed, ref } from 'vue'
import { surgeryProcedures, approachStyles } from '../data/surgery.js'
import { getSurgeryScene } from '../three/surgeryPresets.js'
import SurgeryViewer from '../components/surgery/SurgeryViewer.vue'

const selectedId = ref(surgeryProcedures[0].id)
const selected = computed(() => surgeryProcedures.find((p) => p.id === selectedId.value))
const preset = computed(() => getSurgeryScene(selected.value.scene))
const activeStep = ref(0)
const showAllSteps = ref(false)

const pick = (id) => {
  selectedId.value = id
  activeStep.value = 0
  showAllSteps.value = false
}

const visibleSteps = computed(() =>
  showAllSteps.value ? selected.value.steps : selected.value.steps.slice(0, 3),
)
</script>

<template>
  <section class="mx-auto max-w-6xl px-4 py-10">
    <div class="flex flex-wrap items-end justify-between gap-4">
      <div>
        <p class="text-xs font-medium tracking-wide text-emerald-400">AnatomiMed · Ruang Operasi</p>
        <h1 class="mt-1 text-3xl font-bold">Menu Operasi</h1>
        <p class="mt-2 max-w-2xl text-slate-400">
          Pelajari prosedur bedah dari perspektif kimiawi &amp; anatomi: prinsip minimal invasif,
          peralatan, langkah operasi, dan risiko. Model 3D dapat diputar untuk melihat tata letak port dan organ.
        </p>
      </div>
      <p class="max-w-xs rounded-lg border border-amber-500/30 bg-amber-500/10 px-3 py-2 text-xs text-amber-200">
        Materi edukatif, bukan panduan klinis atau pengganti pelatihan medis.
      </p>
    </div>

    <div class="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,340px)_minmax(0,1fr)]">
      <!-- Daftar prosedur -->
      <nav aria-label="Daftar prosedur" class="flex flex-col gap-2">
        <button
          v-for="proc in surgeryProcedures"
          :key="proc.id"
          type="button"
          class="rounded-xl border p-4 text-left transition-colors focus:ring-2 focus:ring-blue-500/60 focus:outline-none"
          :class="proc.id === selectedId ? 'border-blue-500/60 bg-blue-500/10' : 'border-slate-800 bg-slate-800/40 hover:border-slate-600'"
          :aria-current="proc.id === selectedId ? 'true' : undefined"
          @click="pick(proc.id)"
        >
          <div class="flex items-start justify-between gap-2">
            <h2 class="font-semibold text-white">{{ proc.name }}</h2>
            <span class="shrink-0 text-[10px] text-slate-400">{{ proc.duration }}</span>
          </div>
          <p class="mt-1 text-sm text-slate-400">{{ proc.short }}</p>
          <span
            class="mt-2 inline-block rounded-full px-2 py-0.5 text-[10px]"
            :class="approachStyles[proc.approach] ?? 'bg-slate-700 text-slate-300'"
          >
            {{ proc.approach }}
          </span>
        </button>
      </nav>

      <!-- Detail prosedur -->
      <div class="flex flex-col gap-6">
        <div class="rounded-xl border border-slate-800 bg-slate-800/40 p-5">
          <h2 class="text-xl font-semibold text-white">{{ selected.name }}</h2>
          <p class="mt-2 text-sm text-slate-300">{{ selected.summary }}</p>
          <dl class="mt-4 grid grid-cols-2 gap-3 text-sm sm:grid-cols-4">
            <div>
              <dt class="text-xs text-slate-500">Pendekatan</dt>
              <dd class="text-slate-200">{{ selected.approach }}</dd>
            </div>
            <div>
              <dt class="text-xs text-slate-500">Durasi</dt>
              <dd class="text-slate-200">{{ selected.duration }}</dd>
            </div>
            <div>
              <dt class="text-xs text-slate-500">Anestesi</dt>
              <dd class="text-slate-200">{{ selected.anesthesia }}</dd>
            </div>
            <div>
              <dt class="text-xs text-slate-500">Rawat inap</dt>
              <dd class="text-slate-200">{{ selected.stay }}</dd>
            </div>
          </dl>
        </div>

        <!-- Visual 3D -->
        <div>
          <div class="mb-2 flex items-center justify-between">
            <h3 class="text-sm font-semibold text-slate-200">Visual 3D tata letak bedah</h3>
            <span class="text-[11px] text-slate-500">Model dibuat sendiri dengan Three.js</span>
          </div>
          <SurgeryViewer :key="selected.id" :preset="preset" />
          <p class="mt-2 text-[11px] text-slate-500">
            Skematik-realistis: dinding perut, trokar/laparoskop, instrumen, dan organ yang terlibat.
            Detail anatomi disederhanakan agar tata letak port mudah dipahami.
          </p>
        </div>

        <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
          <div class="rounded-xl border border-slate-800 bg-slate-800/40 p-5">
            <h3 class="font-semibold text-white">Tujuan operasi</h3>
            <ul class="mt-3 space-y-1.5 text-sm text-slate-300">
              <li v-for="goal in selected.goal" :key="goal" class="flex gap-2">
                <span class="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-500" aria-hidden="true" />
                <span>{{ goal }}</span>
              </li>
            </ul>
          </div>
          <div class="rounded-xl border border-slate-800 bg-slate-800/40 p-5">
            <h3 class="font-semibold text-white">Peralatan</h3>
            <ul class="mt-3 space-y-1.5 text-sm text-slate-300">
              <li v-for="tool in selected.equipment" :key="tool" class="flex gap-2">
                <span class="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-sky-500" aria-hidden="true" />
                <span>{{ tool }}</span>
              </li>
            </ul>
          </div>
        </div>

        <!-- Langkah -->
        <div class="rounded-xl border border-slate-800 bg-slate-800/40 p-5">
          <div class="flex items-center justify-between gap-3">
            <h3 class="font-semibold text-white">Langkah operasi</h3>
            <span class="text-xs text-slate-500">{{ selected.steps.length }} langkah</span>
          </div>
          <ol class="mt-4 space-y-3">
            <li
              v-for="(step, index) in visibleSteps"
              :key="step.title"
              class="flex gap-3"
              @mouseenter="activeStep = index"
            >
              <button
                type="button"
                class="flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-xs font-semibold transition-colors focus:ring-2 focus:ring-blue-500/60 focus:outline-none"
                :class="activeStep === index ? 'bg-blue-500 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'"
                :aria-label="`Langkah ${index + 1}: ${step.title}`"
                @click="activeStep = index"
              >
                {{ index + 1 }}
              </button>
              <div>
                <p class="text-sm font-medium text-slate-100">{{ step.title }}</p>
                <p class="mt-0.5 text-sm text-slate-400">{{ step.detail }}</p>
              </div>
            </li>
          </ol>
          <button
            type="button"
            class="mt-4 text-sm text-blue-400 hover:underline focus:ring-2 focus:ring-blue-500/60 focus:outline-none"
            @click="showAllSteps = !showAllSteps"
          >
            {{ showAllSteps ? 'Ringkas langkah' : `Tampilkan semua ${selected.steps.length} langkah` }}
          </button>
        </div>

        <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
          <div class="rounded-xl border border-slate-800 bg-slate-800/40 p-5">
            <h3 class="font-semibold text-white">Risiko & komplikasi</h3>
            <ul class="mt-3 space-y-1.5 text-sm text-slate-300">
              <li v-for="risk in selected.risks" :key="risk" class="flex gap-2">
                <span class="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-red-500" aria-hidden="true" />
                <span>{{ risk }}</span>
              </li>
            </ul>
          </div>
          <div class="flex flex-col gap-4 rounded-xl border border-slate-800 bg-slate-800/40 p-5">
            <div>
              <h3 class="font-semibold text-white">Pemulihan</h3>
              <p class="mt-2 text-sm text-slate-300">{{ selected.recovery }}</p>
            </div>
            <div class="border-t border-slate-700/60 pt-3">
              <h3 class="text-sm font-semibold text-slate-200">Terbuka vs minimal invasif</h3>
              <dl class="mt-2 space-y-1 text-sm">
                <div class="flex justify-between gap-3">
                  <dt class="text-slate-500">Terbuka</dt>
                  <dd class="text-right text-slate-300">{{ selected.compare.open }}</dd>
                </div>
                <div class="flex justify-between gap-3">
                  <dt class="text-slate-500">Minimal invasif</dt>
                  <dd class="text-right text-slate-300">{{ selected.compare.minimally }}</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
