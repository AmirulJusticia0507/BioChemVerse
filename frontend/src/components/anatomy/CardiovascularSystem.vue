<script setup>
import { computed, ref } from 'vue'
import { cardiovascularSystem as system } from '../../data/cardiovascularSystem.js'

const activeScenario = ref(false)
const heart = system.organs[0]
const infarction = system.pathology_scenarios[0]
const values = computed(() => Object.fromEntries(infarction.biochemical_alterations.map((item) => [item.biomarker_code, item.simulated_value])))
</script>

<template>
  <section class="mt-4 overflow-hidden rounded-xl border border-rose-500/25 bg-slate-900/70" aria-labelledby="cardio-title">
    <div class="border-b border-rose-500/20 bg-rose-500/10 px-4 py-3">
      <p class="text-xs font-medium uppercase tracking-wider text-rose-300">{{ system.system_name }} · v{{ system.version }}</p>
      <h3 id="cardio-title" class="mt-1 font-semibold text-white">{{ heart.organ_name }}</h3>
    </div>
    <div class="space-y-4 p-4 text-sm text-slate-300">
      <div>
        <p class="font-medium text-slate-100">Struktur fokus</p>
        <p class="mt-1"><strong class="text-rose-300">{{ heart.sub_structures[0].name }}</strong> — {{ heart.sub_structures[0].description }}</p>
      </div>
      <div>
        <p class="font-medium text-slate-100">Biomarker jantung</p>
        <dl class="mt-2 space-y-2">
          <div v-for="marker in heart.biochemical_parameters.biomarkers" :key="marker.code" class="flex items-start justify-between gap-3 rounded-lg bg-slate-800/70 px-3 py-2">
            <dt><span class="font-semibold text-white">{{ marker.code }}</span><br /><span class="text-xs text-slate-400">{{ marker.name }}</span></dt>
            <dd class="shrink-0 text-right text-xs"><span v-if="activeScenario" class="font-semibold text-rose-300">{{ values[marker.code] }} {{ marker.unit }}</span><span v-else>{{ marker.normal_range }}</span></dd>
          </div>
        </dl>
      </div>
      <div>
        <p class="font-medium text-slate-100">Metabolisme & farmakologi</p>
        <p class="mt-1 text-xs">{{ heart.biochemical_parameters.metabolic_pathways.join(' · ') }}</p>
        <p class="mt-2 text-xs text-slate-400">{{ heart.pharmacology_receptors[0].receptor_name }} — {{ heart.pharmacology_receptors[0].target_drug_class }}</p>
      </div>
      <button type="button" class="w-full rounded-lg border px-3 py-2 text-sm font-medium transition-colors focus:ring-2 focus:ring-rose-400/60 focus:outline-none" :class="activeScenario ? 'border-rose-400 bg-rose-500/20 text-rose-100' : 'border-slate-700 bg-slate-800 text-slate-200 hover:border-rose-400/60'" :aria-pressed="activeScenario" @click="activeScenario = !activeScenario">
        {{ activeScenario ? 'Matikan simulasi infark' : 'Simulasikan infark miokard' }}
      </button>
      <div v-if="activeScenario" class="rounded-lg border border-rose-500/30 bg-rose-950/40 p-3 text-xs text-rose-100" role="status">
        <strong>{{ infarction.disease_name }} ({{ infarction.disease_code_icd10 }})</strong>
        <p class="mt-1">Simulasi: denyut {{ infarction.visual_effects.pulse_rate_bpm }} bpm · {{ infarction.visual_effects.arrhythmia_pattern }}. Nilai biomarker ini untuk edukasi, bukan diagnosis.</p>
      </div>
    </div>
  </section>
</template>
