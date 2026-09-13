module.exports = [
  "eslint:recommended",
  "eslint-plugin-turbo",
  "prettier",
  {
    rules: {
      "no-unused-vars": "warn",
      "@typescript-eslint/no-unused-vars": "warn",
      "no-console": ["error", { allow: ["warn", "error"] }],
    },
  },
];