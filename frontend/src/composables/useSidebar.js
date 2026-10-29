/**
 * State bersama tampilan sidebar: tampil/sembunyi & ciut/lebar di desktop,
 * serta status drawer di mobile.
 * Dipakai App.vue (menyesuaikan padding konten) dan AppSidebar.vue (visual sidebar).
 */
import { computed, ref } from 'vue'

export const sidebarCollapsed = ref(false)
export const sidebarDesktopHidden = ref(false)
export const sidebarMobileOpen = ref(false)

// Lebar sidebar mengikuti keadaan ciut/lebar.
export const sidebarWidth = computed(() => (sidebarDesktopHidden.value ? 0 : (sidebarCollapsed.value ? 72 : 240)))

export const toggleSidebarCollapsed = () => (sidebarCollapsed.value = !sidebarCollapsed.value)
export const toggleDesktopSidebar = () => (sidebarDesktopHidden.value = !sidebarDesktopHidden.value)
