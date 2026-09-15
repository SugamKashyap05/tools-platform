import os
from realesrgan.utils import RealESRGANer
import torch

# Check if the weights file exists
weights_path = 'weights/RealESRGAN_x2.pth'
if not os.path.exists(weights_path):
    print(f"Weights file not found at {weights_path}")
    # We might need to create the directory and download
    os.makedirs(os.path.dirname(weights_path), exist_ok=True)
    # Try to download using torch.hub or the load_file_from_url function
    from realesrgan.utils import load_file_from_url
    # The URL for the RealESRGAN_x2.pth model
    url = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2.pth'
    print(f"Downloading from {url} to {weights_path}")
    load_file_from_url(url, model_dir=os.path.dirname(weights_path), progress=True, file_name=os.path.basename(weights_path))
else:
    print(f"Weights file found at {weights_path}")

# Now try to initialize the model
try:
    upscale_model = RealESRGANer(
        scale=2,
        model_path=weights_path,
        dni_weight=None,
        model=None,
        tile=0,
        tile_pad=10,
        pre_pad=10,
        half=False,
        device='cuda' if torch.cuda.is_available() else 'cpu'
    )
    print("Model initialized successfully")
except Exception as e:
    print(f"Error initializing model: {e}")
    # Maybe we need to call a load method? Let's check if there is a load_weights method
    if hasattr(upscale_model, 'load_weights'):
        print("Model has load_weights method")
    else:
        print("Model does not have load_weights method")