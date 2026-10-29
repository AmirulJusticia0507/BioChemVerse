<template>
  <div class="flex flex-col items-center">
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,380px)_minmax(0,260px)] lg:items-start">
      <!-- Ilustrasi anatomi: pilih tampilan tubuh pria (default) atau wanita -->
      <div class="flex w-full flex-col items-center">
        <div
          class="mb-3 inline-flex rounded-lg bg-slate-800 p-1 ring-1 ring-slate-700"
          role="group"
          aria-label="Pilih tampilan anatomi"
        >
          <button
            v-for="opt in variants"
            :key="opt.id"
            type="button"
            class="rounded-md px-3 py-1.5 text-sm font-medium transition-colors focus:ring-2 focus:ring-blue-500/50 focus:outline-none"
            :class="variant === opt.id ? 'bg-blue-500 text-white' : 'text-slate-300 hover:bg-slate-700'"
            :aria-pressed="variant === opt.id"
            @click="variant = opt.id"
          >
            {{ opt.label }}
          </button>
        </div>

        <div class="relative aspect-[3/4] w-full max-w-md overflow-hidden rounded-2xl border border-slate-700 bg-slate-950 shadow-2xl shadow-blue-950/30">
          <iframe
            :key="variant"
            :src="sketchfabModel.embedUrl"
            :title="`Model 3D anatomi ${variantLabel}`"
            class="absolute inset-0 h-full w-full"
            allow="autoplay; fullscreen; xr-spatial-tracking"
            allowfullscreen
          />
          <canvas v-if="false" ref="canvas" class="block h-full w-full" />
        </div>
        <p class="mt-2 text-center text-[11px] text-slate-500">
          Model 3D: <a :href="sketchfabModel.sourceUrl" class="underline hover:text-slate-300" target="_blank" rel="noopener">{{ sketchfabModel.title }}</a>
          oleh {{ sketchfabModel.author }} · CC BY 4.0
        </p>
        <div
          class="mt-3 max-h-44 w-full max-w-md overflow-y-auto rounded-xl border border-slate-800 bg-slate-900/40 p-2"
          role="group"
          aria-label="Pilih bagian tubuh"
        >
          <div class="flex flex-wrap justify-center gap-1.5">
            <button
              v-for="region in visibleRegions"
              :key="region.id"
              type="button"
              class="rounded-full border px-2.5 py-1 text-[11px] transition-colors focus:ring-2 focus:ring-blue-500/50 focus:outline-none"
              :class="selected === region.id ? 'border-blue-400 bg-blue-500/20 text-blue-100' : 'border-slate-700 bg-slate-800 text-slate-300 hover:border-slate-500'"
              @click="select(region.id)"
            >
              {{ region.label }}
            </button>
          </div>
        </div>

        <svg
          v-if="false"
          viewBox="0 0 300 620"
          role="img"
          :aria-label="`Ilustrasi anatomi tubuh manusia ${variantLabel} beserta organ dalam`"
          class="mx-auto h-auto w-72 text-slate-400 sm:w-[300px]"
        >
        <defs>
          <radialGradient id="skinFill" cx="46%" cy="26%" r="78%">
            <stop offset="0%" stop-color="#3B4A61" />
            <stop offset="55%" stop-color="#26334A" />
            <stop offset="100%" stop-color="#172033" />
          </radialGradient>
          <linearGradient id="clothFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#1B2537" />
            <stop offset="100%" stop-color="#111A29" />
          </linearGradient>
        </defs>

        <!-- Siluet tubuh: leher → bahu → lengan → panggul → kaki → naik kembali → kepala -->
        <g stroke-linejoin="round" stroke-linecap="round">
          <path :d="silPath('bodyPath')" fill="url(#skinFill)" stroke="currentColor" stroke-width="1.3" />
          <!-- pakaian dalam -->
          <path :d="silPath('shortsPath')" fill="url(#clothFill)" stroke="currentColor" stroke-width="1.2" />
          <!-- telinga -->
          <path
            :d="variant === 'wanita' ? 'M125 44 C121 42 119 48 120 54 C121 60 123 63 126 62 Z' : 'M124 44 C120 42 118 48 119 54 C120 60 122 63 125 62 Z'"
            fill="url(#skinFill)" stroke="currentColor" stroke-width="1.1"
          />
          <path
            :d="variant === 'wanita' ? 'M175 44 C179 42 181 48 180 54 C179 60 177 63 174 62 Z' : 'M176 44 C180 42 182 48 181 54 C180 60 178 63 175 62 Z'"
            fill="url(#skinFill)" stroke="currentColor" stroke-width="1.1"
          />
          <!-- lekuk otot & permukaan -->
          <g fill="none" stroke="currentColor" stroke-width="0.9" opacity="0.55">
            <path v-for="(d, i) in silPath('detailPaths')" :key="i" :d="d" />
          </g>
        </g>

        <!-- Organ & bagian tubuh (klik + keyboard) -->
        <!-- Urutan: bagian terluar dulu agar organ dalam berada di atas dan menerima klik -->
        <g
          v-for="region in orderedRegions"
          :key="region.id"
          class="cursor-pointer outline-none"
          :tabindex="0"
          role="button"
          :aria-label="region.label"
          :aria-pressed="selected === region.id"
          @click="select(region.id)"
          @keydown.enter.prevent="select(region.id)"
          @keydown.space.prevent="select(region.id)"
        >
          <g :class="[regionClass(region), 'transition-colors duration-150']">
            <path v-for="(d, i) in regionPaths(region)" :key="i" :d="d" />
            <circle v-for="(c, i) in region.dots ?? []" :key="'c' + i" :cx="c[0]" :cy="c[1]" :r="c[2]" />
          </g>
        </g>
        </svg>
      </div>

      <!-- Panel keterangan -->
      <aside class="w-full rounded-xl bg-slate-800 p-5 ring-1 ring-slate-700 lg:sticky lg:top-6">
        <p class="text-sm text-slate-400">{{ selected ? 'Bagian dipilih' : 'Klik bagian tubuh' }}</p>
        <h2 class="mt-1 text-lg font-semibold text-white">{{ selectedInfo?.label ?? 'Anatomi manusia' }}</h2>
        <p class="mt-2 text-sm text-slate-300">
          {{ selectedInfo?.desc ?? 'Pilih organ atau bagian tubuh pada ilustrasi untuk melihat keterangannya.' }}
        </p>
        <ul v-if="selectedItems" class="mt-4 space-y-1.5 text-sm text-slate-300">
          <li v-for="item in selectedItems" :key="item" class="flex gap-2">
            <span class="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-blue-500" aria-hidden="true" />
            <span>{{ item }}</span>
          </li>
        </ul>
        <button
          v-if="selected"
          type="button"
          class="mt-5 w-full rounded-lg bg-slate-700 px-4 py-2 text-sm font-medium text-white hover:bg-slate-600 focus:ring-2 focus:ring-blue-500/50 focus:outline-none"
          @click="select(null)"
        >
          Reset pilihan
        </button>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

