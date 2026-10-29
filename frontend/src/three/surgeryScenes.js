import * as THREE from 'three'

// Scene bedah 3D dibangun dari geometri Three.js — tanpa aset berlisensi pihak ketiga.
// Koordinat: x = kanan pasien, y = kranial (atas), z = anterior (depan) — dipakai dalam satuan "dm".

const glow = (color, intensity = 1.2, distance = 3.2) =>
  new THREE.PointLight(color, intensity, distance, 2)

const skin = () =>
  new THREE.MeshPhysicalMaterial({
    color: 0xc0856a,
    roughness: 0.66,
    metalness: 0,
    clearcoat: 0.18,
    clearcoatRoughness: 0.6,
    side: THREE.DoubleSide,
  })

const organMat = (color, roughness = 0.55) =>
  new THREE.MeshStandardMaterial({ color, roughness, metalness: 0.02 })

// Dinding perut: kubah terbuka (setengah bola) bagian depan dipotong supaya isi perut terlihat.
const abdomen = () => {
  const group = new THREE.Group()
  const shell = new THREE.Mesh(
    new THREE.SphereGeometry(2.9, 72, 48, 0, Math.PI * 2, 0, Math.PI * 0.78),
    skin(),
  )
  shell.scale.set(1.32, 1.0, 0.9)
  shell.rotation.x = Math.PI * 0.52
  shell.position.y = 0.6
  group.add(shell)

  // Garis tepi dinding (incision edge) supaya kubah terbaca sebagai rongga terbuka.
  const rim = new THREE.Mesh(
    new THREE.TorusGeometry(2.9, 0.045, 10, 96),
    new THREE.MeshStandardMaterial({ color: 0xd9a08a, roughness: 0.7 }),
  )
  rim.rotation.x = Math.PI / 2
  rim.position.y = -0.15
  rim.scale.set(1.32, 0.9, 1)
  group.add(rim)
  return group
}

// Cavity dengan dasar gelap supaya organ yang lebih dalam terbaca.
const cavity = () => {
  const group = new THREE.Group()
  const floor = new THREE.Mesh(
    new THREE.SphereGeometry(2.86, 56, 36, 0, Math.PI * 2, Math.PI * 0.5, Math.PI * 0.5),
    new THREE.MeshStandardMaterial({ color: 0x3b1218, roughness: 0.95, side: THREE.BackSide }),
  )
  floor.position.y = 0.6
  floor.scale.set(1.3, 1, 0.88)
  group.add(floor)
  return group
}

const liver = () => {
  const group = new THREE.Group()
  const mat = organMat(0x7f2d24, 0.48)
  const right = new THREE.Mesh(new THREE.SphereGeometry(1.45, 48, 32), mat)
  right.scale.set(1.35, 0.72, 0.6)
  right.position.set(0.86, 1.25, 0.62)
  const left = new THREE.Mesh(new THREE.SphereGeometry(0.98, 40, 26), mat)
  left.scale.set(1.25, 0.6, 0.55)
  left.position.set(-0.72, 1.12, 0.6)
  left.rotation.z = 0.22
  group.add(right, left)
  return group
}

const gallbladder = () => {
  const group = new THREE.Group()
  const bile = new THREE.Mesh(
    new THREE.CapsuleGeometry(0.24, 0.72, 8, 20),
    new THREE.MeshPhysicalMaterial({ color: 0x1d6b3f, roughness: 0.32, clearcoat: 0.7 }),
  )
  bile.position.set(0.82, 0.56, 1.12)
  bile.rotation.z = -0.35
  group.add(bile)
  // duktus sistikus
  const duct = new THREE.Mesh(
    new THREE.CylinderGeometry(0.04, 0.045, 0.9, 10),
    new THREE.MeshStandardMaterial({ color: 0xd6c49a, roughness: 0.7 }),
  )
  duct.position.set(0.42, -0.12, 1.04)
  duct.rotation.z = 1.05
  group.add(duct)
  return group
}

const appendix = () => {
  const group = new THREE.Group()
  const mat = organMat(0xa8453a, 0.62)
  const curve = new THREE.CatmullRomCurve3([
    new THREE.Vector3(-1.0, -0.9, 0.1),
    new THREE.Vector3(-0.5, -1.2, 0.5),
    new THREE.Vector3(0.15, -1.05, 0.75),
    new THREE.Vector3(0.6, -0.55, 0.9),
  ])
  const tube = new THREE.Mesh(new THREE.TubeGeometry(curve, 48, 0.16, 16, false), mat)
  group.add(tube)
  // ujung terinflamasi (lebih merah & bengkak)
  const tip = new THREE.Mesh(new THREE.SphereGeometry(0.19, 20, 14), organMat(0xd1443a, 0.5))
  tip.position.set(0.6, -0.55, 0.9)
  group.add(tip)
  return group
}

