// Mesin stoikiometri (adaptasi dari ChemSphere `utils/stoichiometry.js`):
// mengurai persamaan reaksi, menyetarakan koefisien dengan aljabar linear,
// serta menghitung massa molar dan konversi mol.
//
// Semua perhitungan murni (tanpa efek samping) supaya bisa diuji langsung.

import { parseFormula, prettyFormula } from './formula.js'

/** Mengurai satu sisi persamaan menjadi daftar spesies. */
export function parseSide(text) {
  return String(text)
    .split('+')
    .map((part) => part.trim())
    .filter(Boolean)
    .map((part) => {
      const match = /^(\d*)\s*(.+)$/.exec(part)
      if (!match) return null
      const coefficient = match[1] ? Number(match[1]) : 1
      const formula = match[2].replace(/\s+/g, '')
      return { coefficient, formula }
    })
    .filter(Boolean)
}

/** Memisahkan persamaan "A + B -> C + D" menjadi dua sisi. */
export function parseEquation(equation) {
  const normalized = String(equation)
    .replace(/[→⟶]/g, '->')
    .replace(/⇌/g, '->')
    .replace(/=/g, '->')

  const parts = normalized.split('->')
  if (parts.length !== 2) {
    return { error: 'Persamaan harus berisi tepat satu tanda panah (->).' }
  }

  const left = parseSide(parts[0])
  const right = parseSide(parts[1])

  if (!left.length || !right.length) {
    return { error: 'Kedua sisi persamaan harus berisi setidaknya satu senyawa.' }
  }

  return { left, right }
}

function gcd(a, b) {
  let x = Math.abs(a)
  let y = Math.abs(b)
  while (y) {
    const t = y
    y = x % y
    x = t
  }
  return x || 1
}

function lcm(a, b) {
  return Math.abs(a * b) / gcd(a, b)
}

/** Menyelesaikan sistem homogen A·x = 0 dengan eliminasi Gauss-Jordan. */
function solveHomogeneous(matrix, columns) {
  const rows = matrix.length
  const augmented = matrix.map((row) => row.map((value) => Number(value)))

  let pivotRow = 0
  const pivotColumns = []

  for (let col = 0; col < columns && pivotRow < rows; col += 1) {
    let best = pivotRow
    for (let row = pivotRow + 1; row < rows; row += 1) {
      if (Math.abs(augmented[row][col]) > Math.abs(augmented[best][col])) best = row
    }
    if (Math.abs(augmented[best][col]) < 1e-12) continue

    const temp = augmented[pivotRow]
    augmented[pivotRow] = augmented[best]
    augmented[best] = temp

    const pivot = augmented[pivotRow][col]
    for (let c = 0; c < columns; c += 1) augmented[pivotRow][c] /= pivot

    for (let row = 0; row < rows; row += 1) {
      if (row === pivotRow) continue
      const factor = augmented[row][col]
      if (Math.abs(factor) < 1e-12) continue
      for (let c = 0; c < columns; c += 1) {
        augmented[row][c] -= factor * augmented[pivotRow][c]
      }
    }

    pivotColumns.push(col)
    pivotRow += 1
  }

  const freeColumns = []
  for (let col = 0; col < columns; col += 1) {
    if (!pivotColumns.includes(col)) freeColumns.push(col)
  }

  // Persamaan reaksi punya satu derajat kebebasan (skala).
  if (freeColumns.length !== 1) return null

  const free = freeColumns[0]
  const solution = new Array(columns).fill(0)
  solution[free] = 1

  pivotColumns.forEach((col, index) => {
    solution[col] = -augmented[index][free]
  })

  return solution
}

/** Mengubah vektor pecahan menjadi bilangan bulat positif terkecil. */
function toIntegers(vector) {
  const EPSILON = 1e-9
  const denominators = []

  for (const value of vector) {
    if (Math.abs(value) < EPSILON) continue
    let found = 1
    for (let d = 1; d <= 720; d += 1) {
      if (Math.abs(value * d - Math.round(value * d)) < 1e-6) {
        found = d
        break
      }
    }
    denominators.push(found)
  }

  if (!denominators.length) return null

  const commonDenominator = denominators.reduce((acc, d) => lcm(acc, d), 1)
  let integers = vector.map((value) => Math.round(value * commonDenominator))

  const divisor = integers.reduce((acc, value) => gcd(acc, value), 0) || 1
  integers = integers.map((value) => value / divisor)

  if (integers.some((value) => value <= 0)) return null
  return integers
}

