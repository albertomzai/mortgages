
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5000',
    supportFile: false, // <-- L�NEA CLAVE A�ADIDA
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
