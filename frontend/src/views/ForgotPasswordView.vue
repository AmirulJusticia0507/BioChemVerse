<script setup>
import { ref } from 'vue'
import { useAuth } from '../composables/useAuth.js'

const { loading, requestPasswordReset, validate } = useAuth()
const email = ref('')
const error = ref('')
const sent = ref(false)

async function submit() {
  error.value = validate({ email: email.value })
  if (error.value) return
  try {
    await requestPasswordReset(email.value.trim().toLowerCase())
    sent.value = true
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <section class="mx-auto max-w-md px-4 py-16">
    <h1 class="text-2xl font-bold">Lupa kata sandi</h1>
    <p class="mt-1 text-sm text-slate-400">Masukkan email akunmu. Kami akan mengirim tautan untuk membuat kata sandi baru.</p>

    <div v-if="sent" class="mt-6 rounded-xl border border-emerald-500/40 bg-emerald-500/10 p-6 text-sm text-emerald-200">
      Jika email tersebut terdaftar, tautan pengaturan ulang sudah dikirim. Periksa inbox dan folder spam.
      <RouterLink to="/login" class="mt-4 block font-medium text-blue-300 hover:underline">Kembali ke halaman masuk</RouterLink>
    </div>
    <form v-else class="mt-6 space-y-4 rounded-xl border border-slate-800 bg-slate-800/40 p-6" @submit.prevent="submit">
      <p v-if="error" class="rounded-lg border border-red-500/40 bg-red-500/10 px-3 py-2 text-sm text-red-300">{{ error }}</p>
      <div>
        <label for="reset-email" class="mb-1 block text-sm text-slate-300">Email</label>
        <input id="reset-email" v-model="email" type="email" autocomplete="email" required placeholder="siswa@contoh.com" class="w-full rounded-lg border border-slate-600 bg-slate-900 px-3 py-2 text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40 focus:outline-none" />
      </div>
      <button type="submit" :disabled="loading" class="w-full rounded-lg bg-blue-500 px-4 py-2 font-medium text-white transition-colors hover:bg-blue-600 disabled:opacity-60">{{ loading ? 'Mengirim…' : 'Kirim tautan reset' }}</button>
    </form>
  </section>
</template>