// Tampilan anatomi: siluet pria (default) atau wanita.
const variants = [
  { id: 'pria', label: 'Pria' },
  { id: 'wanita', label: 'Wanita' },
]
const variant = ref('pria')
const variantLabel = computed(() => variants.find((v) => v.id === variant.value)?.label ?? '')
const sketchfabModel = computed(() => ({
  pria: {
    title: 'Male base muscular anatomy',
    author: 'CharacterZone',
    sourceUrl: 'https://sketchfab.com/3d-models/male-base-muscular-anatomy-0954aa04666d45aab9633009318f7b66',
    embedUrl: 'https://sketchfab.com/models/0954aa04666d45aab9633009318f7b66/embed?autospin=0&ui_theme=dark&ui_infos=0',
  },
  wanita: {
    title: 'Female muscle human body',
    author: 'Rena',
    sourceUrl: 'https://sketchfab.com/3d-models/female-muscle-human-body-aa022f8c27e04aea89e731f66484a299',
    embedUrl: 'https://sketchfab.com/models/aa022f8c27e04aea89e731f66484a299/embed?autospin=0&ui_theme=dark&ui_infos=0',
  },
})[variant.value])
const canvas = ref(null)

let renderer
let scene
let camera
let controls
let body
let animationFrame
let resizeObserver

const addPart = (parent, geometry, material, position, scale = [1, 1, 1]) => {
  const mesh = new THREE.Mesh(geometry, material)
  mesh.position.set(...position)
  mesh.scale.set(...scale)
  parent.add(mesh)
  return mesh
}

