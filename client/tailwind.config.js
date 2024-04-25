const colors = require('tailwindcss/colors')

module.exports = {
  purge: {
    enabled: true,
    content: ['./public/*.{html,js}'],
  },
  theme: {
    extend: {
      colors: {
        'light-blue': colors.lightBlue,
        cyan: colors.cyan,
      },
    },
  },
  variants: {},
  plugins: [],
}