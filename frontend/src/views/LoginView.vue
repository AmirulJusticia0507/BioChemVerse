<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth.js'

const { login, loading, validate } = useAuth()
const route = useRoute()
const router = useRouter()

const username = ref('')
const password = ref('')
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

      <div>
        <label for="login-password" class="mb-1 block text-sm text-slate-300">Password</label>
        <input
          id="login-password"
          v-model="password"
          type="password"
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
