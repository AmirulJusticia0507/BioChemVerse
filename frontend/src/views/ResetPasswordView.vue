<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth.js'

const route = useRoute()
const router = useRouter()
const { loading, resetPassword, validate } = useAuth()
const password = ref('')
const confirm = ref('')
const error = ref('')

async function submit() {
  const token = typeof route.query.token === 'string' ? route.query.token : ''
  error.value = token ? validate({ password: password.value, confirm: confirm.value }) : 'Tautan reset tidak valid.'
  if (error.value) return
  try {
    await resetPassword({ token, password: password.value })
    router.replace('/login')
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <section class="mx-auto max-w-md px-4 py-16">
    <h1 class="text-2xl font-bold">Atur ulang kata sandi</h1>
    <p class="mt-1 text-sm text-slate-400">Buat kata sandi baru untuk akunmu.</p>
    <form class="mt-6 space-y-4 rounded-xl border border-slate-800 bg-slate-800/40 p-6" @submit.prevent="submit">
      <p v-if="error" class="rounded-lg border border-red-500/40 bg-red-500/10 px-3 py-2 text-sm text-red-300">{{ error }}</p>
      <div>
        <label for="new-password" class="mb-1 block text-sm text-slate-300">Kata sandi baru</label>
        <input id="new-password" v-model="password" type="password" autocomplete="new-password" minlength="8" required class="w-full rounded-lg border border-slate-600 bg-slate-900 px-3 py-2 text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none" />
      </div>
      <div>
        <label for="confirm-password" class="mb-1 block text-sm text-slate-300">Ulangi kata sandi baru</label>
        <input id="confirm-password" v-model="confirm" type="password" autocomplete="new-password" minlength="8" required class="w-full rounded-lg border border-slate-600 bg-slate-900 px-3 py-2 text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none" />
      </div>
      <button type="submit" :disabled="loading" class="w-full rounded-lg bg-blue-500 px-4 py-2 font-medium text-white transition-colors hover:bg-blue-600 disabled:opacity-60">{{ loading ? 'Menyimpan…' : 'Simpan kata sandi baru' }}</button>
    </form>
  </section>
</template>
