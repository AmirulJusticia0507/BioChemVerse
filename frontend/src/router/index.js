import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
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
    },    {
      path: '/tabel-periodik/:symbol',
      name: 'element-detail',
      component: () => import('../views/ElementDetailView.vue'),
    },
    {
      path: '/bandingkan',
      name: 'compare',
      component: () => import('../views/CompareView.vue'),
    },
    {
      path: '/belajar',
      name: 'study',
      component: () => import('../views/StudyView.vue'),
    },
    {
      path: '/kalkulator',
      name: 'calculator',
      component: () => import('../views/CalculatorView.vue'),
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
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
    },
  ],
  scrollBehavior: () => ({ top: 0 }),
})

export default router
