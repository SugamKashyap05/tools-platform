import torchvision.transforms
print([attr for attr in dir(torchvision.transforms) if 'functional' in attr.lower()])