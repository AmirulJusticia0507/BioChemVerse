<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { api } from '../api/client.js'
import { useAuth } from '../composables/useAuth.js'

const { isLoggedIn, logout } = useAuth()

const TOPICS = [
  { id: 'campuran', label: 'Campuran', hint: 'Semua jenis soal' },
  { id: 'simbol', label: 'Simbol', hint: 'Nama unsur → simbol' },
  { id: 'nomor-atom', label: 'Nomor atom', hint: 'Simbol → nomor atom' },
  { id: 'kategori', label: 'Kategori', hint: 'Golongan unsur' },
  { id: 'golongan-periode', label: 'Golongan & periode', hint: 'Posisi di tabel' },
]

const topic = ref('campuran')
const count = ref(10)
const COUNT_OPTIONS = [5, 10, 15, 20]

const phase = ref('idle') // idle | playing | result
const starting = ref(false)
const submitting = ref(false)
const error = ref('')

const quiz = ref(null) // { quiz_id, topic, questions }
const answers = ref([]) // index -> pilihan (string) atau ''
const current = ref(0)
const result = ref(null) // respons /quiz/submit
const elapsed = ref(0)

const attempts = ref([])
const attemptsLoading = ref(false)

let timerId = null

const total = computed(() => quiz.value?.questions.length ?? 0)
const answeredCount = computed(() => answers.value.filter(Boolean).length)
const question = computed(() => quiz.value?.questions[current.value] ?? null)
const allAnswered = computed(() => total.value > 0 && answeredCount.value === total.value)
const progressPct = computed(() =>
  total.value ? Math.round((answeredCount.value / total.value) * 100) : 0,
)
const resultMap = computed(() =>
  Object.fromEntries((result.value?.results ?? []).map((row) => [row.index, row])),
)

function clock(seconds) {
  const m = String(Math.floor(seconds / 60)).padStart(2, '0')
  const s = String(seconds % 60).padStart(2, '0')
  return `${m}:${s}`
}

function stopTimer() {
  if (timerId) {
    clearInterval(timerId)
    timerId = null
  }
}

function startTimer() {
  stopTimer()
  elapsed.value = 0
  timerId = setInterval(() => {
    elapsed.value += 1
  }, 1000)
}

function resetLocal() {
  quiz.value = null
  answers.value = []
  current.value = 0
  result.value = null
  error.value = ''
  phase.value = 'idle'
  stopTimer()
}

function handleAuthError(e) {
  if (e.status === 401) {
    logout()
    error.value = 'Sesi berakhir — silakan masuk kembali.'
    return true
  }
  return false
}

async function startQuiz() {
  starting.value = true
  error.value = ''
  result.value = null
  try {
    const res = await api('/api/v1/quiz/start', {
      method: 'POST',
      body: { topic: topic.value, count: Number(count.value) },
    })
    quiz.value = res
    answers.value = Array.from({ length: res.questions.length }, () => '')
    current.value = 0
    phase.value = 'playing'
    startTimer()
  } catch (e) {
    if (!handleAuthError(e)) error.value = e.message
  } finally {
    starting.value = false
  }
}

function choose(option) {
  if (phase.value !== 'playing') return
  answers.value = answers.value.map((value, index) =>
    index === current.value ? option : value,
  )
}

function go(index) {
  if (index < 0 || index >= total.value) return
  current.value = index
}

function next() {
  if (current.value < total.value - 1) current.value += 1
}

function prev() {
  if (current.value > 0) current.value -= 1
}

async function submit() {
  if (!quiz.value || submitting.value) return
  submitting.value = true
  error.value = ''
  try {
    result.value = await api('/api/v1/quiz/submit', {
      method: 'POST',
      body: {
        quiz_id: quiz.value.quiz_id,
        // Jawaban kosong dikirim sebagai '' agar jumlahnya tetap sesuai soal.
        answers: answers.value.map((value) => value ?? ''),
        duration_sec: elapsed.value,
      },
    })
    stopTimer()
    phase.value = 'result'
    current.value = 0
    loadAttempts()
  } catch (e) {
    if (!handleAuthError(e)) error.value = e.message
  } finally {
    submitting.value = false
  }
}

async function loadAttempts() {
  if (!isLoggedIn.value) {
    attempts.value = []
    return
  }
  attemptsLoading.value = true
  try {
    const res = await api('/api/v1/quiz/attempts?limit=10')
    attempts.value = res.data
  } catch (e) {
    if (!handleAuthError(e)) error.value = e.message
  } finally {
    attemptsLoading.value = false
  }
}

