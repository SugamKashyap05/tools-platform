import realesrgan
print(dir(realesrgan))
# Check if RealESRGAN is in the package
if hasattr(realesrgan, 'RealESRGAN'):
    print("RealESRGAN is available in realesrgan")
else:
    print("RealESRGAN not found in realesrgan")
    # Check submodules
    import realesrgan.utils
    print(dir(realesrgan.utils))
    if hasattr(realesrgan.utils, 'RealESRGANer'):
        print("RealESRGANer is available in realesrgan.utils")