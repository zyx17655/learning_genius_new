/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./public/index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'edu-primary': '#4F46E5',
        'edu-secondary': '#7C3AED',
        'edu-accent': '#06B6D4',
        'edu-success': '#10B981',
        'edu-warning': '#F59E0B',
        'edu-error': '#EF4444',
        'edu-bg': '#F8FAFC',
        'edu-card': '#FFFFFF',
        'edu-text': '#1E293B',
        'edu-text-light': '#64748B',
      }
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        edu: {
          "primary": "#4F46E5",
          "primary-content": "#FFFFFF",
          "secondary": "#7C3AED",
          "secondary-content": "#FFFFFF",
          "accent": "#06B6D4",
          "accent-content": "#FFFFFF",
          "neutral": "#1E293B",
          "neutral-content": "#FFFFFF",
          "base-100": "#FFFFFF",
          "base-200": "#F1F5F9",
          "base-300": "#E2E8F0",
          "base-content": "#1E293B",
          "info": "#3B82F6",
          "info-content": "#FFFFFF",
          "success": "#10B981",
          "success-content": "#FFFFFF",
          "warning": "#F59E0B",
          "warning-content": "#FFFFFF",
          "error": "#EF4444",
          "error-content": "#FFFFFF",
        },
      },
    ],
  },
}