function attemptDate(value) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'
  return date.toLocaleString('id-ID', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function topicLabel(id) {
  return TOPICS.find((item) => item.id === id)?.label ?? id
}

function scoreColor(score) {
  if (score >= 80) return 'text-emerald-400'
  if (score >= 50) return 'text-amber-400'
  return 'text-red-400'
}

onMounted(loadAttempts)
onBeforeUnmount(stopTimer)
</script>

<template>
  <section class="mx-auto max-w-4xl px-4 py-10">
    <div class="flex flex-wrap items-end justify-between gap-3">
      <div>
        <h1 class="text-3xl font-bold">Kuis Tabel Periodik</h1>
        <p class="mt-2 text-slate-400">
          Soal dibuat langsung oleh server dari 118 unsur — skor dan riwayat tersimpan di akunmu.
        </p>
      </div>
      <p v-if="isLoggedIn" class="text-xs text-slate-500">Riwayat 10 percobaan terakhir dimuat otomatis.</p>
    </div>

    <!-- Wajib login -->
    <div
      v-if="!isLoggedIn"
      class="mt-8 rounded-xl border border-slate-800 bg-slate-800/40 p-6 text-center"
    >
      <p class="text-slate-300">Kuis membutuhkan akun agar skor bisa disimpan.</p>
      <div class="mt-4 flex justify-center gap-2">
        <RouterLink
          to="/login?next=/kuis"
          class="rounded-lg bg-blue-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-600"
        >
          Masuk
        </RouterLink>
        <RouterLink
          to="/register"
          class="rounded-lg border border-slate-600 px-4 py-2 text-sm text-slate-200 transition-colors hover:border-slate-500 hover:bg-slate-800"
        >
          Daftar
        </RouterLink>
      </div>
    </div>

    <template v-else>
      <p
        v-if="error"
        class="mt-6 rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-300"
      >
        {{ error }}
      </p>

      <!-- Pengaturan -->
      <div v-if="phase === 'idle'" class="mt-8 rounded-xl border border-slate-800 bg-slate-800/40 p-6">
        <h2 class="text-lg font-semibold">Mulai kuis baru</h2>

        <fieldset class="mt-4">
          <legend class="mb-2 text-xs text-slate-400">Topik</legend>
          <div class="grid gap-2 sm:grid-cols-2">
            <button
              v-for="item in TOPICS"
              :key="item.id"
              type="button"
              class="rounded-lg border px-3 py-2 text-left text-sm transition-colors"
              :class="
                topic === item.id
                  ? 'border-blue-500 bg-blue-500/20 text-white'
                  : 'border-slate-700 bg-slate-900/40 text-slate-300 hover:border-slate-500'
              "
              :aria-pressed="topic === item.id"
              @click="topic = item.id"
            >
              <span class="font-medium">{{ item.label }}</span>
              <span class="block text-xs text-slate-500">{{ item.hint }}</span>
            </button>
          </div>
        </fieldset>

        <fieldset class="mt-5">
          <legend class="mb-2 text-xs text-slate-400">Jumlah soal</legend>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="n in COUNT_OPTIONS"
              :key="n"
              type="button"
              class="rounded-lg border px-4 py-1.5 text-sm transition-colors"
              :class="
                count === n
                  ? 'border-blue-500 bg-blue-500/20 text-white'
                  : 'border-slate-700 text-slate-300 hover:border-slate-500'
              "
              :aria-pressed="count === n"
              @click="count = n"
            >
              {{ n }} soal
            </button>
          </div>
        </fieldset>

        <button
          type="button"
          class="mt-6 w-full rounded-lg bg-blue-500 px-4 py-2.5 font-medium text-white transition-colors hover:bg-blue-600 disabled:opacity-50 sm:w-auto sm:px-8"
          :disabled="starting"
          @click="startQuiz"
        >
          {{ starting ? 'Menyiapkan soal…' : 'Mulai kuis' }}
        </button>
      </div>

      <!-- Pengerjaan -->
      <div v-else-if="phase === 'playing' && question" class="mt-8">
        <div class="flex flex-wrap items-center justify-between gap-2 text-sm">
          <p class="text-slate-400">
            Soal <span class="font-semibold text-slate-200">{{ current + 1 }}</span> /
            {{ total }}
            <span class="ml-2 text-xs text-slate-500">{{ answeredCount }} terjawab</span>
          </p>
          <p class="font-mono text-slate-300">{{ clock(elapsed) }}</p>
        </div>
        <div class="mt-2 h-2 overflow-hidden rounded-full bg-slate-700">
          <div
            class="h-full rounded-full bg-blue-500 transition-all duration-300"
            :style="{ width: `${progressPct}%` }"
          ></div>
        </div>

        <div class="mt-5 rounded-xl border border-slate-800 bg-slate-800/40 p-6">
          <p class="text-lg font-medium text-slate-100">{{ question.question }}</p>

          <div class="mt-4 grid gap-2 sm:grid-cols-2">
            <button
              v-for="(option, index) in question.options"
              :key="option"
              type="button"
              class="rounded-lg border px-4 py-3 text-left text-sm transition-colors"
              :class="
                answers[current] === option
                  ? 'border-blue-500 bg-blue-500/20 text-white'
                  : 'border-slate-700 text-slate-300 hover:border-slate-500 hover:bg-slate-900/40'
              "
              :aria-pressed="answers[current] === option"
              :data-option="index"
              @click="choose(option)"
            >
              {{ option }}
            </button>
          </div>
        </div>

        <div class="mt-4 flex flex-wrap items-center gap-2">
          <button
            type="button"
            class="rounded-lg border border-slate-600 px-3 py-2 text-sm text-slate-200 transition-colors hover:border-slate-500 hover:bg-slate-800 disabled:opacity-40"
            :disabled="current === 0"
            @click="prev"
          >
            ← Sebelumnya
          </button>
          <button
            type="button"
            class="rounded-lg border border-slate-600 px-3 py-2 text-sm text-slate-200 transition-colors hover:border-slate-500 hover:bg-slate-800 disabled:opacity-40"
            :disabled="current === total - 1"
            @click="next"
          >
            Berikutnya →
          </button>
          <span class="flex-1"></span>
          <button
            type="button"
            class="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-emerald-600 disabled:opacity-50"
            :disabled="submitting"
            @click="submit"
          >
            {{ submitting ? 'Menilai…' : `Selesai & nilai (${answeredCount}/${total})` }}
          </button>
        </div>
        <p v-if="!allAnswered" class="mt-2 text-xs text-slate-500">
          Jawaban kosong dinilai salah — kamu boleh mengirim sekarang atau melengkapi dulu.
        </p>
      </div>

      <!-- Hasil -->
      <div v-else-if="phase === 'result' && result" class="mt-8">
        <div class="rounded-xl border border-slate-800 bg-slate-800/40 p-6 text-center">
          <p class="text-sm text-slate-400">Topik {{ topicLabel(result.topic) }}</p>
          <p class="mt-2 text-5xl font-bold" :class="scoreColor(result.score)">{{ result.score }}</p>
          <p class="mt-1 text-sm text-slate-400">
            {{ result.correct }} benar dari {{ result.total }} soal · {{ clock(elapsed) }}
          </p>
          <div class="mt-5 flex flex-wrap justify-center gap-2">
            <button
              type="button"
              class="rounded-lg bg-blue-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-600"
              @click="resetLocal"
            >
              Kuis lagi
            </button>
          </div>
        </div>

        <h2 class="mt-8 text-lg font-semibold">Pembahasan</h2>
        <ol class="mt-3 space-y-2">
          <li
            v-for="(item, index) in quiz.questions"
            :key="item.id"
            class="rounded-lg border px-4 py-3 text-sm"
            :class="
              resultMap[index]?.is_correct
                ? 'border-emerald-500/40 bg-emerald-500/5'
                : 'border-red-500/40 bg-red-500/5'
            "
          >
            <p class="font-medium text-slate-200">
              {{ index + 1 }}. {{ item.question }}
            </p>
            <p class="mt-1 text-xs text-slate-400">
              Jawabanmu:
              <span :class="resultMap[index]?.is_correct ? 'text-emerald-400' : 'text-red-400'">
                {{ resultMap[index]?.given || '(kosong)' }}
              </span>
              <template v-if="!resultMap[index]?.is_correct">
                · Benar: <span class="text-emerald-400">{{ resultMap[index]?.correct }}</span>
              </template>
            </p>
          </li>
        </ol>
      </div>

      <!-- Riwayat -->
      <div class="mt-10 rounded-xl border border-slate-800 bg-slate-800/40 p-6">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold">Riwayat percobaan</h2>
          <button
            type="button"
            class="text-xs text-slate-400 transition-colors hover:text-slate-200"
            :disabled="attemptsLoading"
            @click="loadAttempts"
          >
            {{ attemptsLoading ? 'Memuat…' : 'Muat ulang' }}
          </button>
        </div>

        <p v-if="!attempts.length && !attemptsLoading" class="mt-3 text-sm text-slate-500">
          Belum ada percobaan. Selesaikan satu kuis untuk mengisi riwayat.
        </p>

        <table v-else class="mt-3 w-full text-left text-sm">
          <thead>
            <tr class="border-b border-slate-700 text-xs text-slate-400">
              <th class="py-2">Waktu</th>
              <th class="py-2">Topik</th>
              <th class="py-2 text-right">Benar</th>
              <th class="py-2 text-right">Skor</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in attempts" :key="row.id" class="border-b border-slate-800 last:border-0">
              <td class="py-2 text-slate-300">{{ attemptDate(row.created_at) }}</td>
              <td class="py-2 text-slate-300">{{ topicLabel(row.topic) }}</td>
              <td class="py-2 text-right text-slate-300">{{ row.correct }}/{{ row.total }}</td>
              <td class="py-2 text-right font-semibold" :class="scoreColor(row.score)">
                {{ row.score }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </section>
</template>
