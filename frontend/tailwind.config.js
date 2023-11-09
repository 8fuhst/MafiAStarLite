const colors = require('tailwindcss/colors')

module.exports = {
  content: ['./index.html', './src/**/*.{vue, js, ts, tsx, jsx}'],
  theme: {
    extend: {},
    colors: {
      'button-gray': {
        '50': '#f5f7fa',
        '100': '#ebeef3',
        '200': '#d2dbe6',
        '300': '#aabbcf',
        '400': '#7b97b5',
        '500': '#5b7b9c',
        '600': '#476282',
        '700': '#3a4f6a',
        '800': '#314155',
        '900': '#2e3b4c',
        '950': '#1f2632',
      },
      'button-purple': '#3b3255',
      black: colors.black,
      white: colors.white,
      gray: colors.gray,
      emerald: colors.emerald,
      indigo: colors.indigo,
      yellow: colors.yellow,
      blue: colors.blue,
    }
  },
  plugins: [],
}

