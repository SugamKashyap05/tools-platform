import sys
print(sys.path)
try:
    from torchvision.transforms import functional_tensor
    print('functional_tensor found')
except Exception as e:
    print('functional_tensor not found:', e)
try:
    from torchvision.transforms._functional_tensor import rgb_to_grayscale
    print('_functional_tensor.rgb_to_grayscale found')
except Exception as e:
    print('_functional_tensor.rgb_to_grayscale not found:', e)