import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  // Kembalikan posisi scroll saat tombol back/forward; halaman baru selalu dari atas.
  scrollBehavior: (to, from, savedPosition) => savedPosition ?? { top: 0 },
  routes: [
    { path: '/', name: 'home', component: HomeView },
    {
      path: '/modules',
      name: 'modules',
      component: () => import('../views/ModulesView.vue'),
    },
    {
      path: '/operasi',
      name: 'surgery',
      component: () => import('../views/SurgeryView.vue'),
    },
    {
      path: '/tabel-periodik',
      name: 'periodic-table',
      component: () => import('../views/PeriodicTableView.vue'),
    },
    {
      path: '/tabel-periodik/:symbol',
      name: 'element-detail',
      component: () => import('../views/ElementDetailView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('../views/ForgotPasswordView.vue'),
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: () => import('../views/ResetPasswordView.vue'),
    },
    {
      path: '/tentang',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/bantuan',
      name: 'help',
      component: () => import('../views/HelpView.vue'),
    },
    {
      path: '/kebijakan-privasi',
      name: 'privacy',
      component: () => import('../views/PrivacyView.vue'),
    },
    {
      path: '/kebijakan-cookies',
      name: 'cookies',
      component: () => import('../views/CookiesView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
    },
  ],
})

export default router
