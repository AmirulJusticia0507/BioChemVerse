import test from 'node:test'
import assert from 'node:assert/strict'

import {
  AVOGADRO,
  balanceEquation,
  dilution,
  massFromMoles,
  molarMassOf,
  molarity,
  molesFromMass,
  molesFromParticles,
  particlesFromMoles,
  parseEquation,
  volumeFromMoles,
} from '../src/utils/stoichiometry.js'

const masses = { H: 1.008, O: 15.999, C: 12.011, Na: 22.99, Cl: 35.45, Fe: 55.845, Al: 26.982 }
const massOf = (symbol) => masses[symbol] ?? null

test('parseEquation splits reactants and products', () => {
  const { left, right } = parseEquation('Fe2O3 + 3CO -> 2Fe + 3CO2')
  assert.equal(left.length, 2)
  assert.equal(right.length, 2)
  assert.equal(left[1].coefficient, 3)
  assert.equal(left[1].formula, 'CO')
})

test('parseEquation accepts arrow and equals sign', () => {
  assert.ok(!parseEquation('H2 + O2 → H2O').error)
  assert.ok(!parseEquation('H2 + O2 = H2O').error)
})

test('parseEquation rejects an equation without an arrow', () => {
  const result = parseEquation('H2O')
  assert.ok(result.error)
})

test('balances water synthesis', () => {
  const result = balanceEquation('H2 + O2 -> H2O')
  assert.equal(result.ok, true)
  assert.deepEqual(result.coefficients, [2, 1, 2])
})

test('balances iron oxide reduction', () => {
  const result = balanceEquation('Fe2O3 + CO -> Fe + CO2')
  assert.equal(result.ok, true)
  assert.deepEqual(result.coefficients, [1, 3, 2, 3])
})

test('balances propane combustion', () => {
  const result = balanceEquation('C3H8 + O2 -> CO2 + H2O')
  assert.equal(result.ok, true)
  assert.deepEqual(result.coefficients, [1, 5, 3, 4])
})

test('balances aluminium and hydrochloric acid', () => {
  const result = balanceEquation('Al + HCl -> AlCl3 + H2')
  assert.equal(result.ok, true)
  assert.deepEqual(result.coefficients, [2, 6, 2, 3])
})

test('balances a reaction with parentheses', () => {
  const result = balanceEquation('Ca(OH)2 + H3PO4 -> Ca3(PO4)2 + H2O')
  assert.equal(result.ok, true)
  assert.deepEqual(result.coefficients, [3, 2, 1, 6])
})

test('rejects an equation that cannot be balanced', () => {
  const result = balanceEquation('H2 + O2 -> Fe2O3')
  assert.equal(result.ok, false)
  assert.ok(result.error)
})

test('already balanced equation keeps coefficient 1', () => {
  const result = balanceEquation('N2 + 3H2 -> 2NH3')
  assert.equal(result.ok, true)
  assert.deepEqual(result.coefficients, [1, 3, 2])
})

test('molarMassOf sums contributions and reports breakdown', () => {
  const { total, breakdown, missing } = molarMassOf('H2O', massOf)
  assert.equal(missing.length, 0)
  assert.ok(Math.abs(total - 18.015) < 0.001)
  assert.equal(breakdown.length, 2)
})

test('molarMassOf reports unknown symbols', () => {
  const { missing } = molarMassOf('Xx2O', massOf)
  assert.ok(missing.includes('Xx'))
})

test('molesFromMass and massFromMoles are inverses', () => {
  const moles = molesFromMass(18.015, 18.015)
  assert.ok(Math.abs(moles - 1) < 1e-9)
  assert.ok(Math.abs(massFromMoles(moles, 18.015) - 18.015) < 1e-9)
})

test('particle conversions use Avogadro constant', () => {
  assert.ok(Math.abs(particlesFromMoles(1) - AVOGADRO) < 1)
  assert.ok(Math.abs(molesFromParticles(AVOGADRO) - 1) < 1e-12)
})

test('volumeFromMoles uses 22.414 L/mol at STP', () => {
  assert.ok(Math.abs(volumeFromMoles(1) - 22.414) < 1e-9)
})

test('molarity divides moles by litres', () => {
  assert.equal(molarity(0.5, 2), 0.25)
  assert.equal(molarity(1, 0), null)
})

test('dilution solves for the missing value', () => {
  assert.deepEqual(dilution({ m1: null, v1: 0.1, m2: 0.5, v2: 0.5 }), {
    value: 2.5,
    solvedFor: 'M1',
  })
  assert.deepEqual(dilution({ m1: 2, v1: null, m2: 0.5, v2: 0.5 }), {
    value: 0.125,
    solvedFor: 'V1',
  })
})

test('dilution requires exactly three values', () => {
  assert.ok(dilution({ m1: 1, v1: 1, m2: null, v2: null }).error)
})