const bowel = () => {
  const group = new THREE.Group()
  const mat = organMat(0xb0614f, 0.72)
  const loops = [
    [[-1.5, -1.6], [-0.9, -2.0], [0.15, -1.7], [1.1, -2.05], [1.6, -1.5]],
    [[1.5, -0.55], [0.8, -0.9], [-0.15, -0.62], [-1.15, -0.9], [-1.6, -0.45]],
  ]
  for (const loop of loops) {
    const curve = new THREE.CatmullRomCurve3(
      loop.map(([x, y], i) => new THREE.Vector3(x, y, 0.1 + (i % 2) * 0.16)),
    )
    group.add(new THREE.Mesh(new THREE.TubeGeometry(curve, 60, 0.19, 14, false), mat))
  }
  return group
}

const stomach = () => {
  const group = new THREE.Group()
  const body = new THREE.Mesh(
    new THREE.SphereGeometry(0.85, 36, 26),
    organMat(0xc26f6a, 0.6),
  )
  body.scale.set(0.85, 1.15, 0.55)
  body.position.set(-1.0, 0.32, 0.75)
  body.rotation.z = 0.3
  group.add(body)
  return group
}

const kidney = (side) => {
  const group = new THREE.Group()
  const mat = organMat(0x8f4747, 0.5)
  const bean = new THREE.Mesh(new THREE.SphereGeometry(0.33, 32, 22), mat)
  bean.scale.set(0.85, 1.35, 0.65)
  bean.position.set(side * 1.05, -0.15, -0.35)
  group.add(bean)
  const ureter = new THREE.Mesh(
    new THREE.CylinderGeometry(0.025, 0.025, 1.1, 8),
    new THREE.MeshStandardMaterial({ color: 0xdfd0a8, roughness: 0.7 }),
  )
  ureter.position.set(side * 0.9, -0.85, -0.25)
  group.add(ureter)
  return group
}

// Mesh / graft: jaring polipropilen untuk herniorafi.
const meshPatch = () => {
  const group = new THREE.Group()
  const mat = new THREE.MeshStandardMaterial({
    color: 0x9fd7ff, roughness: 0.35, metalness: 0.15, transparent: true, opacity: 0.55, wireframe: true,
  })
  const patch = new THREE.Mesh(new THREE.CircleGeometry(1.25, 28), mat)
  patch.position.set(-1.1, -0.9, 1.9)
  patch.rotation.set(-0.4, 0.15, 0)
  group.add(patch)
  // jahitan penutup defek (tiga benang horizontal)
  const sutureMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.6 })
  for (let i = 0; i < 3; i += 1) {
    const thread = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.9, 8), sutureMat)
    thread.position.set(-1.1, -0.55 - i * 0.3, 2.0)
    thread.rotation.set(Math.PI / 2 - 0.35, 0, 0)
    group.add(thread)
  }
  return group
}

// Uterus gravid + bayi untuk seksio sesarea.
const uterusPregnant = () => {
  const group = new THREE.Group()
  const mat = organMat(0xb05a5a, 0.62)
  const uterus = new THREE.Mesh(new THREE.SphereGeometry(1.35, 48, 32), mat)
  uterus.scale.set(1, 0.95, 0.72)
  uterus.position.set(0, -0.55, 0.7)
  group.add(uterus)

  const baby = new THREE.Group()
  const babyMat = new THREE.MeshPhysicalMaterial({ color: 0xe8b8a4, roughness: 0.5, clearcoat: 0.3 })
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.42, 32, 22), babyMat)
  head.position.set(0, 0.36, 1.42)
  baby.add(head)
  const torso = new THREE.Mesh(new THREE.CapsuleGeometry(0.28, 0.42, 8, 18), babyMat)
  torso.position.set(0, -0.16, 1.34)
  torso.rotation.x = 0.4
  baby.add(torso)
  for (const side of [-1, 1]) {
    const limb = new THREE.Mesh(new THREE.CapsuleGeometry(0.095, 0.28, 6, 12), babyMat)
    limb.position.set(side * 0.28, -0.26, 1.5)
    limb.rotation.z = side * 0.5
    baby.add(limb)
  }
  group.add(baby)
  return group
}

// Trokar: tabung logam + keran gas, ujung masuk rongga perut.
const trocar = (position, rotation = [0, 0, 0], len = 1.5) => {
  const group = new THREE.Group()
  const shaft = new THREE.Mesh(
    new THREE.CylinderGeometry(0.085, 0.085, len, 18),
    new THREE.MeshStandardMaterial({ color: 0xcbd5e1, roughness: 0.22, metalness: 0.9 }),
  )
  group.add(shaft)
  const head = new THREE.Mesh(
    new THREE.CylinderGeometry(0.19, 0.19, 0.4, 20),
    new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.3, metalness: 0.8 }),
  )
  head.position.y = len / 2 + 0.2
  group.add(head)
  const valve = new THREE.Mesh(
    new THREE.CylinderGeometry(0.045, 0.045, 0.34, 12),
    new THREE.MeshStandardMaterial({ color: 0x38bdf8, roughness: 0.4, metalness: 0.5 }),
  )
  valve.rotation.z = Math.PI / 2
  valve.position.set(0.26, len / 2 + 0.2, 0)
  group.add(valve)
  group.position.set(...position)
  group.rotation.set(...rotation)
  return group
}

