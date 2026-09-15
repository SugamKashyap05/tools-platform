import type { NextPage } from 'next'
import { manifest as imageEditorManifest } from '@repo/image-editor'
import Link from 'next/link'

const Tools: NextPage = () => {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Tools</h1>
      <div style={{ marginTop: '20px' }}>
        <h2>{imageEditorManifest.label}</h2>
        <p>{imageEditorManifest.description}</p>
        <Link href={imageEditorManifest.route}>
          <a style={{ color: 'blue', textDecoration: 'underline' }}>Open {imageEditorManifest.label}</a>
        </Link>
      </div>
    </div>
  )
}

export default Tools
