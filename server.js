const express = require('express');
const path = require('path');
const {
  calculateTax,
  calculateTaxWithDeductions,
  calculateNetIncome,
  calculateEffectiveRate,
  validateIncome
} = require('./taxCalculator');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware for parsing JSON and form bodies
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static frontend assets
app.use(express.static(path.join(__dirname)));

// Health check endpoint for container and deployment verification
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'UP',
    service: 'tax-calculator',
    version: '1.0.0',
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// Tax calculation API endpoint
app.post('/api/calculate', (req, res) => {
  try {
    const { income, deductions = 0 } = req.body;

    if (income === undefined || income === null || income === '') {
      return res.status(400).json({
        error: 'Gross annual income is required'
      });
    }

    const numIncome = Number(income);
    const numDeductions = Math.max(0, Number(deductions) || 0);

    const validIncome = validateIncome(numIncome);
    const taxableIncome = Math.max(0, validIncome - numDeductions);
    const tax = calculateTaxWithDeductions(validIncome, numDeductions);
    const netIncome = calculateNetIncome(validIncome, tax);
    const effectiveRate = calculateEffectiveRate(validIncome, tax);

    return res.status(200).json({
      grossIncome: validIncome,
      deductions: numDeductions,
      taxableIncome,
      tax,
      netIncome,
      effectiveRate
    });
  } catch (error) {
    return res.status(400).json({
      error: error.message || 'Error calculating tax'
    });
  }
});

// Fallback route to serve index.html for any unhandled GET request
app.use((req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Start server if executed directly
if (require.main === module) {
  const server = app.listen(PORT, () => {
    console.log(`Tax Calculator server running on port ${PORT}`);
    console.log(`Health check available at http://localhost:${PORT}/health`);
  });

  // Graceful shutdown
  const handleShutdown = (signal) => {
    console.log(`Received ${signal}. Shutting down gracefully...`);
    server.close(() => {
      console.log('HTTP server closed.');
      process.exit(0);
    });
  };

  process.on('SIGTERM', () => handleShutdown('SIGTERM'));
  process.on('SIGINT', () => handleShutdown('SIGINT'));
}

module.exports = app;