const buildBody = () => {
  body?.removeFromParent()
  body = new THREE.Group()
  const female = variant.value === 'wanita'
  const skin = new THREE.MeshStandardMaterial({ color: female ? 0xb96a62 : 0xa9504b, roughness: 0.74, transparent: true, opacity: 0.78 })
  const cloth = new THREE.MeshStandardMaterial({ color: 0xe8d9bd, roughness: 0.88 })
  const lung = new THREE.MeshStandardMaterial({ color: 0xc47b92, roughness: 0.65 })
  const heart = new THREE.MeshStandardMaterial({ color: 0x991b1b, roughness: 0.5 })
  const organ = new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.7 })
  const joint = new THREE.SphereGeometry(0.28, 28, 18)
  const limb = new THREE.CapsuleGeometry(0.25, 1.25, 8, 16)

  addPart(body, new THREE.SphereGeometry(0.58, 32, 22), skin, [0, 3.72, 0], [0.92, 1.12, 0.9])
  addPart(body, new THREE.CylinderGeometry(0.22, 0.28, 0.43, 20), skin, [0, 3.1, 0])
  addPart(body, new THREE.SphereGeometry(1, 36, 24), skin, [0, 2.08, 0], [female ? 0.94 : 1.1, 1.2, 0.55])
  addPart(body, new THREE.SphereGeometry(1, 32, 22), skin, [0, 0.74, 0], [female ? 0.98 : 0.92, 0.72, 0.52])
  addPart(body, new THREE.CylinderGeometry(female ? 0.72 : 0.68, female ? 0.83 : 0.78, 0.75, 28), cloth, [0, 0.34, 0], [1, 1, 0.72])
  // Atlas anatomy layer: organ sederhana di depan torso, bukan aset berlisensi pihak ketiga.
  addPart(body, new THREE.SphereGeometry(0.43, 28, 18), lung, [-0.35, 2.05, 0.56], [0.82, 1.22, 0.3])
  addPart(body, new THREE.SphereGeometry(0.43, 28, 18), lung, [0.35, 2.05, 0.56], [0.82, 1.22, 0.3])
  const cardiac = addPart(body, new THREE.SphereGeometry(0.31, 24, 16), heart, [0.08, 1.68, 0.76], [0.9, 1.15, 0.42])
  cardiac.rotation.z = -0.3
  addPart(body, new THREE.SphereGeometry(0.56, 30, 18), organ, [0.2, 1.06, 0.56], [1.25, 0.62, 0.28])
  for (let row = 0; row < 3; row += 1) for (let col = 0; col < 2; col += 1) {
    addPart(body, new THREE.TorusGeometry(0.16, 0.055, 10, 20), organ, [(col - 0.5) * 0.36, 0.38 - row * 0.19, 0.62])
  }
  for (const side of [-1, 1]) {
    addPart(body, joint, skin, [side * (female ? 0.92 : 1.1), 2.62, 0])
    const upperArm = addPart(body, limb, skin, [side * (female ? 1.13 : 1.32), 1.72, 0], [0.82, 1, 0.82])
    upperArm.rotation.z = side * 0.17
    const lowerArm = addPart(body, limb, skin, [side * (female ? 1.3 : 1.52), 0.3, 0], [0.7, 0.9, 0.7])
    lowerArm.rotation.z = side * 0.1
    addPart(body, new THREE.SphereGeometry(0.24, 22, 14), skin, [side * (female ? 1.38 : 1.62), -0.53, 0], [0.85, 1.18, 0.65])
    addPart(body, limb, skin, [side * (female ? 0.48 : 0.5), -1.18, 0], [female ? 0.9 : 1, 1.27, 0.92])
    addPart(body, limb, skin, [side * (female ? 0.48 : 0.5), -2.74, 0], [female ? 0.72 : 0.82, 1.25, 0.78])
    addPart(body, new THREE.SphereGeometry(0.3, 22, 14), skin, [side * (female ? 0.48 : 0.5), -3.9, 0.14], [0.86, 0.55, 1.45])
  }
  if (female) for (const side of [-1, 1]) addPart(body, new THREE.SphereGeometry(0.35, 24, 16), skin, [side * 0.35, 2.15, 0.45], [1, 1, 0.55])
  scene.add(body)
  frameCamera()
}

// Bingkai kamera dari bounding box sosok: seluruh tubuh (termasuk kaki) dijamin masuk
// layar, dan tinggi figure mengikuti rasio canvas agar tidak terpotong saat sempit.
const frameCamera = () => {
  if (!camera || !body) return
  const box = new THREE.Box3().setFromObject(body)
  const size = box.getSize(new THREE.Vector3())
  const center = box.getCenter(new THREE.Vector3())
  const fitHeight = size.y * 1.18
  const fitWidth = size.x * 1.45
  const vFov = THREE.MathUtils.degToRad(camera.fov)
  const distance = Math.max(
    fitHeight / 2 / Math.tan(vFov / 2),
    fitWidth / 2 / Math.tan(vFov / 2) / Math.max(camera.aspect, 0.01),
  )
  camera.position.set(center.x, center.y, center.z + distance)
  camera.lookAt(center)
  if (controls) {
    controls.target.copy(center)
    controls.minDistance = distance * 0.85
    controls.maxDistance = distance * 1.6
    controls.update()
  }
  camera.updateProjectionMatrix()
}

const resizeScene = () => {
  const { clientWidth: width, clientHeight: height } = canvas.value
  if (!width || !height) return
  renderer.setSize(width, height, false)
  camera.aspect = width / height
  camera.updateProjectionMatrix()
  frameCamera()
}

onMounted(() => {
  if (!canvas.value) return
  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100)
  camera.position.set(0, 0.15, 12)
  renderer = new THREE.WebGLRenderer({ canvas: canvas.value, antialias: true, alpha: true })
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  scene.add(new THREE.HemisphereLight(0xc7d2fe, 0x0f172a, 2.5))
  const key = new THREE.DirectionalLight(0xffffff, 3.5)
  key.position.set(4, 6, 6)
  scene.add(key)
  const rim = new THREE.DirectionalLight(0x60a5fa, 2)
  rim.position.set(-5, 2, -4)
  scene.add(rim)
  controls = new OrbitControls(camera, canvas.value)
  controls.target.set(0, 0, 0)
  controls.enablePan = false
  controls.minPolarAngle = Math.PI / 3
  controls.maxPolarAngle = Math.PI * 0.68
  buildBody()
  resizeObserver = new ResizeObserver(resizeScene)
  resizeObserver.observe(canvas.value)
  resizeScene()
  const render = () => {
    controls.update()
    renderer.render(scene, camera)
    animationFrame = requestAnimationFrame(render)
  }
  render()
})