/**
 * Menyetarakan persamaan reaksi.
 *
 * @param {string} equation contoh "Fe2O3 + CO -> Fe + CO2"
 * @returns {{ok: boolean, error?: string, coefficients?: number[], left?: object[], right?: object[], balanced?: string}}
 */
export function balanceEquation(equation) {
  const parsed = parseEquation(equation)
  if (parsed.error) return { ok: false, error: parsed.error }

  const { left, right } = parsed
  const species = [...left, ...right]

  const elementSet = new Set()
  const compositions = species.map((item) => {
    const counts = parseFormula(item.formula)
    for (const symbol of Object.keys(counts)) elementSet.add(symbol)
    return counts
  })

  if (!elementSet.size) {
    return { ok: false, error: 'Tidak ada unsur yang dapat dikenali pada persamaan.' }
  }

  const elements = [...elementSet]
  const matrix = elements.map((symbol) =>
    species.map((_, index) => {
      const count = compositions[index][symbol] ?? 0
      return index < left.length ? count : -count
    }),
  )

  const solution = solveHomogeneous(matrix, species.length)
  if (!solution) {
    return {
      ok: false,
      error: 'Persamaan ini tidak dapat disetarakan. Periksa kembali rumus senyawanya.',
    }
  }

  const coefficients = toIntegers(solution)
  if (!coefficients) {
    return {
      ok: false,
      error: 'Persamaan ini tidak dapat disetarakan dengan koefisien bulat positif.',
    }
  }

  const balancedLeft = left.map((item, index) => ({
    coefficient: coefficients[index],
    formula: item.formula,
  }))
  const balancedRight = right.map((item, index) => ({
    coefficient: coefficients[left.length + index],
    formula: item.formula,
  }))

  const render = (list) =>
    list
      .map(
        (item) =>
          `${item.coefficient === 1 ? '' : item.coefficient}${prettyFormula(item.formula)}`,
      )
      .join(' + ')

  return {
    ok: true,
    coefficients,
    left: balancedLeft,
    right: balancedRight,
    balanced: `${render(balancedLeft)} → ${render(balancedRight)}`,
  }
}

/**
 * Massa molar dari rumus. `massOf` mengembalikan massa atom per simbol.
 *
 * @returns {{total: number, missing: string[], breakdown: object[]}}
 */
export function molarMassOf(formula, massOf) {
  const counts = parseFormula(formula)
  let total = 0
  const missing = []
  const breakdown = []

  for (const [symbol, count] of Object.entries(counts)) {
    const mass = massOf(symbol)
    if (!mass) {
      missing.push(symbol)
      continue
    }
    total += mass * count
    breakdown.push({ symbol, count, mass, subtotal: mass * count })
  }

  return { total, missing, breakdown }
}

// --- Konversi mol -----------------------------------------------------------

export const AVOGADRO = 6.02214076e23

export function molesFromMass(massGram, molarMass) {
  if (!molarMass || molarMass <= 0) return null
  return massGram / molarMass
}

export function massFromMoles(moles, molarMass) {
  if (!molarMass || molarMass <= 0) return null
  return moles * molarMass
}

export function particlesFromMoles(moles) {
  return moles * AVOGADRO
}

export function molesFromParticles(particles) {
  return particles / AVOGADRO
}

// Volume gas ideal pada kondisi standar (STP: 0 °C, 1 atm = 22,414 L/mol).
export const MOLAR_VOLUME_STP = 22.414

export function volumeFromMoles(moles, molarVolume = MOLAR_VOLUME_STP) {
  return moles * molarVolume
}

// --- Larutan ---------------------------------------------------------------

export function molarity(moles, volumeLiter) {
  if (!volumeLiter || volumeLiter <= 0) return null
  return moles / volumeLiter
}

/** M1·V1 = M2·V2 — isi tepat tiga nilai, satu dihitung. */
export function dilution({ m1, v1, m2, v2 }) {
  const known = [m1, v1, m2, v2].filter(
    (value) => value !== null && value !== undefined && value !== '',
  )
  if (known.length !== 3) {
    return { error: 'Isi tepat tiga nilai; satu nilai akan dihitung.' }
  }
  if (m1 === null || m1 === undefined || m1 === '') return { value: (m2 * v2) / v1, solvedFor: 'M1' }
  if (v1 === null || v1 === undefined || v1 === '') return { value: (m2 * v2) / m1, solvedFor: 'V1' }
  if (m2 === null || m2 === undefined || m2 === '') return { value: (m1 * v1) / v2, solvedFor: 'M2' }
  return { value: (m1 * v1) / m2, solvedFor: 'V2' }
}
