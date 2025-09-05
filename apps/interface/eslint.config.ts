import js from "@eslint/js"
import globals from "globals"
import tseslint from "typescript-eslint"
import pluginReact from "eslint-plugin-react"
import stylistic from '@stylistic/eslint-plugin'
import { defineConfig } from "eslint/config"

export default defineConfig([
  {
    files: ["**/*.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"],
    plugins: { js, '@stylistic': stylistic },
    extends: ["js/recommended"],
    languageOptions: { globals: globals.browser },
    settings: { react: { version: "detect" } },
    rules: {
      "react/react-in-jsx-scope": "off"
    }
  },
  tseslint.configs.recommended,
  {
    ...pluginReact.configs.flat.recommended,
    rules: {
      ...pluginReact.configs.flat.recommended.rules,
      "react/react-in-jsx-scope": "off",
      "semi": ["error", "never"],
      '@stylistic/indent': ['error', 2],
      '@stylistic/comma-dangle': ['error', 'never'],
      '@stylistic/quotes': ['error', 'single'],
      "@typescript-eslint/no-unused-vars": ["error", {
        "args": "all",
        "argsIgnorePattern": "^_",
        "caughtErrors": "all",
        "caughtErrorsIgnorePattern": "^_",
        "destructuredArrayIgnorePattern": "^_",
        "varsIgnorePattern": "^_",
        "ignoreRestSiblings": true
      }]
    }
  }
])