watch(variant, () => {
  selected.value = null
  if (scene) buildBody()
})

onBeforeUnmount(() => {
  cancelAnimationFrame(animationFrame)
  resizeObserver?.disconnect()
  controls?.dispose()
  renderer?.dispose()
})

const selected = ref(null)
const selectedInfo = computed(() => visibleRegions.value.find((r) => r.id === selected.value) ?? null)

// Bagian khusus wanita (payudara, reproduksi) hanya tampil pada tampilan wanita.
const visibleRegions = computed(() => (variant.value === 'wanita' ? regions : regions.filter((r) => !r.femaleOnly)))

// Teks panel ikut berubah bila bagian itu punya deskripsi khusus wanita.
const selectedItems = computed(() =>
  variant.value === 'wanita' ? (selectedInfo.value?.itemsWanita ?? selectedInfo.value?.items) : selectedInfo.value?.items,
)

// Bagian tubuh wanita memakai geo-nya sendiri bila ada, sisanya sama dengan pria.
const regionPaths = (region) => (variant.value === 'wanita' ? (region.geo?.wanita ?? region.d) : region.d)

// Bagian luar (lengan, kaki, tulang, panggul) digambar lebih dulu; organ dalam digambar terakhir
// supaya dapat diklik di area yang bertumpang tindih (mis. jantung di depan kolumna).
const drawnLast = ['kepala', 'leher', 'dada', 'payudara', 'reproduksi-wanita', 'jantung', 'hati', 'lambung', 'usus', 'ginjal']
const orderedRegions = computed(() => [
  ...visibleRegions.value.filter((r) => !drawnLast.includes(r.id)),
  ...visibleRegions.value.filter((r) => drawnLast.includes(r.id)),
])

const select = (id) => (selected.value = selected.value === id ? null : id)

const regionClass = (region) =>
  selected.value === region.id ? 'fill-blue-500/60 stroke-blue-100' : region.tint

// Rangka siluet per tampilan: garis luar, celana, dan detail permukaan.
const silhouettes = {
  pria: { body: 'bodyPath', shorts: 'shortsPath', details: 'detailPaths' },
  wanita: { body: 'bodyPathWanita', shorts: 'shortsPathWanita', details: 'detailPathsWanita' },
}
const silPath = (key) => ({ pria: { bodyPath, shortsPath, detailPaths }, wanita: { bodyPathWanita, shortsPathWanita, detailPaths: detailPathsWanita } })[variant.value][key]

// Siluet laki-laki, ±7,5 kepala: kepala 14–92, bahu 112–130, panggul ±360, tumit 600.
const bodyPath = [
  'M138 88',
  'C126 92 120 102 118 114',
  'C120 126 108 128 96 132',
  'C82 138 72 150 68 168',
  'C65 192 60 222 56 252',
  'C52 282 48 310 46 334',
  'C45 352 44 370 44 386',
  'C43 398 38 410 32 421',
  'C26 432 21 442 20 452',
  'C19 461 21 467 26 468',
  'C32 469 36 464 39 456',
  'C44 442 52 426 58 410',
  'C64 393 70 375 73 358',
  'C76 340 80 322 82 306',
  'C84 292 86 280 88 270',
  'C91 262 94 256 97 250',
  'C101 264 103 284 105 306',
  'C107 330 107 354 105 378',
  'C103 402 103 428 103 452',
  'C103 482 101 512 100 538',
  'C99 560 98 580 102 592',
  'C105 602 113 604 119 600',
  'C124 597 124 590 122 580',
  'C119 562 118 540 118 516',
  'C118 490 120 462 122 436',
  'C124 412 126 395 131 384',
  'C137 376 143 372 150 372',
  'C157 372 163 376 169 384',
  'C174 395 176 412 178 436',
  'C180 462 182 490 182 516',
  'C182 540 181 562 178 580',
  'C176 590 176 597 181 600',
  'C187 604 195 602 198 592',
  'C202 580 201 560 200 538',
  'C199 512 197 482 197 452',
  'C197 428 197 402 195 378',
  'C193 354 193 330 195 306',
  'C197 284 199 264 203 250',
  'C206 256 209 262 212 270',
  'C214 280 216 292 218 306',
  'C220 322 224 340 227 358',
  'C230 375 236 393 242 410',
  'C248 426 256 442 261 456',
  'C264 464 268 469 274 468',
  'C279 467 281 461 280 452',
  'C279 442 274 432 268 421',
  'C262 410 257 398 256 386',
  'C256 370 255 352 254 334',
  'C252 310 248 282 244 252',
  'C240 222 235 192 232 168',
  'C228 150 218 138 204 132',
  'C192 128 180 126 182 114',
  'C179 102 179 94 173 86',
  'C172 76 170 64 164 56',
  'C166 46 164 36 158 28',
  'C154 18 146 14 138 18',
  'C130 22 126 32 128 42',
  'C124 50 124 62 127 72',
  'C130 79 133 84 138 88',
  'Z',
].join(' ')

