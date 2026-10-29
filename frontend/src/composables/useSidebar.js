/**
 * State bersama tampilan sidebar: ciut/lebar di desktop, dan status drawer di mobile.
 * Dipakai App.vue (menyesuaikan padding konten) dan AppSidebar.vue (visual sidebar).
 */
import { computed, ref } from 'vue'

export const sidebarCollapsed = ref(false)
export const sidebarMobileOpen = ref(false)

// Lebar sidebar mengikuti keadaan ciut/lebar.
export const sidebarWidth = computed(() => (sidebarCollapsed.value ? 72 : 240))

export const toggleSidebarCollapsed = () => (sidebarCollapsed.value = !sidebarCollapsed.value)
