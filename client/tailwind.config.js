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
    themes: ["business"],
  },
}