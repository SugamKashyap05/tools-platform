import os
from PIL import Image, ImageDraw

# Create styles directory
styles_dir = r"E:\all projects for hermes\tools-platform\apps\inference\styles"
os.makedirs(styles_dir, exist_ok=True)

# Define style colors (simple placeholders)
styles = {
    "candy": (255, 182, 193),      # Light pink
    "mosaic": (255, 165, 0),       # Orange
    "rain-princess": (147, 112, 219), # Medium purple
    "udnie": (255, 20, 147)        # Deep pink
}

# Create simple 256x256 images for each style
for style_name, color in styles.items():
    # Create image with solid color
    img = Image.new('RGB', (256, 256), color)
    draw = ImageDraw.Draw(img)
    
    # Add some simple pattern to make it more interesting
    # Draw a few shapes
    for i in range(0, 256, 32):
        for j in range(0, 256, 32):
            if (i//32 + j//32) % 2 == 0:
                draw.rectangle([i, j, i+16, j+16], fill=(255, 255, 255, 128))
    
    # Save the image
    img_path = os.path.join(styles_dir, f"{style_name}.jpg")
    img.save(img_path, "JPEG")
    print(f"Created {img_path}")

print("Style images created successfully!")