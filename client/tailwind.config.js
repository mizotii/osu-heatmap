/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./**/*.{svelte,js,ts}'],
  theme: {
    extend: {
      screens: {
        '3xs': '150px',
        '2xs': '320px',
        'xs': '480px',
      }
    },
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui: {
    themes: [
      {
        osuheatmap: {
          "primary": "#ffc0d3",
          "primary-content": "#fff",
          "secondary": "#ce93d8",          
          "secondary-content": "#fff",
          "accent": "#ffc0d3",
          "accent-content": "#fff",
          "neutral-content": "#fff",
          "base-100": "#121212",
          "base-200": "#121212",
          "base-300": "#121212",
          "base-content": "#fff",
        },
      },
    ],
  },
}