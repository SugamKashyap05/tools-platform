# Platform conventions

This file is the tool-building contract for `tools-platform`. It is based on the actual
files in `packages/tool-sdk/src/index.ts` and `packages/tool-sdk/src/manifest.ts`.

## Tool manifest contract

Every tool under `tools/` must provide a manifest conforming to `ToolManifest`:

```ts
interface ToolManifest {
  name: string;
  label: string;
  description: string;
  icon: string;
  route: string;
  quotaHook: string;
  tags?: string[];
  enabled?: boolean;
}
```

Field meanings:

- `name` — unique kebab-case identifier, for example `url-shortener`.
- `label` — human-readable UI label.
- `description` — short description shown on the tool card.
- `icon` — path relative to the tool root, for example `./icon.svg`.
- `route` — URL route where the tool is mounted, for example `/tools/url-shortener`.
- `quotaHook` — required string identifier for the free-tier quota hook. The current SDK
  intentionally provides no enforcement implementation; the field is still mandatory.
- `tags` — optional discovery/filtering tags.
- `enabled` — optional enable flag; when omitted, the platform treats the tool as enabled.

`src/index.ts` exports `ToolManifest`, `isToolManifest(value)`, `ToolEntryPoint`, and
`isToolEntryPoint(value)`. `src/manifest.ts` re-exports the two types and both guards.
The package's public exports are `.` and `./manifest`; do not bypass these exports with
relative imports into another package's source directory.

## Tool entry-point contract

Every tool must export an object conforming to `ToolEntryPoint`:

```ts
interface ToolEntryPoint {
  manifest: ToolManifest;
  init(): Promise<void> | void;
  render(): unknown;
  dispose?(): Promise<void> | void;
}
```

- `manifest` — the tool's `ToolManifest`.
- `init()` — runs once at server startup for migrations, configuration validation, or
  other startup work.
- `render()` — runs when the tool's route is requested and returns the tool's UI element,
  JSX, or response object.
- `dispose?()` — optional cleanup at shutdown.

The runtime guards require the manifest fields listed above and require `init` and `render`
to be functions. A tool that omits either required method is not compliant.

## Naming and layout

- Put each tool in `tools/<kebab-case-tool-name>/`.
- Use the same kebab-case value for the manifest `name` and the route suffix.
- Prefer `/tools/<kebab-case-tool-name>` for `route` unless the platform assigns a
  different mount path.
- Keep the tool's public implementation in `src/index.ts` and keep assets relative to the
  tool root.
- Use `camelCase` for exported functions and variables, `PascalCase` for types/interfaces,
  and `kebab-case` for files, directories, tool names, and routes.
- Use `@repo/*` only for shared workspace packages. Do not invent a new package scope for
  a single tool during Phase 3.
- Do not add production tool logic to Phase 1/2 scaffolding tasks.

## Free-tier quota constraint

Every tool must call the platform quota hook using the exact manifest `quotaHook` value
before performing its work. Today that hook is a no-op/stub and always permits the request,
but the call is mandatory so enforcement can be added later without changing every tool.

Do not rename `quotaHook`, replace it with an optional field, or remove the call because the
current implementation is permissive. The call is a structural free-tier contract, not an
optional optimization.

## Validation and evolution

Use `isToolManifest` and `isToolEntryPoint` when validating dynamically loaded tools. Add
new fields only when the platform has a defined consumer and update this file, the SDK
types, and the guards together. Keep the contract minimal until a real tool requires more
than the fields above.
