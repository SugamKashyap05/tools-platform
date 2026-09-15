import realesrgan
print("Available attributes in realesrgan:")
for attr in dir(realesrgan):
    if not attr.startswith('_'):
        print(f"  {attr}: {getattr(realesrgan, attr)}")
