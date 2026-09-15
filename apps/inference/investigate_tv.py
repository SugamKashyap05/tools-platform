import torchvision
print("torchvision version:", torchvision.__version__)

import torchvision.transforms as T
print("Available attributes in torchvision.transforms (non-private):")
attrs = [a for a in dir(T) if not a.startswith('_')]
print(attrs)

# Check for functional submodule
print("\nChecking for functional submodule:")
if hasattr(T, 'functional'):
    print("T.functional exists")
    import torchvision.transforms.functional as TF
    print("TF has rgb_to_grayscale:", hasattr(TF, 'rgb_to_grayscale'))
else:
    print("T.functional does not exist")

# Check for _functional_tensor
print("\nChecking for _functional_tensor:")
try:
    import torchvision.transforms._functional_tensor as FTT
    print("_functional_tensor exists")
    print("FTT has rgb_to_grayscale:", hasattr(FTT, 'rgb_to_grayscale'))
except ImportError as e:
    print("Could not import _functional_tensor:", e)

# Check for _functional_pil
print("\nChecking for _functional_pil:")
try:
    import torchvision.transforms._functional_pil as FTP
    print("_functional_pil exists")
    print("FTP has rgb_to_grayscale:", hasattr(FTP, 'rgb_to_grayscale'))
except ImportError as e:
    print("Could not import _functional_pil:", e)