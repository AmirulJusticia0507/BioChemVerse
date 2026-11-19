<script setup>
import { onMounted, onBeforeUnmount, ref, computed, watch } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

// Data molekul sederhana: nama -> struktur atom + ikatan
const molecules = {
  water: {
    id: 'water',
    title: 'Water (H₂O)',
    formula: 'H₂O',
    atoms: [
      { id: 'o1', element: 'O', color: 0xff0000, position: [0, 0, 0] },
      { id: 'h1', element: 'H', color: 0xffffff, position: [-0.75, 0, 0.5] },
      { id: 'h2', element: 'H', color: 0xffffff, position: [0.75, 0, 0.5] },
    ],
    bonds: [
      { from: 'o1', to: 'h1', type: 'single' },
      { from: 'o1', to: 'h2', type: 'single' },
    ],
  },
  methane: {
    id: 'methane',
    title: 'Methane (CH₄)',
    formula: 'CH₄',
    atoms: [
      { id: 'c1', element: 'C', color: 0x8b4513, position: [0, 0, 0] },
      { id: 'h1', element: 'H', color: 0xffffff, position: [0.6, 0, 1.1] },
      { id: 'h2', element: 'H', color: 0xffffff, position: [-0.6, 0, 1.1] },
      { id: 'h3', element: 'H', color: 0xffffff, position: [0, 0.8, -0.7] },
      { id: 'h4', element: 'H', color: 0xffffff, position: [0, -0.8, -0.7] },
    ],
    bonds: [
      { from: 'c1', to: 'h1', type: 'single' },
      { from: 'c1', to: 'h2', type: 'single' },
      { from: 'c1', to: 'h3', type: 'single' },
      { from: 'c1', to: 'h4', type: 'single' },
    ],
  },
  co2: {
    id: 'co2',
    title: 'Carbon Dioxide (CO₂)',
    formula: 'CO₂',
    atoms: [
      { id: 'c1', element: 'C', color: 0x8b4513, position: [0, 0, 0] },
      { id: 'o1', element: 'O', color: 0xff0000, position: [-0.6, 0, 1.15] },
      { id: 'o2', element: 'O', color: 0xff0000, position: [0.6, 0, 1.15] },
    ],
    bonds: [
      { from: 'c1', to: 'o1', type: 'double' },
      { from: 'c1', to: 'o2', type: 'double' },
    ],
  },
  // Pilihan default
  selectedMolecule: 'water',
}

// State Three.js
let renderer
let scene
let camera
let controls

// State interaksi
const selectedAtom = ref(null)
const raycaster = new THREE.Raycaster()
const mouse = new THREE.Vector2()

// Element colors
const elementColors = {
  H: 0xffffff,
  He: 0xd9ffff,
  Li: 0xcc77ff,
  Be: 0x9966cc,
  B: 0xffcc33,
  C: 0x8b4513,
  N: 0x00ffff,
  O: 0xff0000,
  F: 0xff99ff,
  Ne: 0x99ffff,
}

const atomSizes = {
  H: 0.5,
  C: 0.8,
  N: 0.7,
  O: 0.7,
  default: 0.6,
}

// Konstruksi atom
const atoms = computed(() => {
  const mol = molecules[selectedMolecule.value]
  return mol.atoms.map((a) => ({
    id: a.id,
    element: a.element,
    color: a.color,
    position: new THREE.Vector3(...a.position),
    size: atomSizes[a.element] || atomSizes.default,
    mesh: null, // akan dibangun setelah renderer siap
  }))
})

// Konstruksi ikatan
const bonds = computed(() => {
  const mol = molecules[selectedMolecule.value]
  const lines = []
  mol.bonds.forEach((b) => {
    const from = atoms.value.find((a) => a.id === b.from)
    const to = atoms.value.find((a) => a.id === b.to)
    if (from && to) {
      lines.push({
        from,
        to,
        type: b.type,
      })
    }
  })
  return lines
})

// Event mouse
function onPointerDown(event) {
  mouse.set(
    (event.clientX / window.innerWidth) * 2 - 1,
    -(event.clientY / window.innerHeight) * 2 + 1
  )
  raycaster.setFromCamera(mouse, camera)
  const intersects = raycaster.intersectObjects(
    atoms.value.map((a) => a.mesh)
  )
  if (intersects.length > 0) {
    selectedAtom.value = intersects[0].object
  } else {
    selectedAtom.value = null
  }
}

function onPointerMove(event) {
  if (!selectedAtom.value) return
  mouse.set(
    (event.clientX / window.innerWidth) * 2 - 1,
    -(event.clientY / window.innerHeight) * 2 + 1
  )
  raycaster.setFromCamera(mouse, camera)
  const planeY = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0)
  const intersect = new THREE.Vector3()
  if (raycaster.ray.intersectPlane(planeY, intersect)) {
    selectedAtom.position.set(intersect.x, selectedAtom.position.y, intersect.z)
  }
}

function onPointerUp() {
  selectedAtom.value = null
}

