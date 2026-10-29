/**
 * Gaya & penanda blok tabel periodik (adaptasi tema gelap BioChemVerse
 * dari proyek ChemSphere — lihat frontend/src/data/categories.js).
 */

export const categoryStyles = {
  alkali: {
    bg: 'bg-orange-500/15',
    text: 'text-orange-400',
    border: 'border-orange-500/40',
    dot: 'bg-orange-500',
    label: 'Logam Alkali',
  },
  alkaline: {
    bg: 'bg-amber-500/15',
    text: 'text-amber-400',
    border: 'border-amber-500/40',
    dot: 'bg-amber-500',
    label: 'Logam Alkali Tanah',
  },
  transition: {
    bg: 'bg-blue-500/15',
    text: 'text-blue-400',
    border: 'border-blue-500/40',
    dot: 'bg-blue-500',
    label: 'Logam Transisi',
  },
  'post-transition': {
    bg: 'bg-slate-500/15',
    text: 'text-slate-300',
    border: 'border-slate-400/40',
    dot: 'bg-slate-400',
    label: 'Logam Pasca-transisi',
  },
  metalloid: {
    bg: 'bg-teal-500/15',
    text: 'text-teal-400',
    border: 'border-teal-500/40',
    dot: 'bg-teal-500',
    label: 'Metaloid',
  },
  nonmetal: {
    bg: 'bg-lime-500/15',
    text: 'text-lime-400',
    border: 'border-lime-500/40',
    dot: 'bg-lime-500',
    label: 'Nonlogam',
  },
  halogen: {
    bg: 'bg-yellow-500/15',
    text: 'text-yellow-400',
    border: 'border-yellow-500/40',
    dot: 'bg-yellow-500',
    label: 'Halogen',
  },
  'noble-gas': {
    bg: 'bg-violet-500/15',
    text: 'text-violet-400',
    border: 'border-violet-500/40',
    dot: 'bg-violet-500',
    label: 'Gas Mulia',
  },
  lanthanide: {
    bg: 'bg-pink-500/15',
    text: 'text-pink-400',
    border: 'border-pink-500/40',
    dot: 'bg-pink-500',
    label: 'Lantanida',
  },
  actinide: {
    bg: 'bg-rose-500/15',
    text: 'text-rose-400',
    border: 'border-rose-500/40',
    dot: 'bg-rose-500',
    label: 'Aktinida',
  },
}

const fallbackStyle = {
  bg: 'bg-slate-500/15',
  text: 'text-slate-300',
  border: 'border-slate-500/40',
  dot: 'bg-slate-400',
  label: 'Tidak diketahui',
}

/** @param {string|null|undefined} slug */
export function styleForCategory(slug) {
  return categoryStyles[slug] ?? fallbackStyle
}

export function isLanthanide(atomicNumber) {
  return atomicNumber >= 57 && atomicNumber <= 71
}

export function isActinide(atomicNumber) {
  return atomicNumber >= 89 && atomicNumber <= 103
}

export function isFBlock(element) {
  return isLanthanide(element.atomic_number) || isActinide(element.atomic_number)
}
