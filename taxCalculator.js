/**
 * Tax Calculator Business Logic
 */

function validateIncome(income) {
  if (income === null || income === undefined || isNaN(income)) {
    throw new Error("Invalid income value");
  }
  if (Number(income) < 0) {
    throw new Error("Income cannot be negative");
  }
  return Number(income);
}

function calculateTax(income) {
  const taxableIncome = validateIncome(income);

  // Example progressive tax brackets:
  // 0 - $10,000 : 0%
  // $10,001 - $40,000 : 10%
  // $40,001 - $80,000 : 20%
  // > $80,000 : 30%

  let tax = 0;

  if (taxableIncome <= 10000) {
    tax = 0;
  } else if (taxableIncome <= 40000) {
    tax = (taxableIncome - 10000) * 0.10;
  } else if (taxableIncome <= 80000) {
    tax = (30000 * 0.10) + ((taxableIncome - 40000) * 0.20);
  } else {
    tax = (30000 * 0.10) + (40000 * 0.20) + ((taxableIncome - 80000) * 0.30);
  }

  return Math.round(tax * 100) / 100;
}

function calculateTaxWithDeductions(income, deductions = 0) {
  const validIncome = validateIncome(income);
  const validDeductions = Math.max(0, Number(deductions) || 0);
  const taxableIncome = Math.max(0, validIncome - validDeductions);
  return calculateTax(taxableIncome);
}

function calculateNetIncome(income, tax) {
  const validIncome = validateIncome(income);
  return Math.round((validIncome - tax) * 100) / 100;
}

function calculateEffectiveRate(income, tax) {
  const validIncome = validateIncome(income);
  if (validIncome === 0) return 0;
  return Math.round((tax / validIncome) * 10000) / 100;
}

// Export for Node.js / Jasmine tests and browser support
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    validateIncome,
    calculateTax,
    calculateTaxWithDeductions,
    calculateNetIncome,
    calculateEffectiveRate
  };
}

if (typeof window !== "undefined") {
  window.TaxCalculator = {
    validateIncome,
    calculateTax,
    calculateTaxWithDeductions,
    calculateNetIncome,
    calculateEffectiveRate
  };
}
