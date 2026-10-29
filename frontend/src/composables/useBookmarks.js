/**
 * State bookmark global (tanpa Pinia) — dipakai halaman detail unsur dan
 * halaman Bookmark agar status simpan/hapus selalu sinkron.
 *
 * Semua panggilan butuh login; composable ini tidak memaksa redirect sendiri.
 */
import { computed, ref } from 'vue'
import { api } from '../api/client.js'

const items = ref([]) // daftar BookmarkOut (terbaru dulu)
const loading = ref(false)
const busy = ref(new Set()) // nomor atom yang sedang diproses
const error = ref('')
let loaded = false
let pending = null

const numbers = computed(() => new Set(items.value.map((row) => row.atomic_number)))

async function load(force = false) {
  if (loaded && !force) return items.value
  if (pending) return pending
  loading.value = true
  error.value = ''
  pending = api('/api/v1/bookmarks')
    .then((res) => {
      items.value = res.data
      loaded = true
      return items.value
    })
    .catch((e) => {
      error.value = e.message
      // 401 → biarkan pemanggil menangani (mis. logout)
      throw e
    })
    .finally(() => {
      loading.value = false
      pending = null
    })
  return pending
}

function isBookmarked(atomicNumber) {
  return numbers.value.has(atomicNumber)
}

function markBusy(atomicNumber, state) {
  const next = new Set(busy.value)
  if (state) next.add(atomicNumber)
  else next.delete(atomicNumber)
  busy.value = next
}

/** Tambah bila belum, hapus bila sudah. Mengembalikan status baru. */
async function toggle(element) {
  const { atomic_number: atomicNumber } = element
  if (busy.value.has(atomicNumber)) return isBookmarked(atomicNumber)
  markBusy(atomicNumber, true)
  error.value = ''
  try {
    if (isBookmarked(atomicNumber)) {
      await api(`/api/v1/bookmarks/${atomicNumber}`, { method: 'DELETE' })
      items.value = items.value.filter((row) => row.atomic_number !== atomicNumber)
      return false
    }
    const created = await api('/api/v1/bookmarks', {
      method: 'POST',
      body: { atomic_number: atomicNumber },
    })
    items.value = [created, ...items.value.filter((row) => row.atomic_number !== atomicNumber)]
    return true
  } catch (e) {
    // 409 → sudah ada di server (mis. dibuka di tab lain); samakan state lokal.
    if (e.status === 409) {
      await load(true)
      return isBookmarked(atomicNumber)
    }
    if (e.status === 401) loaded = false
    error.value = e.message
    throw e
  } finally {
    markBusy(atomicNumber, false)
  }
}

async function remove(atomicNumber) {
  markBusy(atomicNumber, true)
  error.value = ''
  try {
    await api(`/api/v1/bookmarks/${atomicNumber}`, { method: 'DELETE' })
    items.value = items.value.filter((row) => row.atomic_number !== atomicNumber)
  } catch (e) {
    if (e.status === 401) loaded = false
    error.value = e.message
    throw e
  } finally {
    markBusy(atomicNumber, false)
  }
}

/** Dipanggil saat logout atau berganti pengguna. */
function reset() {
  items.value = []
  loaded = false
  pending = null
  error.value = ''
  busy.value = new Set()
}

export function useBookmarks() {
  return { items, loading, busy, error, load, isBookmarked, toggle, remove, reset }
}
