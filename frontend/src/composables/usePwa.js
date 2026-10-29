/**
 * Penangkap event `beforeinstallprompt` (disimpan modul-level agar bertahan
 * walau komponen di-mount ulang).
 */
import { computed, ref } from 'vue'

// Disimpan di konstanta: mencegah minifier menulis ulang literal nama global
// `window` di dalam string (bisa mengubah nama event menjadi tidak valid).
const INSTALL_EVENT = 'beforeinstallprompt'

const deferredPrompt = ref(null)
const installed = ref(false)
const promptFn = ref(null)

const isStandalone = () =>
  window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true

const isIos = () => /iphone|ipad|ipod/i.test(window.navigator.userAgent)

window.addEventListener(INSTALL_EVENT, (event) => {
  // Cegah mini-infobar bawaan; tombol disediakan aplikasi.
  event.preventDefault()
  if (typeof event.prompt !== 'function') return
  promptFn.value = event.prompt.bind(event)
  deferredPrompt.value = { userChoice: event.userChoice }
})

window.addEventListener('appinstalled', () => {
  installed.value = true
  deferredPrompt.value = null
  promptFn.value = null
})

export function usePwa() {
  const standalone = ref(isStandalone())
  if (standalone.value) installed.value = true

  // true bila peramban siap memasang aplikasi (Chromium & sebagian Android).
  const canPrompt = computed(() => !standalone.value && !!promptFn.value)
  const showIosHint = computed(() => !standalone.value && isIos() && !promptFn.value)

  async function promptInstall() {
    if (!promptFn.value) return false
    const invoke = promptFn.value
    const choice = deferredPrompt.value?.userChoice
    // prompt() harus dipanggil dalam alur klik, sebelum await.
    try {
      invoke()
    } catch {
      return false
    }
    promptFn.value = null
    deferredPrompt.value = null
    try {
      const { outcome } = (await choice) ?? {}
      if (outcome === 'accepted') installed.value = true
      return outcome === 'accepted'
    } catch {
      return false
    }
  }

  return { installed, canPrompt, showIosHint, standalone, promptInstall }
}
