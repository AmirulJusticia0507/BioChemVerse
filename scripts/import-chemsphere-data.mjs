/**
 * Importer data ChemSphere → BioChemVerse.
 *
 * Mengekstrak literal data dari proyek ChemSphere (C:\laragon\www\ChemSphere,
 * backend/prisma/seed.mjs + element-properties.json) lalu menuliskan JSON
 * siap-seed ke backend/python/data/.
 *
 * Pemakaian:
 *   node scripts/import-chemsphere-data.mjs [path-ke-seed.mjs]
 */
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const SEED =
  process.argv[2] ?? 'C:/laragon/www/ChemSphere/backend/prisma/seed.mjs'
const OUT_DIR = path.join(
  path.dirname(fileURLToPath(import.meta.url)),
  '..',
  'backend',
  'python',
  'data',
)

const src = fs.readFileSync(SEED, 'utf8')

/** Ekstrak literal array/object bernama `const <name> = [...] / {...}` lalu eval sebagai literal JS. */
function grab(name) {
  const marker = `const ${name} = `
  const idx = src.indexOf(marker)
  if (idx < 0) throw new Error(`konstanta tidak ditemukan: ${name}`)
  const openAt = src.slice(idx + marker.length).search(/[[{]/)
  const start = idx + marker.length + openAt
  const open = src[start]
  const close = open === '[' ? ']' : '}'

  let depth = 0
  let quote = null
  let escaped = false
  for (let p = start; p < src.length; p++) {
    const ch = src[p]
    if (quote) {
      if (escaped) escaped = false
      else if (ch === '\\') escaped = true
      else if (ch === quote) quote = null
      continue
    }
    if (ch === "'" || ch === '"') {
      quote = ch
      continue
    }
    if (ch === open) depth++
    else if (ch === close) {
      depth--
      if (depth === 0) {
        // Literal murni (array of array / object of string) — aman dieval.
        return eval(src.slice(start, p + 1))
      }
    }
  }
  throw new Error(`literal ${name} tidak selesai`)
}

const CATEGORY_LABELS = {
  alkali: 'Logam Alkali',
  alkaline: 'Logam Alkali Tanah',
  transition: 'Logam Transisi',
  'post-transition': 'Logam Pasca-transisi',
  metalloid: 'Metaloid',
  nonmetal: 'Nonlogam',
  halogen: 'Halogen',
  'noble-gas': 'Gas Mulia',
  lanthanide: 'Lantanida',
  actinide: 'Aktinida',
}

const rawElements = grab('rawElements')
const categories = grab('categories')
const details = grab('details')
const categoryDefaults = grab('categoryDefaults')
const ions = grab('ions')

const propsPath = path.join(path.dirname(SEED), 'element-properties.json')
const properties = JSON.parse(fs.readFileSync(propsPath, 'utf8'))

const elements = rawElements.map(
  ([atomicNumber, symbol, nameId, nameLatin, atomicMass, category, period, group]) => {
    const props = properties[symbol] ?? {}
    const detail = details[symbol] ?? {}
    const defaults = categoryDefaults[category] ?? {}
    const label = CATEGORY_LABELS[category] ?? category
    return {
      atomic_number: atomicNumber,
      symbol,
      name: nameId,
      name_latin: nameLatin,
      atomic_mass: atomicMass,
      category,
      period,
      group,
      description:
        detail.description ??
        `${nameId} (${symbol}) adalah ${label.toLowerCase()} pada periode ${period}, golongan ${group}.`,
      uses: detail.uses ?? defaults.uses ?? null,
      hazard: detail.hazard ?? defaults.hazard ?? null,
      properties: {
        melt: props.melt ?? null,
        boil: props.boil ?? null,
        density: props.density ?? null,
        electronegativity: props.electronegativity ?? null,
        ionization: props.ionization ?? null,
        atomicRadius: props.atomicRadius ?? null,
        covalentRadius: props.covalentRadius ?? null,
        molarHeat: props.molarHeat ?? null,
        phase: props.phase ?? null,
        block: props.block ?? null,
        shells: props.shells ?? null,
        oxidationStates: props.oxidationStates ?? null,
        appearance: props.appearance ?? null,
        discoveredBy: props.discoveredBy ?? null,
        namedBy: props.namedBy ?? null,
        yearDiscovered: props.yearDiscovered ?? null,
      },
    }
  },
)

const categoryOut = categories.map(({ slug, name }) => ({ slug, name }))
const ionOut = ions.map(([name, formula, charge, description]) => ({
  name,
  formula,
  charge,
  description: description ?? null,
}))

fs.mkdirSync(OUT_DIR, { recursive: true })
const write = (file, data) =>
  fs.writeFileSync(path.join(OUT_DIR, file), JSON.stringify(data, null, 2) + '\n', 'utf8')

write('elements.json', elements)
write('categories.json', categoryOut)
write('ions.json', ionOut)

console.log(
  `OK: ${elements.length} unsur, ${categoryOut.length} kategori, ${ionOut.length} ion → ${OUT_DIR}`,
)
