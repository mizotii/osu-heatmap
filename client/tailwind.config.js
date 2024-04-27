/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: ['./src/**/*.svelte'],
  content: ["./public/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
}