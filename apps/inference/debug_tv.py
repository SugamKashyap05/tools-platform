import torchvision
print('torchvision file:', torchvision.__file__)
import torchvision.transforms
print('transforms file:', torchvision.transforms.__file__)
print('Available in transforms:', [x for x in dir(torchvision.transforms) if 'functional' in x])