# CLAUDE.md

This file documents the platform conventions for the Hermes agent when working on the tools-platform repository.

## Repository Layout

The repository is a Turborepo monorepo with the following structure:

- `apps/`: Contains web applications (e.g., `web`, `api`)
- `packages/`: Contains shared packages (e.g., `ui`, `auth`, `tool-sdk`, `eslint-config`, `typescript-config`)
- `tools/`: Contains tool implementations (each tool is a separate directory under `tools/`)

### Tool SDK Contract

The `@repo/tool-sdk` package provides the contract for tool development.

#### Tool Manifest

Every tool must declare a manifest in its `package.json` or via a `manifest.ts` file. The manifest shape is defined in `packages/tool-sdk/src/index.ts`:

```typescript
export interface ToolManifest {
  name: string;          // Unique tool identifier, kebab-case
  label: string;         // Human-readable label for UI
  description: string;   // Short description shown on the tool card
  icon: string;          // Path relative to the tool root, e.g. "./icon.svg"
  route: string;         // URL route the tool is mounted at, e.g. "/tools/url-shortener"
  quotaHook: string;     // Stub hook for free-tier quota enforcement (no-op today)
  tags?: string[];       // Optional: tags for discovery
  enabled?: boolean;     // Optional: whether the tool is enabled (default true)
}
```

#### Tool Entry Point

Every tool must export an object conforming to the `ToolEntryPoint` interface from its main module:

```typescript
export interface ToolEntryPoint {
  manifest: ToolManifest;
  init(): Promise<void> | void;   // Called once at server startup
  render(): unknown;              // Called when the tool's route is hit
  dispose?(): Promise<void> | void; // Optional: cleanup on shutdown
}
```

#### Type Guards

The SDK provides `isToolManifest` and `isToolEntryPoint` for runtime validation.

### Development Workflow

1. Create a new tool directory under `tools/` (e.g., `tools/my-tool`).
2. Add a `package.json` with the tool's name and dependencies.
3. Implement the `ToolEntryPoint` in a `src/index.ts` (or similar) and export it.
4. Ensure the tool's `package.json` includes the necessary exports for the SDK to load the manifest and entry point.
5. Build the tool with `tsc` (if using TypeScript) and ensure the output is in the `dist` directory.

### Platform Conventions

- Use TypeScript for all new code.
- Follow the ESLint configuration in `@repo/eslint-config`.
- Use the TypeScript configuration in `@repo/typescript-config`.
- All tools must be registered with the platform via the manifest and entry point contract.
- The `quotaHook` is a placeholder for future quota enforcement; currently, it can be any string (e.g., `"noop"`).

### Ignore Rules

The `.gitignore` file includes rules for:
- Node modules and build outputs
- Environment variables
- IDE files
- Turbo cache and logs

## Committing and Pushing

After making changes, run:
```bash
git add .
git commit -m "feat: initial commit of Phase 1 - monorepo scaffold and tool-sdk contract"
git push origin master
```
