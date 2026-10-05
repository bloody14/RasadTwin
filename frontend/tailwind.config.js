/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        command: {
          black: '#0B0F0C',
          dark: '#121713',
          panel: '#181F1A',
        },
        olive: {
          deep: '#202820',
          military: '#46543A',
          muted: '#2F3D31',
        },
        sand: {
          field: '#C8B98A',
          warm: '#E0D2AA',
        },
        accent: {
          amber: '#D6A63C',
          blue: '#6D9FB3',
          green: '#6F9C5B',
          warning: '#D49A34',
          critical: '#C94C45',
        },
        neutral: {
          gray: '#9AA39A',
          white: '#E9ECE7',
        }
      },
      fontFamily: {
        sans: ['Inter', 'IBM Plex Sans', 'system-ui', 'sans-serif'],
        mono: ['IBM Plex Mono', 'JetBrains Mono', 'monospace'],
      }
    },
  },
  plugins: [],
}
