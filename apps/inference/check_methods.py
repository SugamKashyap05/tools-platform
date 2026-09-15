from realesrgan import RealESRGANer
import inspect
# Create an instance (we need a model path, but we can check the class without loading)
# We'll just check the class methods
print("Methods of RealESRGANer:")
methods = [method for method in dir(RealESRGANer) if not method.startswith('_')]
print(methods)
# Check for predict or enhance
for m in methods:
    if 'predict' in m.lower() or 'enhance' in m.lower():
        print(f"Found method: {m}")