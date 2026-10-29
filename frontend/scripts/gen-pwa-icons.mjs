/**
 * Render ikon PWA (PNG) dari public/icons/app-icon.svg.
 * Jalankan setelah mengubah app-icon.svg:  node scripts/gen-pwa-icons.mjs
 *
 * Memakai Chromium yang tersedia di mesin ini: paket `patchright` lokal bila ada,
 * atau Playwright bawaan ekstensi CodeGPT (tidak perlu dependensi baru).
 */
import { createRequire } from 'node:module'
import { existsSync, readdirSync } from 'node:fs'
import { mkdir, readFile } from 'node:fs/promises'
import { homedir } from 'node:os'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')

function loadChromium() {
  const roots = [process.cwd() + '/', root + '/']
  for (const base of [join(homedir(), '.vscode/extensions'), join(homedir(), '.vscode-server/extensions')]) {
    if (!existsSync(base)) continue
    const dirs = readdirSync(base)
      .filter((d) => d.startsWith('danielsanmedium.dscodegpt-'))
      .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }))
    if (dirs.length) roots.push(join(base, dirs[dirs.length - 1], 'standalone') + '/')
  }
  for (const r of roots) {
    for (const pkg of ['patchright', 'playwright']) {
      try {
        const mod = createRequire(r)(pkg)
        const chromium = mod?.chromium ?? mod?.default?.chromium
        if (chromium) return chromium
      } catch {}
    }
  }
  throw new Error('Chromium (patchright/playwright) tidak ditemukan')
}

const outDir = resolve(root, 'public/icons')
const svg = await readFile(resolve(outDir, 'app-icon.svg'), 'utf8')

const targets = [
  { name: 'pwa-192.png', size: 192 },
  { name: 'pwa-512.png', size: 512 },
  // Maskable: padding 20% supaya aman saat dipotong bentuk lingkaran/squircle.
  { name: 'pwa-maskable-512.png', size: 512, padding: 0.2 },
  { name: 'apple-touch-icon.png', size: 180 },
]

await mkdir(outDir, { recursive: true })
const browser = await loadChromium().launch()
const page = await browser.newPage()

for (const { name, size, padding = 0 } of targets) {
  const inner = Math.round(size * (1 - padding * 2))
  const offset = Math.round((size - inner) / 2)
  await page.setViewportSize({ width: size, height: size })
  await page.setContent(`<body style="margin:0;background:#0f172a">
    <div style="position:absolute;left:${offset}px;top:${offset}px;width:${inner}px;height:${inner}px">
      ${svg.replace('<svg ', `<svg width="${inner}" height="${inner}" `)}
    </div>
  </body>`)
  await page.screenshot({ path: resolve(outDir, name) })
  console.log(`ok ${name} (${size}px)`)
}

await browser.close()
