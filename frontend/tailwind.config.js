/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      colors: {
        neon: {
          blue:   '#00d4ff',
          purple: '#8b5cf6',
          cyan:   '#06b6d4',
          green:  '#10b981',
          red:    '#ef4444',
        },
      },
      keyframes: {
        'gradient-shift': {
          '0%, 100%': { 'background-position': '0% 50%' },
          '50%':      { 'background-position': '100% 50%' },
        },
        'pulse-glow': {
          '0%, 100%': { opacity: '0.6' },
          '50%':      { opacity: '1' },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%':      { transform: 'translateY(-16px)' },
        },
        'spin-slow': {
          from: { transform: 'rotate(0deg)' },
          to:   { transform: 'rotate(360deg)' },
        },
      },
      animation: {
        'gradient-shift': 'gradient-shift 5s ease infinite',
        'pulse-glow':     'pulse-glow 2.5s ease-in-out infinite',
        'float':          'float 7s ease-in-out infinite',
        'spin-slow':      'spin-slow 20s linear infinite',
      },
    },
  },
  plugins: [],
}
