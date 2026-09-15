import pytest
import os
import sys
from fastapi.testclient import TestClient
from io import BytesIO
from PIL import Image

@pytest.fixture(scope="session")
def client():
    # Patch the RealESRGANer to avoid loading weights
    import realesrgan.utils
    def mock_init(self, scale, model_path, dni_weight, model, tile, tile_pad, pre_pad, half, device):
        # Do nothing, just set the device and scale
        self.scale = scale
        self.device = device
        # We don't load the model, so we set the model to None
        self.model = model
    # Patch the __init__ method
    realesrgan.utils.RealESRGANer.__init__ = mock_init

    # Also, we need to patch the enhance method to return a dummy image
    def mock_enhance(self, img, outscale=None):
        # Return the same image and a dummy status
        return img, False
    realesrgan.utils.RealESRGANer.enhance = mock_enhance

    # Now import main
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from main import app
    return TestClient(app)

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "models" in data
    assert "version" in data

def test_invalid_style(client):
    # Create a dummy image file
    img = Image.new('RGB', (10, 10), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    response = client.post(
        "/style-transfer",
        files={"file": ("test.png", img_bytes, "image/png")},
        data={"style": "invalid_style"}
    )
    assert response.status_code == 400
    assert "Invalid style name" in response.json()["detail"]

def test_valid_style_missing_file(client):
    # No file provided
    response = client.post(
        "/style-transfer",
        data={"style": "candy"}
    )
    # Should be 422 because file is required
    assert response.status_code == 422

def test_file_too_large(client):
    # Create a file larger than 5 MiB
    large_content = b"x" * (6 * 1024 * 1024)  # 6 MiB
    img_bytes = BytesIO(large_content)
    
    response = client.post(
        "/remove-background",
        files={"file": ("large.png", img_bytes, "image/png")}
    )
    assert response.status_code == 413
    assert "File too large" in response.json()["detail"]