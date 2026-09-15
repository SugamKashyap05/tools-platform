import React, { useState, useRef, useCallback } from 'react';

type EditorState = {
  imageSrc: string | null;
  editedImageSrc: string | null;
};

export const ImageEditor: React.FC = () => {
  const [state, setState] = useState<EditorState>({
    imageSrc: null,
    editedImageSrc: null,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const imageRef = useRef<HTMLImageElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const loadImage = useCallback((file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const result = e.target?.result as string;
      setState({
        imageSrc: result,
        editedImageSrc: result,
      });
    };
    reader.readAsDataURL(file);
  }, []);

  const resetCanvas = useCallback(() => {
    if (state.imageSrc) {
      setState((prev) => ({ ...prev, editedImageSrc: state.imageSrc }));
    }
  }, [state.imageSrc]);

  const applyCrop = useCallback(() => {
    if (!state.editedImageSrc) return;
    const img = new Image();
    img.src = state.editedImageSrc;
    img.onload = () => {
      const x = parseInt(prompt('Crop X:', '0') || '0');
      const y = parseInt(prompt('Crop Y:', '0') || '0');
      const width = parseInt(prompt('Crop Width:', String(img.width)) || String(img.width));
      const height = parseInt(prompt('Crop Height:', String(img.height)) || String(img.height));

      const canvas = canvasRef.current;
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      canvas.width = width;
      canvas.height = height;
      ctx.drawImage(img, x, y, width, height, 0, 0, width, height);
      setState((prev) => ({ ...prev, editedImageSrc: canvas.toDataURL() }));
    };
  }, [state.editedImageSrc]);

  const applyResize = useCallback(() => {
    if (!state.editedImageSrc) return;
    const img = new Image();
    img.src = state.editedImageSrc;
    img.onload = () => {
      const width = parseInt(prompt('Resize Width:', String(img.width)) || String(img.width));
      const height = parseInt(prompt('Resize Height:', String(img.height)) || String(img.height));

      const canvas = canvasRef.current;
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      canvas.width = width;
      canvas.height = height;
      ctx.drawImage(img, 0, 0, width, height);
      setState((prev) => ({ ...prev, editedImageSrc: canvas.toDataURL() }));
    };
  }, [state.editedImageSrc]);

  const applyBrightnessContrast = useCallback(() => {
    if (!state.editedImageSrc) return;
    const img = new Image();
    img.src = state.editedImageSrc;
    img.onload = () => {
      const brightness = parseInt(prompt('Brightness (-255 to 255):', '0') || '0');
      const contrast = parseInt(prompt('Contrast (-100 to 100):', '0') || '0');

      const canvas = canvasRef.current;
      if (!canvas) return;
      const ctxRaw = canvas.getContext('2d');
      if (!ctxRaw) return;
      const ctx = ctxRaw as CanvasRenderingContext2D;

      // Draw image to canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0);
      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const data = imageData.data;

      for (let i = 0; i < data.length; i += 4) {
        const r = data[i]!;
        const g = data[i + 1]!;
        const b = data[i + 2]!;

        let nr = r + brightness;
        let ng = g + brightness;
        let nb = b + brightness;

        nr = ((nr / 255 - 0.5) * contrast) * 255 + 255 / 2;
        ng = ((ng / 255 - 0.5) * contrast) * 255 + 255 / 2;
        nb = ((nb / 255 - 0.5) * contrast) * 255 + 255 / 2;

        nr = Math.max(0, Math.min(255, nr));
        ng = Math.max(0, Math.min(255, ng));
        nb = Math.max(0, Math.min(255, nb));

        data[i] = nr;
        data[i + 1] = ng;
        data[i + 2] = nb;
      }

      ctx.putImageData(imageData, 0, 0);
      setState((prev) => ({ ...prev, editedImageSrc: canvas.toDataURL() }));
    };
  }, [state.editedImageSrc]);

  const exportImage = useCallback(() => {
    if (!state.editedImageSrc) return;
    const link = document.createElement('a');
    link.href = state.editedImageSrc;
    link.download = 'edited-image.png';
    link.click();
  }, [state.editedImageSrc]);

  // Convert a string (data URL or blob URL) to a Blob
  const imageSrcToBlob = useCallback(async (src: string): Promise<Blob> => {
    if (src.startsWith('blob:')) {
      const response = await fetch(src);
      if (!response.ok) {
        throw new Error(`Failed to fetch blob: ${response.status}`);
      }
      return await response.blob();
    } else {
      // Assume data URL
      const arr = src.split(',');
      if (arr.length < 2) {
        throw new Error('Invalid data URL');
      }
      let match = null;
      if (src.startsWith('data:')) {
        match = src.match(/^data:([^;]+);/);
      }
      let mime = 'application/octet-stream';
      if (match && match[1]) {
        mime = match[1];
      }
      const bstr = atob(arr[1] as string);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new Blob([u8arr], { type: mime });
    }
  }, []);

  const handleRemoveBackground = useCallback(async () => {
    if (!state.editedImageSrc) return;
    setLoading(true);
    setError(null);
    try {
      const blob = await imageSrcToBlob(state.editedImageSrc);
      const formData = new FormData();
      formData.append('file', blob, 'image.png');
      const response = await fetch('http://localhost:8000/remove-background', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const resultBlob = await response.blob();
      const resultUrl = URL.createObjectURL(resultBlob);
      setState(prev => ({ ...prev, editedImageSrc: resultUrl }));
    } catch (err: any) {
      setError(err.message);
      alert(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }, [state.editedImageSrc, imageSrcToBlob]);

  const handleUpscale = useCallback(async () => {
    if (!state.editedImageSrc) return;
    setLoading(true);
    setError(null);
    try {
      const blob = await imageSrcToBlob(state.editedImageSrc);
      const formData = new FormData();
      formData.append('file', blob, 'image.png');
      const response = await fetch('http://localhost:8000/upscale', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const resultBlob = await response.blob();
      const resultUrl = URL.createObjectURL(resultBlob);
      setState(prev => ({ ...prev, editedImageSrc: resultUrl }));
    } catch (err: any) {
      setError(err.message);
      alert(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }, [state.editedImageSrc, imageSrcToBlob]);

  const handleStyleTransfer = useCallback(async () => {
    if (!state.editedImageSrc) return;
    const style = prompt('Enter style (candy, mosaic, rain-princess, udnie):', 'candy');
    if (!style) return; // user cancelled
    const allowedStyles = ['candy', 'mosaic', 'rain-princess', 'udnie'];
    if (!allowedStyles.includes(style)) {
      alert('Invalid style. Please choose from: candy, mosaic, rain-princess, udnie');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const blob = await imageSrcToBlob(state.editedImageSrc);
      const formData = new FormData();
      formData.append('file', blob, 'image.png');
      formData.append('style', style);
      const response = await fetch('http://localhost:8000/style-transfer', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const resultBlob = await response.blob();
      const resultUrl = URL.createObjectURL(resultBlob);
      setState(prev => ({ ...prev, editedImageSrc: resultUrl }));
    } catch (err: any) {
      setError(err.message);
      alert(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }, [state.editedImageSrc, imageSrcToBlob]);

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h2>Image Editor</h2>
      <div>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => {
            const file = e.target?.files?.[0];
            if (file) loadImage(file);
          }}
        />
        <button onClick={resetCanvas} disabled={!state.imageSrc || loading}>
          Reset
        </button>
      </div>
      <div style={{ marginTop: '20px' }}>
        {state.editedImageSrc ? (
          <img src={state.editedImageSrc} alt="Edited" style={{ maxWidth: '100%', border: '1px solid #ccc' }} />
        ) : (
          <p>No image loaded</p>
        )}
      </div>
      <div style={{ marginTop: '20px' }}>
        <button onClick={applyCrop} disabled={!state.editedImageSrc || loading}>
          Crop
        </button>
        <button onClick={applyResize} disabled={!state.editedImageSrc || loading}>
          Resize
        </button>
        <button onClick={applyBrightnessContrast} disabled={!state.editedImageSrc || loading}>
          Adjust
        </button>
        <button onClick={exportImage} disabled={!state.editedImageSrc || loading}>
          Export
        </button>
        <button onClick={handleRemoveBackground} disabled={!state.editedImageSrc || loading} style={{ marginLeft: '10px' }}>
          Remove Background
        </button>
        <button onClick={handleUpscale} disabled={!state.editedImageSrc || loading} style={{ marginLeft: '10px' }}>
          Upscale
        </button>
        <button onClick={handleStyleTransfer} disabled={!state.editedImageSrc || loading} style={{ marginLeft: '10px' }}>
          Style Transfer
        </button>
      </div>
      {error && (
        <div style={{ marginTop: '10px', color: 'red' }}>
          Error: {error}
        </div>
      )}
    </div>
  );
};