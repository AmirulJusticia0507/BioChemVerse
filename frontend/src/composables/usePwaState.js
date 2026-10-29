/**
 * State PWA bersama: status offline dan kesiapan update service worker.
 * Dipakai App.vue (banner) dan composable instalasi di usePwa.js.
 */
import { ref } from 'vue'

// Lapisan "pakai versi baru" (dari virtual:pwa-register).
export const applyUpdate = ref(null)
export const updateReady = ref(false)

// Aplikasi sedang berjalan tanpa koneksi (dilayani dari cache service worker).
export const offline = ref(typeof navigator === 'object' && !navigator.onLine)

export function bindOnlineStatus() {
  const on = () => (offline.value = false)
  const off = () => (offline.value = true)
  window.addEventListener('online', on)
  window.addEventListener('offline', off)
  return () => {
    window.removeEventListener('online', on)
    window.removeEventListener('offline', off)
  }
}
