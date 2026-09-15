import { ToolManifest, ToolEntryPoint } from '@repo/tool-sdk';
import { ImageEditor } from './ImageEditor';

export const manifest: ToolManifest = {
  name: 'image-editor',
  label: 'Image Editor',
  description: 'A basic image editor with upload, crop, resize, brightness/contrast, and export.',
  icon: './icon.svg', // We'll create a placeholder later if needed
  route: '/tools/image-editor',
  quotaHook: 'noop',
  tags: ['image', 'editor'],
  enabled: true,
};

export function init(): Promise<void> | void {
  // No-op for now; could be used for setting up state, etc.
  return;
}

export function render(): unknown {
  return <ImageEditor />;
}

export function dispose(): Promise<void> | void {
  // No-op for now.
  return;
}

const entryPoint: ToolEntryPoint = {
  manifest,
  init,
  render,
  dispose,
};

export default entryPoint;