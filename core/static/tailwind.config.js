/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './core/static/**/*.{html,js}',
    './core/static/*.{html,js}',
  ], //"index.html","login.html","signup.html",
  darkMode: 'class',
  theme: {
    container: {
      center: true,
      padding: '16px',
    },
    extend: {
      fontFamily:{
        roboto: ['Roboto'],
        nunito: ['Nunito']
      },
      screens: {
        '2xl': '1320px',
      },
      colors: {
        dark: '#0f172a',
      }
    },
  },
  plugins: [],
}