const shortsPath =
  'M96 338 C112 334 136 334 150 340 C164 334 188 334 204 338 C208 352 208 366 206 382 C203 398 203 410 202 424 C198 442 190 456 184 468 L168 464 C166 444 166 424 164 408 L150 404 L136 408 C134 424 134 444 132 464 L116 468 C110 456 102 442 98 424 C97 410 97 398 94 382 C92 366 92 352 96 338 Z'

const detailPaths = [
  'M123 120 C133 127 167 127 177 120',
  'M137 134 C141 147 141 162 138 174',
  'M163 134 C159 147 159 162 162 174',
  'M150 196 V236',
  'M150 254 V304',
  'M124 228 C118 250 116 272 118 292',
  'M176 228 C182 250 184 272 182 292',
  'M118 430 C114 452 114 474 116 496',
  'M182 430 C186 452 186 474 184 496',
  'M113 392 C120 389 130 389 137 392 M163 392 C170 389 180 389 187 392',
  'M57 206 C54 230 51 252 49 272',
  'M243 206 C246 230 249 252 251 272',
]

// Siluet wanita, proporsi ±7,5 kepala: bahu lebih sempit (108–192), pinggang ±88,
// panggul ±84, payudara di toraks atas (142–162), tumit tetap 600.
const bodyPathWanita = [
  'M140 88',
  'C130 92 125 102 124 114',
  'C126 126 114 128 104 132',
  'C92 138 84 150 81 168',
  'C79 192 75 222 72 252',
  'C70 282 67 310 66 334',
  'C65 352 64 370 64 386',
  'C63 398 59 410 54 421',
  'C49 432 45 442 44 452',
  'C43 461 45 467 50 468',
  'C56 469 60 464 62 456',
  'C66 442 73 426 78 410',
  'C83 393 88 375 90 358',
  'C92 340 94 322 95 306',
  'C96 292 96 280 96 270',
  'C97 262 98 256 99 250',
  'C101 264 102 284 102 306',
  'C102 330 100 354 98 378',
  'C96 402 96 428 96 452',
  'C96 482 94 512 94 538',
  'C93 560 92 580 96 592',
  'C99 602 107 604 113 600',
  'C118 597 118 590 116 580',
  'C113 562 112 540 112 516',
  'C112 490 113 462 114 436',
  'C115 412 116 395 120 384',
  'C126 376 137 372 150 372',
  'C163 372 174 376 180 384',
  'C184 395 185 412 186 436',
  'C187 462 188 490 188 516',
  'C188 540 187 562 184 580',
  'C182 590 182 597 187 600',
  'C193 604 201 602 204 592',
  'C208 580 207 560 206 538',
  'C206 512 204 482 204 452',
  'C204 428 204 402 202 378',
  'C200 354 198 330 198 306',
  'C198 284 199 264 201 250',
  'C202 256 203 262 204 270',
  'C204 280 204 292 205 306',
  'C206 322 208 340 210 358',
  'C212 375 217 393 222 410',
  'C227 426 234 442 238 456',
  'C240 464 244 469 250 468',
  'C255 467 257 461 256 452',
  'C255 442 251 432 246 421',
  'C241 410 237 398 236 386',
  'C236 370 235 352 234 334',
  'C233 310 230 282 228 252',
  'C225 222 221 192 219 168',
  'C216 150 208 138 196 132',
  'C186 128 174 126 176 114',
  'C175 102 175 94 170 86',
  'C169 76 168 64 163 56',
  'C165 46 163 36 158 28',
  'C154 18 146 14 140 18',
  'C132 22 128 32 130 42',
  'C127 50 126 62 128 72',
  'C131 79 134 84 140 88',
  'Z',
].join(' ')

const shortsPathWanita =
  'M98 342 C112 338 135 338 150 344 C165 338 188 338 202 342 C205 356 204 366 202 382 C199 398 199 410 198 424 C194 442 187 456 182 468 L168 464 C166 444 166 424 164 408 L150 404 L136 408 C134 424 134 444 132 464 L118 468 C112 456 105 442 101 424 C100 410 100 398 97 382 C95 366 95 356 98 342 Z'

const detailPathsWanita = [
  // klavikula & tulang selangka
  'M126 120 C136 127 164 127 174 120',
  // payudara
  'M134 146 C132 158 136 170 144 173',
  'M166 146 C168 158 164 170 156 173',
  // garis sternum di antara payudara
  'M150 132 V180',
  // pinggang
  'M122 234 C118 252 116 272 117 290',
  'M178 234 C182 252 184 272 183 290',
  // garis otot perut
  'M150 200 V272',
  // panggul
  'M104 348 C112 340 122 336 130 336',
  'M196 348 C188 340 178 336 170 336',
  // lutut & betis
  'M108 392 C112 389 120 389 123 392 M177 392 C180 389 188 389 192 392',
  'M110 430 C107 452 107 474 110 496',
  'M190 430 C193 452 193 474 190 496',
  'M76 206 C73 230 71 252 70 272',
  'M224 206 C227 230 229 252 230 272',
]

const line = 'stroke-[1.1] fill-none'
const filled = 'stroke-[1.1]'

