/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#19535F',      // Azul oscuro
        secondary: '#0B7A75',    // Verde azulado
        accent: '#7B2D26',       // Rojo terroso
        beige: '#D7C9AA',        // Color crema principal
        light: '#F0F3F5',        // Fondo claro
      }
    },
  },
  plugins: [],
}

