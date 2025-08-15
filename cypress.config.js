
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5000',
    supportFile: false, // <-- LÍNEA CLAVE AÑADIDA
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
