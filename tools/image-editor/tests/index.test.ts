import { describe, expect, it, vi, beforeAll } from 'vitest';
import type { ToolEntryPoint, ToolManifest } from '@repo/tool-sdk';

// We'll import the actual entry point after we create it
// For now, we'll mock the import to see the test fail, then replace with real import.

describe('image-editor tool entry point', () => {
  let entryPoint: ToolEntryPoint;

  beforeAll(async () => {
    // Dynamically import the module we are about to create
    const module = await import('../src/index');
    entryPoint = module.default as ToolEntryPoint;
  });

  it('exports a manifest object', () => {
    expect(entryPoint.manifest).toBeDefined();
    // Check required fields
    expect(typeof entryPoint.manifest.name).toBe('string');
    expect(entryPoint.manifest.name).toBe('image-editor');
    expect(typeof entryPoint.manifest.label).toBe('string');
    expect(typeof entryPoint.manifest.description).toBe('string');
    expect(typeof entryPoint.manifest.icon).toBe('string');
    expect(typeof entryPoint.manifest.route).toBe('string');
    expect(typeof entryPoint.manifest.quotaHook).toBe('string');
  });

  it('exports an init function', () => {
    expect(typeof entryPoint.init).toBe('function');
  });

  it('exports a render function', () => {
    expect(typeof entryPoint.render).toBe('function');
  });

  it('exports an optional dispose function', () => {
    // dispose is optional, so we just check if it's a function if present
    if (entryPoint.dispose) {
      expect(typeof entryPoint.dispose).toBe('function');
    }
  });

  // Additional test: init should not throw
  it('init runs without throwing', () => {
    expect(() => entryPoint.init()).not.toThrow();
  });

  // Additional test: render returns something (we don't specify what, just not throw)
  it('render returns without throwing', () => {
    expect(() => entryPoint.render()).not.toThrow();
  });
});