const regions = [
  {
    id: 'kepala',
    label: 'Kepala & Otak',
    desc: 'Tengkorak melindungi otak: cerebrum, cerebellum, dan batang otak.',
    items: ['Cerebrum (frontal, parietal, temporal, oksipital)', 'Cerebellum', 'Batang otak', 'Tengkorak & wajah'],
    tint: `fill-slate-600/40 stroke-slate-300 ${filled}`,
    d: [
      'M129 52 C126 36 134 22 150 20 C166 20 174 34 171 52 C173 60 166 66 158 64 C155 70 145 70 142 64 C134 66 127 60 129 52 Z',
      // gyri
      'M150 24 V62 M134 40 C138 36 142 38 142 43 C142 48 136 49 134 46 M158 40 C162 36 166 38 166 43 C166 48 160 49 158 46 M138 56 C142 54 146 56 146 59 M154 56 C158 54 162 56 162 59',
      // cerebellum + batang otak
      'M144 64 C148 62 152 62 156 64 C156 70 148 70 144 64 Z M148 62 V84 M152 62 V84',
    ],
  },
  {
    id: 'leher',
    label: 'Leher',
    desc: 'Menghubungkan kepala dan toraks: jalur napas, makanan, dan pembuluh darah besar.',
    items: ['Trakea & laring', 'Esofagus', 'Arteri karotis & vena jugularis', 'Kelenjar tiroid & paratiroid'],
    tint: `fill-slate-400/45 stroke-slate-200 ${filled}`,
    d: [
      'M137 86 C136 96 135 106 135 118 L150 122 L165 118 C165 106 164 96 163 86 C158 92 142 92 137 86 Z',
      'M145 100 V120 M155 100 V120 M140 112 C146 109 154 109 160 112',
    ],
  },
  {
    id: 'dada',
    label: 'Paru-paru & Toraks',
    desc: 'Rongga dada dilindungi tulang rusuk; di dalamnya paru-paru dan jantung.',
    items: ['Paru kanan (3 lobus)', 'Paru kiri (2 lobus & insisura jantung)', 'Bronkus & bronkiolus', 'Pleura', 'Trakea bawah'],
    tint: `fill-sky-500/35 stroke-sky-300 ${filled}`,
    d: [
      'M146 120 C146 132 146 144 146 154 M154 120 C154 132 154 144 154 154',
      // paru kanan
      'M146 148 C138 142 130 144 125 154 C119 168 117 190 120 210 C122 224 128 232 138 232 C144 232 146 228 146 220 Z',
      // paru kiri dengan insisura jantung
      'M154 148 C162 142 170 144 175 154 C181 168 183 190 180 210 C178 224 172 228 164 224 C158 221 155 214 156 204 C158 194 160 186 159 176 C158 166 156 156 154 148 Z',
      'M132 164 C128 178 127 192 129 206 M168 164 C172 176 172 186 170 196',
    ],
  },
  {
    id: 'jantung',
    label: 'Jantung',
    desc: 'Pompa ganda berotot; terletak miring di mediastinum antara kedua paru.',
    items: ['Atrium kanan & kiri', 'Ventrikel kanan & kiri', 'Aorta, arteri pulmonalis, vena cava', 'Katup trikuspid & mitral'],
    tint: `fill-red-600/80 stroke-red-200 ${filled}`,
    dots: [[146, 162, 2.4], [157, 161, 2.4], [151, 186, 1.9]],
    d: [
      // badan jantung (apeks menghadap kiri-bawah)
      'M151 150 C158 143 170 145 172 157 C175 172 166 188 154 196 C151 198 148 196 146 192 C139 182 134 172 134 162 C134 152 143 144 151 150 Z',
      // aorta
      'M156 146 C158 138 164 136 167 141 C170 146 164 150 160 149 Z',
    ],
  },
  {
    id: 'hati',
    label: 'Hati & Kandung Empedu',
    desc: 'Organ terbesar; detoksifikasi, metabolisme, penyimpanan glikogen, dan produksi empedu.',
    items: ['Lobus kanan & lobus kiri', 'Kantung empedu', 'Vena porta hepatis', 'Saluran empedu'],
    tint: `fill-orange-600/70 stroke-orange-200 ${filled}`,
    dots: [[171, 232, 3]],
    d: [
      // lobus kanan besar
      'M152 214 C160 206 176 208 182 220 C187 232 184 250 174 258 C164 265 154 262 150 252 C147 242 147 222 152 214 Z',
      // lobus kiri
      'M150 220 C144 216 136 220 134 230 C132 240 137 250 146 252 C148 244 149 232 150 220 Z',
    ],
  },
  {
    id: 'lambung',
    label: 'Lambung',
    desc: 'Kantong otot berbentuk J; mencerna makanan dengan asam lambung dan enzim.',
    items: ['Kardia & fundus', 'Korpus', 'Pilorus (sfingter)', 'Mukosa & asam HCl'],
    tint: `fill-rose-500/75 stroke-rose-200 ${filled}`,
    d: [
      'M139 216 C145 210 153 212 156 221 C160 232 158 250 150 259 C143 266 134 262 134 253 C134 240 133 224 139 216 Z',
      'M148 259 C152 265 157 270 162 273',
    ],
  },
  {
    id: 'usus',
    label: 'Usus Halus & Besar',
    desc: 'Usus halus menyerap nutrisi; usus besar menyerap air dan membentuk feses.',
    items: ['Duodenum, jejunum, ileum', 'Sekum & apendiks', 'Kolon asendens, transversum, desendens', 'Rektum'],
    tint: `fill-amber-500/45 stroke-amber-200 ${filled}`,
    d: [
      // kolon: bingkai usus besar
      'M134 278 C131 292 131 310 134 324 C137 330 142 332 146 330 L154 330 C158 332 163 330 166 324 C169 310 169 292 166 278 C166 272 160 270 156 274 L150 278 L144 274 C140 270 134 272 134 278 Z',
      'M140 286 C136 298 136 312 139 320 M160 286 C164 298 164 312 161 320',
      // usus halus berlipat
      'M143 288 C149 282 153 288 147 294 C141 300 149 304 155 298 C161 292 159 306 149 310 C141 312 145 320 153 318 M144 300 C138 306 142 314 148 312',
    ],
  },
  {
    id: 'ginjal',
    label: 'Ginjal',
    desc: 'Sepasang organ berbentuk kacang yang menyaring darah menjadi urin.',
    items: ['Korteks', 'Medula', 'Pelvis renalis', 'Nefron', 'Ureter'],
    tint: `fill-violet-500/80 stroke-violet-200 ${filled}`,
    d: [
      'M127 262 C133 255 140 260 139 270 C138 282 131 288 125 283 C120 278 121 268 127 262 Z',
      'M173 262 C179 268 180 278 175 283 C169 288 162 282 161 270 C160 260 167 255 173 262 Z',
      'M134 284 C136 292 140 298 144 302 M166 284 C164 292 160 298 156 302',
    ],
  },
  {
    id: 'serat-otot',
    label: 'Struktur Serat Otot',
    desc: 'Otot rangka tersusun berlapis dari bundel besar hingga protein kontraktil mikroskopis.',
    items: [
      'Epimisium: jaringan ikat yang membungkus seluruh otot',
      'Perimisium: membungkus bundel serat (fasikulus)',
      'Endomisium: membungkus tiap serat otot',
      'Miofibril: struktur kontraktil di dalam serat otot',
      'Aktin & miosin: filamen tipis dan tebal penggerak kontraksi',
    ],
    tint: `fill-red-500/45 stroke-red-200 ${filled}`,
    d: [],
  },
  {
    id: 'payudara',
    label: 'Payudara',
    desc: 'Kelenjar susu (mamma) di jaringan adiposa toraks, yang membesar karena estrogen dan progesteron.',
    items: ['Glandula mammaria & lobus', 'Duktus laktiferus & sinus laktiferus', 'Papilla mammae & areola', 'Vena & limfonodi aksila'],
    tint: `fill-pink-500/45 stroke-pink-200 ${filled}`,
    femaleOnly: true,
    d: [
      'M133 140 C143 135 149 145 148 158 C147 171 141 179 133 177 C126 175 124 162 127 152 Z',
      'M167 140 C157 135 151 145 152 158 C153 171 159 179 167 177 C174 175 176 162 173 152 Z',
      'M138 152 C140 150 142 150 144 152 M156 152 C158 150 160 150 162 152',
    ],
  },
  {
    id: 'panggul',
    label: 'Panggul & Perkemihan',
    desc: 'Gelang panggul menopang saluran kemih dan organ reproduksi.',
    items: ['Os coxae (ilium, iskium, pubis)', 'Kandung kemih', 'Ureter & uretra', 'Organ reproduksi pria'],
    itemsWanita: ['Os coxae (ilium, iskium, pubis)', 'Kandung kemih & uretra', 'Ureter', 'Apertura pelvis (lebih lebar)'],
    tint: `fill-teal-400/50 stroke-teal-200 ${filled}`,
    d: [
      // kandung kemih
      'M143 334 C149 329 156 329 158 336 C160 345 155 351 150 351 C144 351 140 345 142 339 Z',
      // garis panggul (ilium)
      'M118 330 C128 320 142 320 148 328 M182 330 C172 320 158 320 152 328 M114 348 C120 340 128 336 134 336 M186 348 C180 340 172 336 166 336',
    ],
    // Panggul wanita: lebih lebar, sudut subpubik lebih besar, apertura pelvis melebar.
    geo: {
      wanita: [
        'M141 334 C147 329 154 329 157 336 C159 345 154 351 149 351 C144 351 138 345 140 339 Z',
        'M108 330 C120 318 138 318 147 327 M192 330 C180 318 162 318 153 327 M102 350 C110 341 122 337 131 337 M198 350 C190 341 178 337 169 337',
        'M132 340 C126 344 118 346 112 344 M168 340 C174 344 182 346 188 344',
      ],
    },
  },
  {
    id: 'reproduksi-wanita',
    label: 'Reproduksi Wanita',
    desc: 'Uterus, tuba uterina, dan ovarium terletak di kavum pelvis antara rektum dan vesika urinaria.',
    items: ['Uterus (fundus, korpus, serviks)', 'Tuba uterina (fallopi)', 'Ovarium & folikel', 'Vagina', 'Endometrium & siklus haid'],
    tint: `fill-fuchsia-500/70 stroke-fuchsia-200 ${filled}`,
    femaleOnly: true,
    dots: [[129, 340, 2.6], [171, 340, 2.6]],
    geo: {
      wanita: [
        // uterus
        'M143 337 C147 329 153 329 157 337 C159 346 158 356 157 362 C153 366 147 366 143 362 C142 356 141 346 143 337 Z',
        // tuba uterina
        'M141 337 C134 332 128 334 127 340 C126 345 131 346 133 342 M159 337 C166 332 172 334 173 340 C174 345 169 346 167 342',
        // ovarium (circles via dots)
        // serviks & vagina
        'M146 366 C147 374 147 380 148 386 M154 366 C153 374 153 380 152 386',
      ],
    },
  },
  {
    id: 'tulang',
    label: 'Rangka & Kolumna',
    desc: 'Rangka aksial menopang tubuh dan melindungi organ dalam.',
    items: ['Kolumna vertebralis (servikal, torakal, lumbal)', 'Sternum', 'Costa 1–12', 'Os coxae'],
    tint: `fill-slate-200/35 stroke-slate-50 ${filled}`,
    d: [
      // kolumna vertebralis
      'M150 120 C153 120 154 124 154 130 C155 168 155 212 154 256 C153 300 155 330 154 356 C153 362 147 362 146 356 C145 330 147 300 146 256 C145 212 145 168 146 130 C146 124 147 120 150 120 Z',
      // sternum
      'M146 140 L154 140 L153 170 L147 170 Z',
      // rusuk
      'M150 150 C140 152 131 158 127 167 M150 164 C140 166 131 172 127 181 M150 178 C140 180 132 186 129 195 M150 192 C141 194 134 200 132 209 M150 206 C142 208 137 214 135 221 M150 154 C160 156 169 162 173 171 M150 168 C160 170 169 176 173 185 M150 182 C160 184 168 190 171 199 M150 196 C159 198 165 204 167 213 M150 210 C158 212 162 218 164 225',
    ],
  },
  {
    id: 'lengan',
    label: 'Lengan',
    desc: 'Ekstremitas atas: bahu, lengan atas, lengan bawah, dan tangan.',
    items: ['Humerus', 'Radius & ulna', 'Karpal, metakarpal, falang', 'Otot bisep & trisep'],
    tint: `fill-teal-400/25 stroke-teal-200 ${filled}`,
    d: [
      'M92 134 C80 140 70 152 66 170 C63 194 58 224 54 254 C50 284 47 312 45 336 C44 354 43 372 43 388 C42 400 37 412 31 423 C26 434 21 444 20 453 C19 461 21 466 25 467 C22 462 23 452 27 442 C32 430 38 418 41 404 C45 386 52 366 58 348 C64 330 70 312 74 294 C78 274 82 254 84 236 C86 212 82 190 82 172 C82 154 84 140 92 134 Z',
      'M208 134 C220 140 230 152 234 170 C237 194 242 224 246 254 C250 284 253 312 255 336 C256 354 257 372 257 388 C258 400 263 412 269 423 C274 434 279 444 280 453 C281 461 279 466 275 467 C278 462 277 452 273 442 C268 430 262 418 259 404 C255 386 248 366 242 348 C236 330 230 312 226 294 C222 274 218 254 216 236 C214 212 218 190 218 172 C218 154 216 140 208 134 Z',
    ],
  },
  {
    id: 'kaki',
    label: 'Tungkai',
    desc: 'Ekstremitas bawah: paha, lutut, tungkai bawah, dan kaki.',
    items: ['Femur', 'Patela (tempurung lutut)', 'Tibia & fibula', 'Tarsal, metatarsal, falang', 'Otot kuadrisep & betis'],
    tint: `fill-teal-400/25 stroke-teal-200 ${filled}`,
    d: [
      // kaki kiri
      'M105 380 C103 404 103 428 103 452 C103 482 101 512 100 538 C99 560 98 580 102 592 C105 602 113 604 119 600 C124 597 124 590 122 580 C119 562 118 540 118 516 C118 490 120 462 122 436 C124 412 126 395 131 384 C133 376 130 372 124 372 C117 373 110 376 105 380 Z',
      // kaki kanan
      'M195 380 C197 404 197 428 197 452 C197 482 199 512 200 538 C201 560 202 580 198 592 C195 602 187 604 181 600 C176 597 176 590 178 580 C181 562 182 540 182 516 C182 490 180 462 178 436 C176 412 174 395 169 384 C167 376 170 372 176 372 C183 373 190 376 195 380 Z',
      // patela
      'M110 382 C117 378 126 378 132 382 C125 388 116 388 110 382 Z M190 382 C183 378 174 378 168 382 C175 388 184 388 190 382 Z',
    ],
  },
]
</script>
