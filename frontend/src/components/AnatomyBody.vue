<template>
  <div class="flex flex-col items-center">
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-[300px_minmax(0,260px)] lg:items-start">
      <!-- Ilustrasi anatomi: siluet tubuh laki-laki + organ dalam -->
      <svg
        viewBox="0 0 300 620"
        role="img"
        aria-label="Ilustrasi anatomi tubuh manusia laki-laki beserta organ dalam"
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
          <path :d="bodyPath" fill="url(#skinFill)" stroke="currentColor" stroke-width="1.3" />
          <!-- celana pendek -->
          <path :d="shortsPath" fill="url(#clothFill)" stroke="currentColor" stroke-width="1.2" />
          <!-- telinga -->
          <path d="M124 44 C120 42 118 48 119 54 C120 60 122 63 125 62 Z" fill="url(#skinFill)" stroke="currentColor" stroke-width="1.1" />
          <path d="M176 44 C180 42 182 48 181 54 C180 60 178 63 175 62 Z" fill="url(#skinFill)" stroke="currentColor" stroke-width="1.1" />
          <!-- lekuk otot & permukaan -->
          <g fill="none" stroke="currentColor" stroke-width="0.9" opacity="0.55">
            <path d="M123 120 C133 127 167 127 177 120" />
            <path d="M137 134 C141 147 141 162 138 174" />
            <path d="M163 134 C159 147 159 162 162 174" />
            <path d="M150 196 V236" opacity="0.4" />
            <path d="M150 254 V304" opacity="0.4" />
            <path d="M124 228 C118 250 116 272 118 292" opacity="0.35" />
            <path d="M176 228 C182 250 184 272 182 292" opacity="0.35" />
            <path d="M118 430 C114 452 114 474 116 496" />
            <path d="M182 430 C186 452 186 474 184 496" />
            <path d="M113 392 C120 389 130 389 137 392 M163 392 C170 389 180 389 187 392" />
            <path d="M57 206 C54 230 51 252 49 272" opacity="0.45" />
            <path d="M243 206 C246 230 249 252 251 272" opacity="0.45" />
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
            <path v-for="(d, i) in region.d" :key="i" :d="d" />
            <circle v-for="(c, i) in region.dots ?? []" :key="'c' + i" :cx="c[0]" :cy="c[1]" :r="c[2]" />
          </g>
        </g>
      </svg>

      <!-- Panel keterangan -->
      <aside class="w-full rounded-xl bg-slate-800 p-5 ring-1 ring-slate-700 lg:sticky lg:top-6">
        <p class="text-sm text-slate-400">{{ selected ? 'Bagian dipilih' : 'Klik bagian tubuh' }}</p>
        <h2 class="mt-1 text-lg font-semibold text-white">{{ selectedInfo?.label ?? 'Anatomi manusia' }}</h2>
        <p class="mt-2 text-sm text-slate-300">
          {{ selectedInfo?.desc ?? 'Pilih organ atau bagian tubuh pada ilustrasi untuk melihat keterangannya.' }}
        </p>
        <ul v-if="selectedInfo?.items" class="mt-4 space-y-1.5 text-sm text-slate-300">
          <li v-for="item in selectedInfo.items" :key="item" class="flex gap-2">
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
import { computed, ref } from 'vue'

const selected = ref(null)
const selectedInfo = computed(() => regions.find((r) => r.id === selected.value) ?? null)

// Bagian luar (lengan, kaki, tulang, panggul) digambar lebih dulu; organ dalam digambar terakhir
// supaya dapat diklik di area yang bertumpang tindih (mis. jantung di depan kolumna).
const drawnLast = ['kepala', 'leher', 'dada', 'jantung', 'hati', 'lambung', 'usus', 'ginjal']
const orderedRegions = computed(() => [
  ...regions.filter((r) => !drawnLast.includes(r.id)),
  ...regions.filter((r) => drawnLast.includes(r.id)),
])

const select = (id) => (selected.value = selected.value === id ? null : id)

const regionClass = (region) =>
  selected.value === region.id ? 'fill-blue-500/60 stroke-blue-100' : region.tint

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
    id: 'panggul',
    label: 'Panggul & Perkemihan',
    desc: 'Gelang panggul menopang saluran kemih dan organ reproduksi.',
    items: ['Os coxae (ilium, iskium, pubis)', 'Kandung kemih', 'Ureter & uretra', 'Organ reproduksi pria'],
    tint: `fill-teal-400/50 stroke-teal-200 ${filled}`,
    d: [
      // kandung kemih
      'M143 334 C149 329 156 329 158 336 C160 345 155 351 150 351 C144 351 140 345 142 339 Z',
      // garis panggul (ilium)
      'M118 330 C128 320 142 320 148 328 M182 330 C172 320 158 320 152 328 M114 348 C120 340 128 336 134 336 M186 348 C180 340 172 336 166 336',
    ],
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
