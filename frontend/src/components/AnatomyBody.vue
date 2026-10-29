<template>
  <div class="flex flex-col items-center">
    <svg viewBox="0 0 220 420" class="w-72 h-auto" fill="none" stroke="currentColor" stroke-width="2">
      <g v-for="part in parts" :key="part.id" :class="part.id" @click="select(part.id)">
        <component :is="part.shape" v-bind="part.props" :class="selected===part.id?'fill-blue-500/40':'fill-transparent'" />
      </g>
    </svg>
    <p class="mt-4 text-slate-300">{{ selected ? `Dipilih: ${selected}` : 'Klik bagian tubuh' }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const selected = ref(null)
const select = (id) => (selected.value = id)
const parts = [
  { id: 'head', shape: 'circle', props: { cx: 110, cy: 40, r: 30 } },
  { id: 'torso', shape: 'rect', props: { x: 80, y: 75, width: 60, height: 110, rx: 10 } },
  { id: 'leftArm', shape: 'line', props: { x1: 80, y1: 90, x2: 40, y2: 170 } },
  { id: 'rightArm', shape: 'line', props: { x1: 140, y1: 90, x2: 180, y2: 170 } },
  { id: 'leftLeg', shape: 'line', props: { x1: 95, y1: 185, x2: 80, y2: 300 } },
  { id: 'rightLeg', shape: 'line', props: { x1: 125, y1: 185, x2: 140, y2: 300 } },
]
</script>