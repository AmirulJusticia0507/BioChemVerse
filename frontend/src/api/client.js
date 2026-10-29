/**
 * Klien API tipikal untuk BioChemVerse.
 * Base URL: env VITE_API_URL (default http://localhost:8000)
 * Token JWT disimpan di localStorage dan otomatis dikirim sebagai Bearer.
 */

const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const TOKEN_KEY = 'bcv_token'
const USER_KEY = 'bcv_user'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token)
  else localStorage.removeItem(TOKEN_KEY)
}

export function getStoredUser() {
  try {
    return JSON.parse(localStorage.getItem(USER_KEY) || 'null')
  } catch {
    return null
  }
}

export function setStoredUser(user) {
  if (user) localStorage.setItem(USER_KEY, JSON.stringify(user))
  else localStorage.removeItem(USER_KEY)
}

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

/**
 * @param {string} path  path relatif, mis. '/api/v1/modules'
 * @param {{method?: string, body?: unknown, auth?: boolean}} options
 */
export async function api(path, { method = 'GET', body, auth = true } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  const token = getToken()
  if (auth && token) headers.Authorization = `Bearer ${token}`

  let res
  try {
    res = await fetch(`${BASE}${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
    })
  } catch {
    throw new ApiError('Tidak dapat terhubung ke server API', 0)
  }

  let data = null
  try {
    data = await res.json()
  } catch {
    /* respons bukan JSON */
  }

  if (!res.ok) {
    const detail = data?.detail
    const message =
      typeof detail === 'string'
        ? detail
        : Array.isArray(detail)
          ? detail.map((d) => d.msg).join('; ')
          : `Permintaan gagal (HTTP ${res.status})`
    throw new ApiError(message, res.status)
  }
  return data
}

export default api
