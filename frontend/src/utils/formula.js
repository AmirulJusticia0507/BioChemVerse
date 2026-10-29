/**
 * Parser & formatter rumus kimia (adaptasi dari ChemSphere `utils/formula.js`).
 *
 * Hanya bagian yang dipakai kalkulator stoikiometri — generator senyawa
 * (yang bergantung pada tabel valensi) tidak ikut diport.
 */

const SUBSCRIPT = ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉']

/** Menulis angka sebagai subskrip Unicode; angka 1 tidak ditulis. */
export function subscript(count) {
  if (!count || count === 1) return ''
  return String(count)
    .split('')
    .map((digit) => SUBSCRIPT[Number(digit)])
    .join('')
}

/** Rumus ASCII (mis. "H2O") menjadi rumus bersubskrip ("H₂O"). */
export function prettyFormula(formula) {
  return String(formula).replace(/(\d+)/g, (match) => subscript(Number(match)))
}

/**
 * Mengurai rumus ASCII menjadi peta jumlah atom.
 * Mendukung tanda kurung: "Ca(OH)2", "Al2(SO4)3", "Fe2(SO4)3".
 *
 * @param {string} formula
 * @returns {Record<string, number>} mis. { Fe: 2, S: 3, O: 12 }
 */
export function parseFormula(formula) {
  const counts = {}
  const stack = [counts]
  let index = 0
  const text = String(formula)

  while (index < text.length) {
    const char = text[index]

    if (char === '(') {
      stack.push({})
      index += 1
      continue
    }

    if (char === ')') {
      const group = stack.pop()
      index += 1
      let digits = ''
      while (index < text.length && /\d/.test(text[index])) {
        digits += text[index]
        index += 1
      }
      const multiplier = digits ? Number(digits) : 1
      const target = stack[stack.length - 1]
      for (const [symbol, count] of Object.entries(group)) {
        target[symbol] = (target[symbol] ?? 0) + count * multiplier
      }
      continue
    }

    const match = /^[A-Z][a-z]?/.exec(text.slice(index))
    if (!match) {
      index += 1
      continue
    }
    const symbol = match[0]
    index += symbol.length
    let digits = ''
    while (index < text.length && /\d/.test(text[index])) {
      digits += text[index]
      index += 1
    }
    const target = stack[stack.length - 1]
    target[symbol] = (target[symbol] ?? 0) + (digits ? Number(digits) : 1)
  }

  return counts
}
