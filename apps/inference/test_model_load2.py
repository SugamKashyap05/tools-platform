import os
import torch
from realesrgan.utils import RealESRGANer, load_file_from_url

# Define the model URL and path
model_name = 'RealESRGAN_x2.pth'
model_dir = os.path.join('weights')
model_path = os.path.join(model_dir, model_name)

# Create the directory if it doesn't exist
os.makedirs(model_dir, exist_ok=True)

# If the model file doesn't exist, try to download it from a few possible URLs
if not os.path.exists(model_path):
    print(f"Model not found at {model_path}. Attempting to download...")
    urls = [
        f'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/{model_name}',
        f'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/{model_name}',
        f'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/{model_name}'
    ]
    for url in urls:
        try:
            print(f"Trying to download from {url}")
            load_file_from_url(url, model_dir=model_dir, progress=True, file_name=model_name)
            # If we get here, the download succeeded
            print(f"Successfully downloaded {model_name} from {url}")
            break
        except Exception as e:
            print(f"Failed to download from {url}: {e}")
            continue
else:
    print(f"Model already exists at {model_path}")

# Now try to initialize the model
try:
    upscale_model = RealESRGANer(
        scale=2,
        model_path=model_path,
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