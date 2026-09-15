import type { NextPage } from 'next'
import React from 'react'
import entryPoint from '@repo/image-editor'

const ImageEditorPage: NextPage = () => {
  const Element = entryPoint.render() as React.ReactNode
  return <>{Element}</>
}

export default ImageEditorPage