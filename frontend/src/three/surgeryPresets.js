// Preset scene 3D tiap prosedur. Koordinat: x = kanan pasien, y = kranial, z = anterior (dm).
// Port adalah titik masuk instrumen; posisinya mengikuti tata letak laparoskopi standar.
// Kamera diposisikan miring ke dalam rongga perut (seperti sudut laparoskop sebenarnya).

const trocar = (position, rotation = [0, 0, 0], length = 1.9) => ({ kind: 'trocar', position, rotation, length })
const scopePort = (position, rotation = [0, 0, 0]) => ({ kind: 'scope', position, rotation })

export const surgeryScenes = {
  // 4 trokar standar: umbilikus (kamera), epigastrium (kerja), kanan & kiri bawah (traksi).
  laparoskopi: {
    organs: ['liver', 'stomach', 'bowel', 'fascia'],
    ports: [
      scopePort([0, -0.6, 2.0], [0.35, 0, 0]),
      trocar([0.1, 1.3, 1.9], [-0.6, 0, 0]),
      trocar([-1.9, -0.7, 1.4], [0, 0.7, 0.35], 1.7),
      trocar([1.9, -0.7, 1.4], [0, -0.7, -0.35], 1.7),
    ],
    instruments: [
      { position: [0.55, 1.75, 1.7], rotation: [-0.75, 0, 0.1], color: 0xa5b4fc, tip: 'grasper' },
    ],
    camera: { position: [2.6, 2.2, 5.4], target: [0, -0.35, 0.3] },
  },

  // Apendektomi laparoskopi: apendiks di kuadran kanan bawah; kamera umbilikus,
  // grasper suprapubik & kiri untuk mengangkat apendiks, hook elektrokauter di kanan.
  apendektomi: {
    organs: ['bowel', 'appendix', 'fascia'],
    ports: [
      scopePort([0, -0.3, 2.0], [0.35, 0, 0]),
      trocar([-1.0, -1.9, 1.75], [-0.7, 0, -0.15], 1.7),
      trocar([1.5, -1.7, 1.8], [-0.65, 0, 0.3], 1.7),
    ],
    instruments: [
      { position: [-0.5, -0.95, 1.35], rotation: [0.15, 0, -0.35], color: 0xa5b4fc, tip: 'grasper' },
      { position: [0.5, -1.3, 1.5], rotation: [0.05, 0, 0.45], color: 0xfca5a5, tip: 'hook' },
    ],
    camera: { position: [2.1, 1.3, 4.9], target: [0.1, -1.0, 0.5] },
  },

  // Kolesistektomi: kandung empedu di bawah hati, diekspos dengan traksi fundus ke kranial.
  kolesistektomi: {
    organs: ['liver', 'gallbladder', 'bowel', 'fascia'],
    ports: [
      scopePort([0, -0.5, 2.0], [0.35, 0, 0]),
      trocar([0.1, 1.6, 1.95], [-0.65, 0, 0]),
      trocar([1.9, 0.2, 1.55], [0, -0.6, 0.3], 1.7),
      trocar([-1.9, -0.6, 1.5], [0, 0.6, -0.3], 1.7),
    ],
    instruments: [
      { position: [1.2, 2.0, 1.6], rotation: [0.05, 0, 0.45], color: 0xa5b4fc, tip: 'grasper' },
      { position: [0.7, 1.45, 1.75], rotation: [-0.5, 0, 0.15], color: 0xfde68a, tip: 'hook' },
    ],
    camera: { position: [0.6, 2.4, 4.6], target: [0.35, 0.9, 0.8] },
  },

  // Herniorafi: mesh polipropilen ditempatkan di defek kanalis inguinalis.
  herniorafi: {
    organs: ['bowel', 'mesh'],
    ports: [],
    instruments: [
      { position: [-2.1, -1.3, 1.7], rotation: [0.15, 0.4, 0.6], color: 0xa5b4fc, tip: 'grasper' },
      { position: [-0.3, -2.2, 1.9], rotation: [-0.7, 0, -0.2], color: 0x93c5fd, tip: 'hook' },
    ],
    camera: { position: [-2.4, 0.2, 4.6], target: [-1.0, -0.8, 1.0] },
  },

  // Seksio sesarea: insisi Pfannenstiel transversal di atas simfisis, uterus gravid terlihat.
  seksio: {
    organs: ['uterus', 'bowel'],
    ports: [
      trocar([-2.0, 1.2, 1.6], [0, 0, -1.1], 1.4),
      trocar([2.0, 1.2, 1.6], [0, 0, 1.1], 1.4),
    ],
    instruments: [
      { position: [0.2, 1.1, 2.2], rotation: [-0.75, 0, 0], color: 0xe2e8f0, tip: 'hook' },
      { position: [1.5, 0.5, 1.9], rotation: [0, 0, 0.5], color: 0x93c5fd, tip: 'grasper' },
    ],
    camera: { position: [0, 1.0, 6.2], target: [0, -0.3, 0.6] },
  },
}

export const getSurgeryScene = (id) => surgeryScenes[id] ?? surgeryScenes.laparoskopi
