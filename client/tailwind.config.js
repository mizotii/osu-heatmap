/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./**/*.{svelte,js,ts}'],
  theme: {
    extend: {},
  },
  plugins: [
    require("daisyui")
  ],
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
          "base-100": "#333333",
          "base-200": "#222222",
          "base-300": "#111111",
          "base-content": "#fff",
        },
      },
    ],
  },
}