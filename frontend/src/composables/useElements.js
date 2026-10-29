/**
 * Daftar seluruh unsur (118) — dimuat sekali lalu dipakai bersama
 * oleh halaman Bandingkan, Belajar, dan Kalkulator.
 */
import { onMounted, ref } from 'vue'
import { api } from '../api/client.js'

const elements = ref([])
const loading = ref(false)
const error = ref('')
let pending = null

export function useElements() {
  async function load() {
    if (elements.value.length) return
    if (pending) return pending
    loading.value = true
    error.value = ''
    pending = api('/api/v1/elements', { auth: false })
      .then((res) => {
        elements.value = res.data
      })
      .catch((e) => {
        error.value = e.message
      })
      .finally(() => {
        loading.value = false
        pending = null
      })
    return pending
  }

  onMounted(load)

  return { elements, loading, error, reload: load }
}
