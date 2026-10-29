<template>
  <div class="relative overflow-hidden rounded-2xl border border-slate-700 bg-slate-950">
    <canvas ref="canvas" class="block aspect-4/3 w-full touch-none" aria-hidden="true" />
    <div class="pointer-events-none absolute inset-x-0 top-0 flex items-start justify-between gap-2 p-3">
      <span
        class="pointer-events-auto rounded-full bg-slate-900/80 px-2.5 py-1 text-[11px] text-slate-300 ring-1 ring-slate-700"
      >
        Drag untuk memutar · Scroll untuk zoom
      </span>
      <div class="pointer-events-auto flex gap-1.5">
        <button
          v-for="action in actions"
          :key="action.id"
          type="button"
          class="rounded-lg bg-slate-900/80 px-2.5 py-1 text-[11px] font-medium text-slate-200 ring-1 ring-slate-700 hover:bg-slate-800 focus:ring-2 focus:ring-blue-500/60 focus:outline-none"
          @click="runAction(action.id)"
        >
          {{ action.label }}
        </button>
      </div>
    </div>
    <p v-if="error" class="absolute inset-0 flex items-center justify-center p-6 text-center text-sm text-slate-400">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { buildSurgeryScene } from '../../three/surgeryScenes.js'

const props = defineProps({
  preset: { type: Object, required: true },
})

const canvas = ref(null)
const error = ref('')

const actions = [
  { id: 'reset', label: 'Reset kamera' },
  { id: 'rotate', label: 'Putar otomatis' },
]

let renderer
let scene
let camera
let controls
let frame
let observer
let autoRotate = false

const frameCamera = () => {
  const { position, target } = props.preset.camera
  camera.position.set(...position)
  controls.target.set(...target)
  controls.update()
}

const resize = () => {
  const { clientWidth: width, clientHeight: height } = canvas.value
  if (!width || !height) return
  renderer.setSize(width, height, false)
  camera.aspect = width / height
  camera.updateProjectionMatrix()
}

const runAction = (id) => {
  if (id === 'reset') {
    frameCamera()
    return
  }
  autoRotate = !autoRotate
  if (controls) controls.autoRotate = autoRotate
}

onMounted(() => {
  try {
    renderer = new THREE.WebGLRenderer({ canvas: canvas.value, antialias: true, alpha: false })
  } catch {
    error.value = 'Browser ini tidak mendukung WebGL, sehingga model 3D tidak dapat ditampilkan.'
    return
  }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.setClearColor(0x05070d, 1)
  renderer.toneMapping = THREE.ACESFilmicToneMapping
  renderer.toneMappingExposure = 1.1

  camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100)
  controls = new OrbitControls(camera, canvas.value)
  controls.enableDamping = true
  controls.dampingFactor = 0.08
  controls.minDistance = 2.2
  controls.maxDistance = 11
  controls.maxPolarAngle = Math.PI * 0.82
  controls.autoRotateSpeed = 0.9

  applyPreset()
  applyPreset()
  scene = buildSurgeryScene(props.preset).scene
  frameCamera()
  observer = new ResizeObserver(resize)
  observer.observe(canvas.value)
  resize()

  const loop = () => {
    controls.update()
    if (scene && camera) renderer.render(scene, camera)
    frame = requestAnimationFrame(loop)
  }
  loop()
})

watch(
  () => props.preset,
  (next) => {
    if (!next || !renderer) return
    autoRotate = false
    if (controls) controls.autoRotate = false
    const built = buildSurgeryScene(next)
    scene = built.scene
    frameCamera()
  },
  { deep: true },
)

onBeforeUnmount(() => {
  cancelAnimationFrame(frame)
  observer?.disconnect()
  controls?.dispose()
  renderer?.dispose()
})
</script>
