import unittest
from fastapi.testclient import TestClient
import io
from PIL import Image
import numpy as np

# Import the app from main
from main import app

class TestInferenceService(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Create a small black image for testing
        self.img = Image.new('RGB', (10, 10), color='black')
        self.img_bytes = io.BytesIO()
        self.img.save(self.img_bytes, format='PNG')
        self.img_bytes.seek(0)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("models", data)

    def test_invalid_style(self):
        # Test with an invalid style name
        response = self.client.post(
            "/style-transfer",
            files={"file": ("test.png", self.img_bytes, "image/png")},
            data={"style": "invalid_style"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json())

    def test_valid_style(self):
        # Test with a valid style (should return 200 if processing works, or 500 if style image missing)
        # We have created the style images, so it should work.
        response = self.client.post(
            "/style-transfer",
            files={"file": ("test.png", self.img_bytes, "image/png")},
            data={"style": "candy"}
        )
        # The style transfer might take a moment, but we expect a 200 if successful
        # If the style image is missing, we get 500. We have created the images, so we expect 200.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "image/png")

    def test_file_size_limit(self):
        # Create an image larger than 5 MiB
        large_img = Image.new('RGB', (3000, 3000), color='white')
        large_img_bytes = io.BytesIO()
        large_img.save(large_img_bytes, format='PNG')
        large_img_bytes.seek(0)
        # The size is about 3000*3000*3 bytes ~ 27 MiB, which is over 5 MiB
        response = self.client.post(
            "/remove-background",
            files={"file": ("large.png", large_img_bytes, "image/png")},
        )
        self.assertEqual(response.status_code, 413)
        self.assertIn("detail", response.json())

if __name__ == '__main__':
    unittest.main()