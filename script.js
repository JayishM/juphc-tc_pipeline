document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("tax-form");
  const incomeInput = document.getElementById("income");
  const deductionsInput = document.getElementById("deductions");
  const resultsCard = document.getElementById("results");

  const resTaxable = document.getElementById("res-taxable");
  const resTax = document.getElementById("res-tax");
  const resNet = document.getElementById("res-net");
  const resRate = document.getElementById("res-rate");

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const grossIncome = parseFloat(incomeInput.value);
    const deductions = parseFloat(deductionsInput.value) || 0;

    if (isNaN(grossIncome) || grossIncome < 0) {
      alert("Please enter a valid positive income.");
      return;
    }

    try {
      const taxable = Math.max(0, grossIncome - deductions);
      const tax = window.TaxCalculator.calculateTaxWithDeductions(grossIncome, deductions);
      const net = window.TaxCalculator.calculateNetIncome(grossIncome, tax);
      const rate = window.TaxCalculator.calculateEffectiveRate(grossIncome, tax);

      resTaxable.textContent = `$${taxable.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      resTax.textContent = `$${tax.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      resNet.textContent = `$${net.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      resRate.textContent = `${rate.toFixed(2)}%`;

      resultsCard.classList.remove("hidden");
    } catch (err) {
      alert("Error calculating tax: " + err.message);
    }
  });
});
