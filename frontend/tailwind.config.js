/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        soil: '#7c4a24',
        canopy: '#0f8f62',
        leaf: '#30c77b',
        mist: '#eefbf4',
        ink: '#101828',
      },
      boxShadow: {
        glow: '0 24px 90px rgba(48, 199, 123, 0.22)',
        soft: '0 20px 60px rgba(15, 23, 42, 0.12)',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
