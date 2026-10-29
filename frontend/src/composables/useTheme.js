import { computed, ref } from 'vue'

const STORAGE_KEY = 'bcv_theme'
const theme = ref(document.documentElement.dataset.theme === 'light' ? 'light' : 'dark')

function applyTheme(next) {
  theme.value = next
  document.documentElement.dataset.theme = next
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', next === 'dark' ? '#0f172a' : '#f8fafc')
  localStorage.setItem(STORAGE_KEY, next)
}

export function useTheme() {
  const isDark = computed(() => theme.value === 'dark')
  const toggleTheme = () => applyTheme(isDark.value ? 'light' : 'dark')
  return { theme, isDark, toggleTheme, applyTheme }
}
