# Inference Service

A local FastAPI service for image processing tasks: background removal, upscaling, and style transfer.

## Models Used

1. **Background Removal (`/remove-background`)**
   - **Model**: U2Net (via [rembg](https://github.com/danielgatis/rembg))
   - **Why**: High accuracy, open-source, and lightweight enough for local use. rembg handles model loading automatically.

2. **Upscaling (`/upscale`)**
   - **Model**: Real-ESRGAN (x2 scale)
   - **Why**: State-of-the-art for real-world image upscaling, preserves details well. The `realesrgan` package provides easy integration.

3. **Style Transfer (`/style-transfer`)**
   - **Model**: Neural style transfer using VGG19 features (lightweight implementation)
   - **Why**: For a truly lightweight dependency, we avoid heavy style transfer models (e.g., Arbitrary Style Transfer) and instead use a classic optimization-based approach with VGG19. This is suitable for demonstration and low-resource environments. For production, consider a pre-trained fast style transfer model (e.g., from [torch-hub](https://pytorch.org/hub/)).

## Setup

1. **Clone the repository** (if not already done)
2. Navigate to the `apps/inference` directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Note: The first run will download model weights (U2Net, RealESRGAN_x2.pth) and may take a moment.

## Running the Service

```bash
uvicorn main:app --reload
```
The service will be available at `http://localhost:8000`.

## API Endpoints

All endpoints expect a multipart/form-data file upload with key `file` and return a PNG image.

- **POST /remove-background**
  - Removes the background from the input image.
  - Returns: PNG with transparent background.

- **POST /upscale**
  - Upscales the input image by 2x.
  - Returns: Upscaled PNG.

- **POST /style-transfer**
  - Applies neural style transfer using one of the allowed style images.
  - **Allowed styles**: candy, mosaic, rain-princess, udnie
  - Returns: Stylized PNG.

- **GET /health**
  - Health check endpoint.
  - Returns: JSON with service status and model loading information.

## Notes

- The service runs entirely locally; no external API calls are made.
- Model weights are cached locally after first download.
- For style transfer, we use a fixed set of style images located in the `styles/` directory.
  To add a new style, place a `<style_name>.jpg` file in `styles/` and add the style name to the allowed list in the code.
- The service implements security measures:
  - Input validation for file size (max 5 MiB)
  - Allowlist validation for style names to prevent path traversal
  - CORS middleware configured for local development origins
  - Generic error messages to avoid leaking internal details
- The style transfer implementation is intentionally lightweight for accessibility. For higher quality/faster style transfer, consider integrating a model like [Fast Neural Style](https://github.com/pytorch/examples/tree/main/fast_neural_style).

## Troubleshooting

- **CUDA not available**: The service will fall back to CPU. Processing will be slower.
- **Model download fails**: Check internet connection and permissions to write to the cache directory (usually `~/.cache`).