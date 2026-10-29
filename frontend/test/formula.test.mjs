import test from 'node:test'
import assert from 'node:assert/strict'

import { parseFormula, prettyFormula, subscript } from '../src/utils/formula.js'

test('parseFormula handles parentheses and multipliers', () => {
  assert.deepEqual(parseFormula('Al2(SO4)3'), { Al: 2, S: 3, O: 12 })
  assert.deepEqual(parseFormula('Ca(OH)2'), { Ca: 1, O: 2, H: 2 })
  assert.deepEqual(parseFormula('C6H12O6'), { C: 6, H: 12, O: 6 })
})

test('parseFormula handles nested element symbols', () => {
  assert.deepEqual(parseFormula('NaCl'), { Na: 1, Cl: 1 })
  assert.deepEqual(parseFormula('Fe2(SO4)3'), { Fe: 2, S: 3, O: 12 })
})

test('prettyFormula converts digits to subscripts', () => {
  assert.equal(prettyFormula('Fe2O3'), 'Fe₂O₃')
  assert.equal(prettyFormula('H2O'), 'H₂O')
})

test('subscript skips the number one', () => {
  assert.equal(subscript(1), '')
  assert.equal(subscript(12), '₁₂')
})
