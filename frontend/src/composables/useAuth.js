/**
 * State autentikasi global (tanpa Pinia) — token & user disimpan di localStorage
 * sehingga tetap login setelah refresh halaman.
 */
import { computed, ref } from 'vue'
import api, { getToken, getStoredUser, setStoredUser, setToken } from '../api/client.js'

const user = ref(getStoredUser())
const loading = ref(false)

export function useAuth() {
  const isLoggedIn = computed(() => !!user.value)

  async function login({ username, password }) {
    loading.value = true
    try {
      const res = await api('/api/v1/auth/login', {
        method: 'POST',
        body: { username, password },
        auth: false,
      })
      setToken(res.access_token)
      setStoredUser(res.user)
      user.value = res.user
      return res.user
    } finally {
      loading.value = false
    }
  }

  async function register({ username, email, password }) {
    loading.value = true
    try {
      await api('/api/v1/auth/register', {
        method: 'POST',
        body: { username, email, password },
        auth: false,
      })
    } finally {
      loading.value = false
    }
    // Langsung login agar user tidak perlu mengisi form dua kali.
    return login({ username, password })
  }

  async function requestPasswordReset(email) {
    loading.value = true
    try {
      return await api('/api/v1/auth/forgot-password', {
        method: 'POST', body: { email }, auth: false,
      })
    } finally {
      loading.value = false
    }
  }

  async function resetPassword({ token, password }) {
    loading.value = true
    try {
      return await api('/api/v1/auth/reset-password', {
        method: 'POST', body: { token, password }, auth: false,
      })
    } finally {
      loading.value = false
    }
  }

  function logout() {
    setToken(null)
    setStoredUser(null)
    user.value = null
  }

  /** Validasi ringan sebelum kirim ke API. */
  function validate({ username, email, password, confirm }) {
    if (username && username.trim().length < 3) return 'Username minimal 3 karakter'
    if (password && password.length < 8) return 'Password minimal 8 karakter'
    if (confirm !== undefined && password !== confirm) return 'Konfirmasi password tidak sama'
    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return 'Format email tidak valid'
    return ''
  }

  return { user, loading, isLoggedIn, login, register, requestPasswordReset, resetPassword, logout, validate }
}
