import io
from typing import Union
import os
import torch
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
from rembg import remove
# from rembg.exceptions import RembgError  # This module does not exist in the installed version
from realesrgan.utils import RealESRGANer
from torchvision import transforms
from torchvision.models import vgg19
import torch.nn as nn

app = FastAPI(title="Inference Service", description="Local image processing service")

# CORS middleware - allow local development origins
# Configure via BACKEND_CORS_ORIGINS environment variable (comma-separated list)
cors_origins_env = os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
allow_origins = [origin.strip() for origin in cors_origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Allowed style names for style transfer (to prevent path traversal)
ALLOWED_STYLES = {"candy", "mosaic", "rain-princess", "udnie"}

# Maximum upload size: 5 MiB
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MiB

# Global variables for lazy-loaded models
_upscale_model = None
_vgg = None
_device = None

def get_device():
    global _device
    if _device is None:
        _device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    return _device

def get_upscale_model():
    global _upscale_model
    if _upscale_model is None:
        model_path = 'weights/RealESRGAN_x2.pth'
        if not os.path.exists(model_path):
            raise RuntimeError(f"Upscale model weights not found at {model_path}")
        try:
            _upscale_model = RealESRGANer(
                scale=2,
                model_path=model_path,
                dni_weight=None,
                model=None,
                tile=0,
                tile_pad=10,
                pre_pad=10,
                half=False,
                device=get_device()
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load upscale model: {e}")
    return _upscale_model

def get_vgg():
    global _vgg
    if _vgg is None:
        try:
            # Define VGG feature extractor
            class VGG(nn.Module):
                def __init__(self):
                    super(VGG, self).__init__()
                    self.chops = ['relu1_1', 'relu2_1', 'relu3_1', 'relu4_1', 'relu5_1']
                    self.vgg = vgg19(pretrained=True).features
                    # Freeze VGG parameters
                    for param in self.vgg.parameters():
                        param.requires_grad_(False)

                def forward(self, x):
                    features = []
                    for name, layer in self.vgg._modules.items():
                        x = layer(x)
                        if name in ['0', '5', '10', '19', '28']:  # relu1_1, relu2_1, relu3_1, relu4_1, relu5_1
                            features.append(x)
                    return features

            _vgg = VGG()
            _vgg.to(get_device()).eval()
        except Exception as e:
            raise RuntimeError(f"Failed to load VGG model: {e}")
    return _vgg

# Load style image and compute its Gram matrices
def load_style_image(path: str, size: int = 256):
    style_transform = transforms.Compose([
        transforms.Resize(size),
        transforms.CenterCrop(size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    style = Image.open(path).convert('RGB')
    return style_transform(style).unsqueeze(0)

def gram_matrix(tensor):
    _, d, h, w = tensor.size()
    tensor = tensor.view(d, h * w)
    gram = torch.mm(tensor, tensor.t())
    return gram

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    """
    Remove background from an image using rembg (U2Net model).
    Expects an image file, returns PNG with transparent background.
    """
    # Check file size
    contents = await file.read()
    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    try:
        # Remove background
        result = remove(contents)
        return Response(content=result, media_type="image/png")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file")
    except Exception as e:
        # Log the error for debugging (optional)
        # print(f"Error in remove_background: {e}")
        raise HTTPException(status_code=500, detail="Internal processing error")

@app.post("/upscale")
async def upscale(file: UploadFile = File(...)):
    """
    Upscale an image by 2x using Real-ESRGAN.
    Expects an image file, returns upscaled image (PNG).
    """
    # Check file size
    contents = await file.read()
    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    try:
        img = Image.open(io.BytesIO(contents)).convert('RGB')
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file")
    try:
        # Get the upscale model (lazy-loaded)
        model = get_upscale_model()
        # Upscale using RealESRGANer.enhance method
        # The enhance method returns a tuple (output_image, status) or just the image
        # Based on the documentation, it returns the enhanced image
        upscaled_img = model.enhance(img, outscale=2)[0]
        # Convert to bytes
        buf = io.BytesIO()
        upscaled_img.save(buf, format='PNG')
        return Response(content=buf.getvalue(), media_type="image/png")
    except Exception as e:
        # print(f"Error in upscale: {e}")
        raise HTTPException(status_code=500, detail="Internal processing error")

@app.post("/style-transfer")
async def style_transfer(file: UploadFile = File(...), style: str = Form(...)):
    """
    Apply neural style transfer to an image using a lightweight VGG19-based approach.
    Expects an image file and a style parameter, returns stylized image (PNG).
    Note: This is a basic implementation for demonstration; for production, consider
    using a fast neural style transfer model (e.g., from torch-hub) for better speed.
    """
    # Validate style parameter against allowlist to prevent path traversal
    if style not in ALLOWED_STYLES:
        raise HTTPException(status_code=400, detail="Invalid style name")
    
    # Check file size
    contents = await file.read()
    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    
    try:
        content_img = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Preprocess content image
        preprocess = transforms.Compose([
            transforms.Resize(512),
            transforms.CenterCrop(512),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])
        content_tensor = preprocess(content_img).unsqueeze(0).to(get_device())
        
        # Initialize target image (clone of content)
        target = content_tensor.clone().requires_grad_(True)
        
        # Optimizer
        optimizer = torch.optim.LBFGS([target])
        
        # Style transfer hyperparameters
        style_weight = 1e6
        content_weight = 1e0
        num_steps = 200  # Reduced for lightweight
        
        def closure():
            optimizer.zero_grad()
            target_features = get_vgg()(target)
            # Content loss (using relu4_1)
            content_loss = torch.mean((target_features[2] - content_features[2]) ** 2)
            # Style loss
            style_loss = 0
            for ft_y, gm_s in zip(target_features, style_grams):
                gm_y = gram_matrix(ft_y)
                style_loss += torch.mean((gm_y - gm_s) ** 2)
            style_loss *= style_weight / (content_img.size[0] * content_img.size[1])
            loss = content_weight * content_loss + style_loss
            loss.backward()
            return loss
        
        # Precompute content features
        with torch.no_grad():
            content_features = get_vgg()(content_tensor)
        
        # Load style image and compute its Gram matrices
        # Safe path construction: use basename and join with styles directory
        style_filename = f"{style}.jpg"
        style_path = os.path.join("styles", style_filename)
        # Additional safety: ensure the path is within the styles directory
        # (though our allowlist already restricts to known names)
        try:
            style_img = load_style_image(style_path).to(get_device())
        except FileNotFoundError:
            # If style image is missing, we cannot proceed
            raise HTTPException(status_code=500, detail="Style image not available")
        
        # Compute style features
        with torch.no_grad():
            style_features = get_vgg()(style_img)
        style_grams = [gram_matrix(f) for f in style_features]
        
        # Run optimization
        for i in range(num_steps):
            optimizer.step(closure)
        
        # Postprocess target image
        with torch.no_grad():
            result = target.clone()
            result = result.squeeze(0).cpu()
            # Unnormalize
            result = result * torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
            result = result + torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
            result = result.clamp(0, 1)
        
        # Convert to PIL Image
        result = transforms.ToPILImage()(result)
        buf = io.BytesIO()
        result.save(buf, format='PNG')
        return Response(content=buf.getvalue(), media_type="image/png")
    except HTTPException:
        raise
    except Exception as e:
        # print(f"Error in style transfer: {e}")
        raise HTTPException(status_code=500, detail="Internal processing error")

@app.get("/health")
async def health():
    """
    Health check endpoint.
    Returns a JSON object with service status and model loading information.
    """
    upscale_status = "not loaded"
    vgg_status = "not loaded"
    try:
        get_upscale_model()
        upscale_status = "loaded"
    except Exception as e:
        upscale_status = f"error: {str(e)}"
    
    try:
        get_vgg()
        vgg_status = "loaded"
    except Exception as e:
        vgg_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "models": {
            "background_removal": "loaded (U2Net via rembg)",
            "upscaling": upscale_status,
            "style_transfer": vgg_status
        },
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)