// Laparoskop: batang panjang dengan lensa bercahaya di ujung.
const scope = (position, rotation = [0, 0, 0]) => {
  const group = new THREE.Group()
  const body = new THREE.Mesh(
    new THREE.CylinderGeometry(0.095, 0.095, 2.6, 20),
    new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.2, metalness: 0.85 }),
  )
  group.add(body)
  const housing = new THREE.Mesh(
    new THREE.CylinderGeometry(0.26, 0.26, 0.4, 22),
    new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.5, metalness: 0.4 }),
  )
  housing.position.y = 1.55
  group.add(housing)
  const lens = new THREE.Mesh(
    new THREE.SphereGeometry(0.09, 16, 12),
    new THREE.MeshStandardMaterial({ color: 0xfef9c3, emissive: 0xfde68a, emissiveIntensity: 2.5 }),
  )
  lens.position.y = -1.3
  group.add(lens)
  const beam = glow(0xfde68a, 3, 4)
  beam.position.y = -1.5
  group.add(beam)
  group.position.set(...position)
  group.rotation.set(...rotation)
  return group
}

// Instrumen (grasper / hook) untuk diseksi.
const instrument = (position, rotation = [0, 0, 0], color = 0x93c5fd, tip = 'grasper') => {
  const group = new THREE.Group()
  const shaft = new THREE.Mesh(
    new THREE.CylinderGeometry(0.055, 0.055, 2.8, 14),
    new THREE.MeshStandardMaterial({ color, roughness: 0.28, metalness: 0.8 }),
  )
  group.add(shaft)
  const jawMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.35, metalness: 0.75 })
  if (tip === 'grasper') {
    for (const side of [-1, 1]) {
      const jaw = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.28, 0.12), jawMat)
      jaw.position.set(side * 0.07, -1.48, 0)
      jaw.rotation.z = side * 0.22
      group.add(jaw)
    }
  } else {
    const hook = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.03, 8, 20, Math.PI), jawMat)
    hook.position.y = -1.45
    hook.rotation.y = Math.PI / 2
    group.add(hook)
  }
  group.position.set(...position)
  group.rotation.set(...rotation)
  return group
}

// Jaringan ikat / adhesi tipis untuk memperlihatkan area diseksi.
const fascia = () => {
  const mat = new THREE.MeshStandardMaterial({
    color: 0xe8dcc6, roughness: 0.82, transparent: true, opacity: 0.42, side: THREE.DoubleSide,
  })
  const group = new THREE.Group()
  for (let i = 0; i < 7; i += 1) {
    const strand = new THREE.Mesh(new THREE.PlaneGeometry(0.75, 0.045), mat)
    strand.position.set(-0.75 + i * 0.22, 0.28 - i * 0.07, 1.45 - i * 0.05)
    strand.rotation.set(0.4, 0.6, i * 0.12)
    group.add(strand)
  }
  return group
}

const organLayer = (scene, id) => {
  switch (id) {
    case 'liver': return liver()
    case 'gallbladder': return gallbladder()
    case 'appendix': return appendix()
    case 'bowel': return bowel()
    case 'stomach': return stomach()
    case 'kidney': return new THREE.Group().add(kidney(-1), kidney(1))
    case 'mesh': return meshPatch()
    case 'uterus': return uterusPregnant()
    case 'fascia': return fascia()
    default: return new THREE.Group()
  }
}

/**
 * Bangun scene bedah lengkap.
 * @param {object} preset dari surgeryScenes di data/surgery.js
 */
export function buildSurgeryScene(preset) {
  const scene = new THREE.Scene()
  scene.add(new THREE.HemisphereLight(0xe0f2fe, 0x1b1013, 1.5))
  const key = new THREE.DirectionalLight(0xffffff, 2.6)
  key.position.set(4, 6, 6)
  scene.add(key)
  const fill = new THREE.DirectionalLight(0x93c5fd, 1.2)
  fill.position.set(-5, 1, 3)
  scene.add(fill)

  const root = new THREE.Group()
  scene.add(root)
  root.add(cavity(), abdomen())

  for (const id of preset.organs) root.add(organLayer(scene, id))

  for (const port of preset.ports) {
    root.add(port.kind === 'scope' ? scope(port.position, port.rotation) : trocar(port.position, port.rotation, port.length))
  }
  for (const tool of preset.instruments ?? []) {
    root.add(instrument(tool.position, tool.rotation, tool.color, tool.tip))
  }
  return { scene, root }
}

export { organMat }
