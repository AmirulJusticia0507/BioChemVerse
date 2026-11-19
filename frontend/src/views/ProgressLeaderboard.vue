<script setup>
import { computed, onMounted, ref, watch } from 'vue'

// Data statis untuk demo: peringkat per modul
// Di production, ini akan diambil dari API/localStorage
const mockLeaderboard = [
  { id: 1, name: 'Ani K', score: 98, module: 'Anatomi', date: 'Kemarin' },
  { id: 2, name: 'Budi S', score: 95, module: 'Anatomi', date: '2 hari yang lalu' },
  { id: 3, name: 'Siti R', score: 92, module: 'Anatomi', date: '3 hari yang lalu' },
  { id: 4, name: 'Raka W', score: 88, module: 'Kimia', date: '4 hari yang lalu' },
  { id: 5, name: 'Dewi L', score: 85, module: 'Kimia', date: '5 hari yang lalu' },
]

// Progress per user (disimpan di localStorage)
const userProgress = ref(JSON.parse(localStorage.getItem('bcv-user-progress') || '{}'))

watch(userProgress, (newVal) => {
  localStorage.setItem('bcv-user-progress', JSON.stringify(newVal))
}, { deep: true })

// Menghitung total progress persentase
const totalModules = computed(() => 5) // jumlah modul yang ada
const completedModules = computed(() => {
  let count = 0
  for (const key of Object.keys(userProgress.value)) {
    if (userProgress.value[key].completed) count++
  }
  return count
})

const overallProgress = computed(() =>
  totalModules.value > 0 ? Math.round((completedModules.value / totalModules.value) * 100) : 0
)

// Fungsi bantuan
function getProgress(mod) {
  const prog = userProgress.value[mod.toLowerCase()]
  return prog ? (prog.completed ? 100 : Math.round(prog.progress * 100)) : 0
}

function getCompletion(mod) {
  const prog = userProgress.value[mod.toLowerCase()]
  if (!prog) return 0
  if (prog.completed) return 100
  return Math.round(prog.progress * 100)
}

function scoreColor(score) {
  if (score >= 90) return 'text-emerald-400'
  if (score >= 75) return 'text-amber-400'
  return 'text-red-400'
}

// Komputed style untuk menghindari parsing % di :style
const progressStyles = computed(() => {
  const styles = {}
  ;['Anatomi', 'Kimia', 'Forensik', 'Kuis', 'Biochim'].forEach((mod, i) => {
    const modKey = mod.toLowerCase()
    const prog = userProgress.value[modKey]
    if (prog) {
      styles[mod] = { width: prog.completed ? '100%' : Math.round(prog.progress * 100) + '%' }
    } else {
      styles[mod] = { width: '0%' }
    }
  })
  return styles
})
</script>

<template>
<div class="space-y-4">
  <!-- Card Progress Saya -->
  <div class="rounded-lg border border-slate-800 bg-slate-800/40 p-4">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-sm font-medium text-white">Progress Saya</h3>
      <span class="text-xs text-slate-400">{{ overallProgress }}% selesai</span>
    </div>

    <div class="mt-2">
      <div v-for="(mod, index) in ['Anatomi', 'Kimia', 'Forensik', 'Kuis', 'Biochim']" :key="index" class="flex items-center gap-2 py-1">
        <span class="text-xs text-slate-400 w-24">{{ mod }}</span>
        <div class="flex-1 h-1 rounded-full bg-slate-700">
          <div
            class="h-1 rounded-full bg-blue-500 transition-width"
            :style="progressStyles[mod]"
          ></div>
        </div>
        <span class="text-xs text-slate-500">{{ getCompletion(mod) }}% </span>
      </div>
    </div>
  </div>

  <!-- Leaderboard Umum -->
  <div class="rounded-lg border border-slate-800 bg-slate-800/40 p-4">
    <h3 class="text-sm font-medium text-white">Peringkat Teratas</h3>
    <p class="text-xs text-slate-400 mt-1">10 pengguna terbaik</p>
    <table class="mt-2 w-full text-left text-xs">
      <thead>
        <tr class="border-b border-slate-700 text-xs text-slate-400">
          <th class="py-2">#</th>
          <th class="py-2">Nama</th>
          <th class="py-2 text-right">Skor</th>
          <th class="py-2 text-right">Modul</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, i) in mockLeaderboard" :key="user.id">
          <td class="py-2 text-slate-300">{{ i + 1 }}</td>
          <td class="py-2 text-slate-300">{{ user.name }}</td>
          <td class="py-2 text-right font-semibold" :class="scoreColor(user.score)">
            {{ user.score }}
          </td>
          <td class="py-2 text-right text-slate-300">{{ user.module }}</td>
        </tr>
        </tbody>
      </table>
      <p class="mt-2 text-xs text-slate-500">* Data berdasarkan sesi aktif.</p>
  </div>
</div>
</template>