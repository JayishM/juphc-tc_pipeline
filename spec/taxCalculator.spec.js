const {
  calculateTax,
  calculateTaxWithDeductions,
  calculateNetIncome,
  calculateEffectiveRate,
  validateIncome
} = require("../taxCalculator");

describe("Tax Calculator Unit Tests", function() {

  it("should calculate 0 tax for income within the first tax-free bracket", function() {
    const tax = calculateTax(8000);
    expect(tax).toEqual(0);
  });

  it("should calculate 10% tax correctly for the second bracket", function() {
    // Income: 25000 -> First 10000 free, remaining 15000 * 0.10 = 1500
    const tax = calculateTax(25000);
    expect(tax).toEqual(1500);
  });

  it("should calculate progressive tax correctly for the third bracket", function() {
    // Income: 50000 -> 0 + (30000 * 0.10 = 3000) + (10000 * 0.20 = 2000) = 5000
    const tax = calculateTax(50000);
    expect(tax).toEqual(5000);
  });

  it("should calculate progressive tax correctly for income in the top bracket", function() {
    // Income: 100000 -> 0 + 3000 + (40000 * 0.20 = 8000) + (20000 * 0.30 = 6000) = 17000
    const tax = calculateTax(100000);
    expect(tax).toEqual(17000);
  });

  it("should accurately apply deductions before computing tax", function() {
    // Income: 50000 with 10000 deduction -> Taxable: 40000 -> Tax: 3000
    const tax = calculateTaxWithDeductions(50000, 10000);
    expect(tax).toEqual(3000);
  });

  it("should throw an error when income is negative", function() {
    expect(function() {
      validateIncome(-500);
    }).toThrowError("Income cannot be negative");
  });

  it("should calculate net income and effective tax rate correctly", function() {
    const income = 50000;
    const tax = 5000;
    const net = calculateNetIncome(income, tax);
    const rate = calculateEffectiveRate(income, tax);

    expect(net).toEqual(45000);
    expect(rate).toEqual(10);
  });

});
