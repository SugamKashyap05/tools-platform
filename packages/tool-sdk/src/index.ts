/**
 * Tool manifest schema — every tool in `tools/` must declare one of these.
 * This is the canonical shape the platform reads at registration time.
 */
export interface ToolManifest {
  /** Unique tool identifier, kebab-case, e.g. "url-shortener" */
  name: string;
  /** Human-readable label for UI */
  label: string;
  /** Short description shown on the tool card */
  description: string;
  /** Path relative to the tool root, e.g. "./icon.svg" */
  icon: string;
  /** URL route the tool is mounted at, e.g. "/tools/url-shortener" */
  route: string;
  /** Stub hook for free-tier quota enforcement (no-op today, see platform-conventions.md) */
  quotaHook: string;
  /** Optional: tags for discovery */
  tags?: string[];
  /** Optional: whether the tool is enabled (default true) */
  enabled?: boolean;
}

/**
 * Tool entry-point interface — every tool must export an object conforming to this
 * from its main module. The platform calls `init()` at startup and `render()` for
 * the tool's page.
 */
export interface ToolEntryPoint {
  /** The tool's manifest */
  manifest: ToolManifest;
  /** Called once at server startup; use for DB migrations, config validation */
  init(): Promise<void> | void;
  /** Called when the tool's route is hit; returns JSX/element or a response object */
  render(): unknown;
  /** Optional: cleanup on shutdown */
  dispose?(): Promise<void> | void;
}

/**
 * Type guard for runtime manifest validation.
 */
export function isToolManifest(value: unknown): value is ToolManifest {
  return (
    typeof value === 'object' &&
    value !== null &&
    typeof (value as Record<string, unknown>).name === 'string' &&
    typeof (value as Record<string, unknown>).label === 'string' &&
    typeof (value as Record<string, unknown>).description === 'string' &&
    typeof (value as Record<string, unknown>).icon === 'string' &&
    typeof (value as Record<string, unknown>).route === 'string' &&
    typeof (value as Record<string, unknown>).quotaHook === 'string'
  );
}

/**
 * Type guard for tool entry-point conformance.
 */
export function isToolEntryPoint(value: unknown): value is ToolEntryPoint {
  return (
    typeof value === 'object' &&
    value !== null &&
    isToolManifest((value as Record<string, unknown>).manifest) &&
    typeof (value as Record<string, unknown>).init === 'function' &&
    typeof (value as Record<string, unknown>).render === 'function'
  );
}