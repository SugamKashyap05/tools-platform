import realesrgan
attrs = [x for x in dir(realesrgan) if not x.startswith('_')]
print("Attributes:", attrs)
for attr in attrs:
    if 'RealESRGAN' in attr:
        obj = getattr(realesrgan, attr)
        print(f"{attr}: {obj} (type: {type(obj)})")
