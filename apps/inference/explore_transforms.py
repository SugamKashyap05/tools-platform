import torchvision.transforms as T
print("Attributes in torchvision.transforms:", [a for a in dir(T) if not a.startswith('_')])
print("\nSubmodules:")
import pkgutil
for importer, modname, ispkg in pkgutil.iter_modules(T.__path__):
    print(f"  {modname}: {'package' if ispkg else 'module'}")