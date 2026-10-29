import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'
import { VitePWA } from 'vite-plugin-pwa'

const APP_NAME = 'BioChemVerse'
const APP_DESCRIPTION =
  'Platform edukasi kimia, forensik, dan anatomi: tabel periodik, kuis, simulasi, dan katalog prosedur bedah.'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
    // PWA: manifest + service worker (Workbox). Aktif saat build, mati saat dev.
    VitePWA({
      registerType: 'prompt',
      includeAssets: ['favicon.svg', 'icons.svg', 'apple-touch-icon.png'],
      manifest: {
        id: '/',
        name: APP_NAME,
        short_name: 'BioChem',
        description: APP_DESCRIPTION,
        lang: 'id',
        start_url: '/',
        scope: '/',
        display: 'standalone',
        orientation: 'portrait-primary',
        background_color: '#0f172a',
        theme_color: '#0f172a',
        categories: ['education', 'science'],
        icons: [
          { src: '/icons/pwa-192.png', sizes: '192x192', type: 'image/png', purpose: 'any' },
          { src: '/icons/pwa-512.png', sizes: '512x512', type: 'image/png', purpose: 'any' },
          { src: '/icons/pwa-maskable-512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
        ],
      },
      workbox: {
        // SPA: semua navigasi jatuh ke index.html (router memilih halamannya).
        navigateFallback: '/index.html',
        navigateFallbackDenylist: [/^\/api\//],
        globPatterns: ['**/*.{js,css,html,svg,png,ico,woff2}'],
        // Model 3D bisa besar; biarkan lewat network, jangan disimpan ke cache.
        maximumFileSizeToCacheInBytes: 3 * 1024 * 1024,
        runtimeCaching: [
          {
            // Data dinamis (progres, kuis, auth) selalu dari jaringan.
            urlPattern: ({ url, request }) =>
              request.destination === '' && url.pathname.startsWith('/api/'),
            handler: 'NetworkOnly',
          },
          {
            // Sumber statis lintas-origin (three.js contohnya) boleh dari cache.
            urlPattern: ({ request }) =>
              ['script', 'style', 'font', 'image'].includes(request.destination),
            handler: 'CacheFirst',
            options: {
              cacheName: 'bcv-assets',
              expiration: { maxEntries: 200, maxAgeSeconds: 60 * 60 * 24 * 30 },
            },
          },
        ],
      },
      devOptions: { enabled: false },
    }),
  ],
})
