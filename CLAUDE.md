# tools-platform

## Overview

`tools-platform` is an npm-workspaces monorepo orchestrated by Turborepo. It provides the
shared application and package skeleton for the web UI, API, authentication, UI primitives,
and the contract used by every tool under `tools/`.

The repository is deliberately scaffold-only at this phase. `tools/` is empty and no
production tool implementation is included.

## Architecture

- `apps/web/` — Next.js web application (`next`, React, and React DOM).
- `apps/api/` — TypeScript API application using `tsx` and Hono; it depends on `@repo/auth`
  and `@repo/tool-sdk`.
- `packages/ui/` — React UI package with source exports under `src/`.
- `packages/auth/` — authentication package with a `better-auth` dependency and a compiled
  `dist/` entry point.
- `packages/tool-sdk/` — TypeScript contract package. `src/index.ts` defines `ToolManifest`
  and `ToolEntryPoint`; `src/manifest.ts` re-exports those types and the runtime guards.
- `packages/eslint-config/` — shared ESLint configuration.
- `packages/typescript-config/` — shared TypeScript configuration presets.
- `tools/` — reserved for future tool implementations; currently empty.
- `turbo.json` — Turborepo task graph for build, dev, lint, and type-check tasks.

Internal packages use the `@repo/*` scope and are linked through the root `workspaces`
configuration.

## Key commands

Run these from the repository root:

```bash
npm install          # install/link all workspace dependencies
npm run dev          # start all persistent workspace dev tasks
npm run build        # build all workspaces through Turbo
npm run lint         # lint all workspaces through Turbo
npm run check-types  # type-check all workspaces through Turbo
npm run format       # format TypeScript, TSX, and Markdown files with Prettier
```

There is no test script yet. Until tests are introduced, use `npm run check-types` and
`npm run lint` as the baseline verification commands; package-level test scripts should be
added with the first testable implementation.

## Code standards

- Use two spaces for indentation in JSON, Markdown, TypeScript, JavaScript, and config files.
- Use double quotes in JSON and single quotes in TypeScript/JavaScript strings.
- Use semicolons in TypeScript and JavaScript.
- Use `kebab-case` for directories, tool names, routes, and commit task prefixes; use
  `camelCase` for variables/functions and `PascalCase` for types/interfaces.
- Name tool entry files `src/index.ts` unless a package's public exports require a more
  specific module name.
- Keep public TypeScript functions typed, enable strict checking, avoid `any`, and prefer
  explicit return types for exported functions.
- Keep package boundaries intact: import shared code through workspace package exports, not
  through relative paths that cross package boundaries.
- Do not use wildcard imports or default exports unless the package's public API requires
  them.
- Keep `console` usage to warnings and errors; ordinary logging belongs in the platform
  logger once one is introduced.
- Keep commits scoped to one logical change. Commit messages use the form
  `PHASEn-NNN: concise subject` for phased work.
- Do not commit `node_modules/`, `.turbo/`, `dist/`, `.next/`, `coverage/`, logs, or the
  temporary `phase1-*.md` prompt files.

## Working conventions

Quote Windows paths containing spaces in shell commands. Run commands from the repository
root unless a package script explicitly requires package-local execution. Do not add tool
logic while a task is scaffold-only.