// Life cycle
onMounted(() => {
  const canvas = document.getElementById('molecule-canvas')
  if (!canvas) return

  // Scene
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x0f172a)

  // Camera
  camera = new THREE.PerspectiveCamera(45, canvas.clientWidth / canvas.clientHeight, 0.1, 100)
  camera.position.set(0, 1, 2)

  // Renderer
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true })
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.setSize(canvas.clientWidth, canvas.clientHeight)

  // Lights
  const hemi = new THREE.HemisphereLight(0xc7d2fe, 0x0f172a, 2.5)
  scene.add(hemi)
  const keyLight = new THREE.DirectionalLight(0xffffff, 3.5)
  keyLight.position.set(4, 6, 6)
  scene.add(keyLight)
  const fillLight = new THREE.DirectionalLight(0xffffff, 1.5)
  fillLight.position.set(-4, -6, -6)
  scene.add(fillLight)

  // Controls
  controls = new OrbitControls(camera, renderer.domElement)
  controls.target.set(0, 0, 0)
  controls.enablePan = false
  controls.minDistance = 1
  controls.maxDistance = 5

  // Bangun atom
  buildAtoms()

  // Loop render
  const render = () => {
    controls.update()
    renderer.render(scene, camera)
    requestAnimationFrame(render)
  }
  render()

  // Event listener
  canvas.addEventListener('pointerdown', onPointerDown)
  canvas.addEventListener('pointermove', onPointerMove)
  canvas.addEventListener('pointerup', onPointerUp)

  // Resize
  window.addEventListener('resize', () => {
    camera.aspect = canvas.clientWidth / canvas.clientHeight
    camera.updateProjectionMatrix()
    renderer.setSize(canvas.clientWidth, canvas.clientHeight)
  })
})

onBeforeUnmount(() => {
  if (renderer) renderer.dispose()
  if (canvas) canvas.removeEventListener('pointerdown', onPointerDown)
  if (canvas) canvas.removeEventListener('pointermove', onPointerMove)
  if (canvas) canvas.removeEventListener('pointerup', onPointerUp)
  window.removeEventListener('resize', () => {})
})

// Watch molecule change
watch(selectedMolecule, (newId) => {
  // Reset atom positions when switching molecules
  buildAtoms()
})

// Bangun atom ke mesh
function buildAtoms() {
  const mol = molecules[selectedMolecule.value]
  if (!mol || !renderer) return

  // Hapus mesh lama
  atoms.value.forEach((a) => {
    if (a.mesh && a.mesh.parent) {
      a.mesh.parent.remove(a.mesh)
    }
  })

  // Buat atom baru
  atoms.value = mol.atoms.map((a) => ({
    id: a.id,
    element: a.element,
    color: a.color,
    position: new THREE.Vector3(...a.position),
    size: atomSizes[a.element] || atomSizes.default,
    mesh: null,
  }))

  // Buat sphere untuk setiap atom
  atoms.value.forEach((atom) => {
    const geometry = new THREE.SphereGeometry(atom.size, 32, 32)
    const material = new THREE.MeshStandardMaterial({
      color: atom.color,
      roughness: 0.7,
    })
    atom.mesh = new THREE.Mesh(geometry, material)
    atom.mesh.position.copy(atom.position)
    scene.add(atom.mesh)
  })

  // Tambahkan ikatan (garis)
  bonds.value.forEach((bond) => {
    const from = atoms.value.find((a) => a.id === bond.from)
    const to = atoms.value.find((a) => a.id === bond.to)
    if (from && to) {
      const geometry = new THREE.CylinderGeometry(
        0.05,
        0.05,
        from.position.distanceTo(to.position),
        8
      )
      const material = new THREE.MeshStandardMaterial({ color: 0x7f8c8d })
      const cylinder = new THREE.Mesh(geometry, material)
      // Posisikan di tengah dan rotasi ke titik tujuan
      const mid = new THREE.Vector3()
      mid.addVectors(from.position, to.position).multiplyScalar(0.5)
      cylinder.position.copy(mid)
      // Rotasi ke titik tujuan
      const direction = new THREE.Vector3()
      direction.subVectors(to.position, from.position)
      cylinder.rotation.z = Math.atan2(direction.x, direction.z)
      cylinder.rotation.x = Math.atan2(direction.y, Math.sqrt(direction.x ** 2 + direction.z ** 2))
      scene.add(cylinder)
    }
  })
}
</script>

<template>
<div class="relative h-[500px] w-full rounded-2xl border border-slate-700 bg-slate-950 overflow-hidden">
  <div id="molecule-canvas" class="block w-full h-full"></div>

  <!-- Panel kontrol -->
  <div class="absolute top-3 left-3 right-3 flex flex-col gap-2">
    <h3 class="text-xs font-medium text-slate-300 uppercase tracking-wider">Molekul</h3>
    <div class="flex gap-2">
      <button
        v-for "(mId, mTitle) in moleculeOptions"
        :key="mId"
        type="button"
        class="rounded-md px-2.5 py-1.5 text-xs font-medium transition-colors focus:ring-2 focus:ring-blue-500/50 focus:outline-none"
        :class="selectedMolecule === mId ? 'bg-blue-500 text-white' : 'text-slate-300 hover:bg-slate-700'"
        @click="selectedMolecule = mId"
      >
        {{ mTitle }}
      </button>
    </div>
  </div>
</div>

<template #moleculeOptions>
  <template v-for="id in Object.keys(molecules)" :key="id">
    <button type="button" class="rounded-md px-2.5 py-1.5 text-xs font-medium transition-colors focus:ring-2 focus:ring-blue-500/50 focus:outline-none">
      {{ molecules[id].title }}
    </button>
  </template>