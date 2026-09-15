import torchvision
print("torchvision version:", torchvision.__version__)

# Check what's in torchvision.transforms.functional
import torchvision.transforms.functional as TF
print("Has rgb_to_grayscale in TF:", hasattr(TF, 'rgb_to_grayscale'))
if hasattr(TF, 'rgb_to_grayscale'):
    print("TF.rgb_to_grayscale:", TF.rgb_to_grayscale)

# Check what's in torchvision.transforms._functional_tensor
try:
    import torchvision.transforms._functional_tensor as FTT
    print("Has rgb_to_grayscale in _functional_tensor:", hasattr(FTT, 'rgb_to_grayscale'))
    if hasattr(FTT, 'rgb_to_grayscale'):
        print("FTT.rgb_to_grayscale:", FTT.rgb_to_grayscale)
except ImportError as e:
    print("Could not import _functional_tensor:", e)

# Check what's in torchvision.transforms._functional_pil
try:
    import torchvision.transforms._functional_pil as FTP
    print("Has rgb_to_grayscale in _functional_pil:", hasattr(FTP, 'rgb_to_grayscale'))
    if hasattr(FTP, 'rgb_to_grayscale'):
        print("FTP.rgb_to_grayscale:", FTP.rgb_to_grayscale)
except ImportError as e:
    print("Could not import _functional_pil:", e)