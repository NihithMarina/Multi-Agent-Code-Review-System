/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Space Grotesk"', 'Segoe UI', 'sans-serif'],
        body: ['"Space Grotesk"', 'Segoe UI', 'sans-serif'],
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(255,255,255,0.05), 0 20px 60px rgba(0,0,0,0.35)',
      },
      colors: {
        ink: {
          950: '#050816',
          900: '#0a1020',
          800: '#111a33',
          700: '#1d2a4a',
        },
        aurora: {
          cyan: '#39d0ff',
          mint: '#57f7c8',
          gold: '#ffd166',
          coral: '#ff7a59',
        },
      },
    },
  },
  plugins: [],
}
