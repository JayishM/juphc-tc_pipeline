document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("tax-form");
  const incomeInput = document.getElementById("income");
  const deductionsInput = document.getElementById("deductions");
  const resultsCard = document.getElementById("results");
  const resetBtn = document.getElementById("reset-btn");
  const alertBanner = document.getElementById("alert-banner");

  const resTaxable = document.getElementById("res-taxable");
  const resTax = document.getElementById("res-tax");
  const resNet = document.getElementById("res-net");
  const resRate = document.getElementById("res-rate");

  function showAlert(message) {
    if (alertBanner) {
      alertBanner.textContent = message;
      alertBanner.classList.remove("hidden");
    }
  }

  function hideAlert() {
    if (alertBanner) {
      alertBanner.textContent = "";
      alertBanner.classList.add("hidden");
    }
  }

  function resetForm() {
    form.reset();
    deductionsInput.value = "0";
    hideAlert();
    resultsCard.classList.add("hidden");
    incomeInput.focus();
  }

  if (resetBtn) {
    resetBtn.addEventListener("click", resetForm);
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    hideAlert();

    const rawIncome = incomeInput.value.trim();
    const rawDeductions = deductionsInput.value.trim();

    if (rawIncome === "") {
      showAlert("Please enter your gross annual income.");
      incomeInput.focus();
      return;
    }

    const grossIncome = parseFloat(rawIncome);
    const deductions = rawDeductions === "" ? 0 : parseFloat(rawDeductions);

    if (isNaN(grossIncome)) {
      showAlert("Gross annual income must be a valid number.");
      incomeInput.focus();
      return;
    }

    if (grossIncome < 0) {
      showAlert("Gross annual income cannot be negative.");
      incomeInput.focus();
      return;
    }

    if (isNaN(deductions) || deductions < 0) {
      showAlert("Total deductions must be a positive number or zero.");
      deductionsInput.focus();
      return;
    }

    try {
      const calc = window.TaxCalculator;
      if (!calc) {
        throw new Error("Tax calculation module not loaded.");
      }

      const taxable = Math.max(0, grossIncome - deductions);
      const tax = calc.calculateTaxWithDeductions(grossIncome, deductions);
      const net = calc.calculateNetIncome(grossIncome, tax);
      const rate = calc.calculateEffectiveRate(grossIncome, tax);

      resTaxable.textContent = `$${taxable.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      resTax.textContent = `$${tax.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      resNet.textContent = `$${net.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      resRate.textContent = `${rate.toFixed(2)}%`;

      resultsCard.classList.remove("hidden");
    } catch (err) {
      showAlert("Error calculating tax: " + err.message);
    }
  });
});
