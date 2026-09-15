import torchvision
print('torchvision version:', torchvision.__version__)
try:
    from torchvision.transforms.functional_tensor import rgb_to_grayscale
    print('Import successful')
except Exception as e:
    print('Import failed:', e)