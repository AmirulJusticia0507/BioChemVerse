<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth.js'

const { login, loading, validate } = useAuth()
const route = useRoute()
const router = useRouter()

const username = ref('')
const password = ref('')
const showPassword = ref(false)
const error = ref('')

async function submit() {
  error.value = validate({ password: password.value }) // cek panjang password
  if (error.value) return
  try {
    await login({ username: username.value.trim(), password: password.value })
    const next = typeof route.query.next === 'string' ? route.query.next : '/'
    router.push(next)
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <section class="mx-auto max-w-md px-4 py-16">
    <h1 class="text-2xl font-bold">Masuk</h1>
    <p class="mt-1 text-sm text-slate-400">Belum punya akun? <RouterLink to="/register" class="text-blue-400 hover:underline">Daftar</RouterLink></p>

    <form class="mt-6 space-y-4 rounded-xl border border-slate-800 bg-slate-800/40 p-6" @submit.prevent="submit">
      <p v-if="error" class="rounded-lg border border-red-500/40 bg-red-500/10 px-3 py-2 text-sm text-red-300">
        {{ error }}
      </p>

      <div>
        <label for="login-username" class="mb-1 block text-sm text-slate-300">Username</label>
        <input
          id="login-username"
          v-model="username"
          type="text"
          autocomplete="username"
          required
          placeholder="student1"
          class="w-full rounded-lg border border-slate-600 bg-slate-900 px-3 py-2 text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
        />
      </div>

      <div class="text-right text-sm">
        <RouterLink to="/forgot-password" class="text-blue-400 hover:underline">Lupa kata sandi?</RouterLink>
      </div>

      <div>
        <div class="mb-1 flex items-center justify-between"><label for="login-password" class="text-sm text-slate-300">Password</label><button type="button" class="rounded p-1 text-slate-400 hover:text-slate-200 focus:ring-2 focus:ring-blue-500/60 focus:outline-none" :aria-label="showPassword ? 'Sembunyikan password' : 'Tampilkan password'" @click="showPassword = !showPassword"><svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path v-if="showPassword" d="m3 3 18 18M10.6 10.6a2 2 0 0 0 2.8 2.8M2.3 10.1a1.7 1.7 0 0 0 0 1.8C3.2 13.3 6.7 18 12 18c1 0 2-.2 2.9-.5M9.9 4.2A10.9 10.9 0 0 1 12 4c5.3 0 8.8 4.7 9.7 6.1a1.7 1.7 0 0 1 0 1.8 18.2 18.2 0 0 1-3.1 3.6" /><path v-else d="M2.3 10.1a1.7 1.7 0 0 0 0 1.8C3.2 13.3 6.7 18 12 18s8.8-4.7 9.7-6.1a1.7 1.7 0 0 0 0-1.8C20.8 9.7 17.3 5 12 5S3.2 9.7 2.3 10.1Z" /><circle v-if="!showPassword" cx="12" cy="11" r="3" /></svg></button></div>
        <input
          id="login-password"
          v-model="password"
          :type="showPassword ? 'text' : 'password'"
          autocomplete="current-password"
          required
          placeholder="••••••••"
          class="w-full rounded-lg border border-slate-600 bg-slate-900 px-3 py-2 text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
        />
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full rounded-lg bg-blue-500 px-4 py-2 font-medium text-white transition-colors hover:bg-blue-600 focus:ring-2 focus:ring-blue-500/50 focus:outline-none disabled:opacity-60"
      >
        {{ loading ? 'Memproses…' : 'Masuk' }}
      </button>
    </form>
  </section>
</template>
