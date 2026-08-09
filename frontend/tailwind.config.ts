import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0b0f17",
        foreground: "#f8fafc",
        card: {
          DEFAULT: "rgba(15, 23, 42, 0.75)",
          foreground: "#f8fafc",
        },
        popover: {
          DEFAULT: "#0f172a",
          foreground: "#f8fafc",
        },
        primary: {
          DEFAULT: "#0d9488", // DecisionX Teal
          foreground: "#ffffff",
        },
        secondary: {
          DEFAULT: "#1e293b",
          foreground: "#f8fafc",
        },
        accent: {
          DEFAULT: "#2563eb", // Base Blue
          purple: "#8b5cf6",  // Tempo Purple
          amber: "#d97706",   // Early Access Amber
        },
        destructive: {
          DEFAULT: "#e11d48", // Rose Red
          foreground: "#ffffff",
        },
        border: "rgba(255, 255, 255, 0.08)",
        input: "rgba(255, 255, 255, 0.06)",
        ring: "#0d9488",
      },
      borderRadius: {
        xl: "18px",
        lg: "14px",
        md: "10px",
        sm: "6px",
      },
      fontFamily: {
        sans: ["var(--font-sans)", "Inter", "system-ui", "sans-serif"],
        mono: ["var(--font-mono)", "JetBrains Mono", "monospace"],
      },
      boxShadow: {
        glow: "0 0 30px -5px rgba(13, 148, 136, 0.25)",
        "glow-purple": "0 0 30px -5px rgba(139, 92, 246, 0.25)",
        "glow-blue": "0 0 30px -5px rgba(37, 99, 235, 0.25)",
        "dx-card": "0 4px 20px rgba(0, 0, 0, 0.25), inset 0 1px 0 0 rgba(255, 255, 255, 0.08)",
      },
    },
  },
  plugins: [],
};

export default config;
