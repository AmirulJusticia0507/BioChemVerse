<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth.js'

const { register, loading, validate } = useAuth()
const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const confirm = ref('')
const showPassword = ref(false)
const showConfirm = ref(false)
const error = ref('')

async function submit() {
  error.value = validate({
    username: username.value,
    email: email.value,
    password: password.value,
    confirm: confirm.value,
  })
  if (error.value) return
  try {
    await register({
      username: username.value.trim(),
      email: email.value.trim(),
      password: password.value,
    })
    router.push('/')
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <section class="mx-auto max-w-md px-4 py-16">
    <h1 class="text-2xl font-bold">Daftar Akun</h1>
    <p class="mt-1 text-sm text-slate-400">
      Sudah punya akun? <RouterLink to="/login" class="text-blue-400 hover:underline">Masuk</RouterLink>
    </p>

    <form class="mt-6 space-y-4 rounded-xl border border-slate-800 bg-slate-800/40 p-6" @submit.prevent="submit">
      <p v-if="error" class="rounded-lg border border-red-500/40 bg-red-500/10 px-3 py-2 text-sm text-red-300">
        {{ error }}
      </p>

      <div>
        <label for="reg-username" class="mb-1 block text-sm text-slate-300">Username</label>
        <input
          id="reg-username"
          v-model="username"
          type="text"
          autocomplete="username"
          required
          minlength="3"
          placeholder="student1"
          class="w-full rounded-lg border border-slate-600 bg-slate-900 px-3 py-2 text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
        />
      </div>

      <div>
        <label for="reg-email" class="mb-1 block text-sm text-slate-300">Email</label>
        <input
          id="reg-email"
          v-model="email"
          type="email"
          autocomplete="email"
          required
          placeholder="siswa@contoh.com"
          class="w-full rounded-lg border border-slate-600 bg-slate-900 px-3 py-2 text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
        />
      </div>

      <div>
        <div class="mb-1 flex items-center justify-between"><label for="reg-password" class="text-sm text-slate-300">Password</label><button type="button" class="rounded p-1 text-slate-400 hover:text-slate-200 focus:ring-2 focus:ring-blue-500/60 focus:outline-none" :aria-label="showPassword ? 'Sembunyikan password' : 'Tampilkan password'" @click="showPassword = !showPassword" aria-hidden="false">👁</button></div>
        <input
          id="reg-password"
          v-model="password"
          :type="showPassword ? 'text' : 'password'"
          autocomplete="new-password"
          required
          minlength="8"
          placeholder="minimal 8 karakter"
          class="w-full rounded-lg border border-slate-600 bg-slate-900 px-3 py-2 text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
        />
      </div>

      <div>
        <div class="mb-1 flex items-center justify-between"><label for="reg-confirm" class="text-sm text-slate-300">Ulangi Password</label><button type="button" class="rounded p-1 text-slate-400 hover:text-slate-200 focus:ring-2 focus:ring-blue-500/60 focus:outline-none" :aria-label="showConfirm ? 'Sembunyikan konfirmasi password' : 'Tampilkan konfirmasi password'" @click="showConfirm = !showConfirm">👁</button></div>
        <input
          id="reg-confirm"
          v-model="confirm"
          :type="showConfirm ? 'text' : 'password'"
          autocomplete="new-password"
          required
          placeholder="ketik ulang password"
          class="w-full rounded-lg border border-slate-600 bg-slate-900 px-3 py-2 text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none"
        />
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full rounded-lg bg-blue-500 px-4 py-2 font-medium text-white transition-colors hover:bg-blue-600 focus:ring-2 focus:ring-blue-500/50 focus:outline-none disabled:opacity-60"
      >
        {{ loading ? 'Memproses…' : 'Daftar & Masuk' }}
      </button>
    </form>
  </section>
</template>
