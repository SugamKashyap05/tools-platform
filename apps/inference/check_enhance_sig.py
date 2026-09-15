from realesrgan import RealESRGANer
import inspect
# Get the signature of the enhance method
sig = inspect.signature(RealESRGANer.enhance)
print("RealESRGANer.enhance signature:", sig)
# Also, let's see if we can get the docstring
print("RealESRGANer.enhance docstring:", RealESRGANer.enhance.__doc__)