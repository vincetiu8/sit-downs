const plugin = require("tailwindcss/plugin")

/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "jit",
  darkMode: "class",
  content: ["./**/*.tsx"],
  theme: {
    extend: {
      colors: {
        primary: "#b986ff",
        secondary: "#b986ff",
        background: "#111111",
        "background-light": "#222222",
        "text-primary": "#dddddd",
        "text-secondary": "#B4B4B4",
        blur: "#b99ee7",
        transparent: "transparent",
        "border-color": "#ffffff20"
      },
      fontFamily: {
        inter: ["Inter", "sans-serif"]
      }
    }
  },
  plugins: [
    plugin(function ({ addComponents }) {
      addComponents({
        ".btn": {
          width: "100%",
          minHeight: "3rem",
          borderRadius: "0.75rem",
          color: "#dddddd",
          fontWeight: "500",
          fontSize: "0.875rem",
          background: "#222222",
          borderWidth: "1px",
          borderColor: "#ffffff20",
          transitionDuration: "300ms",
          "&:hover": {
            boxShadow: "inset 0 1rem 2rem 0 #ffffff05"
          }
        }
      })
    })
  ]
}
