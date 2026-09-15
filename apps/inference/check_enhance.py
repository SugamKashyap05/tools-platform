from realesrgan import RealESRGANer
import inspect
# We cannot actually create an instance without the model file, but we can inspect the class
print("RealESRGANer.enhance method:")
if hasattr(RealESRGANer, 'enhance'):
    enhance = getattr(RealESRGANer, 'enhance')
    print(f"  Method: {enhance}")
    try:
        print(f"  Signature: {inspect.signature(enhance)}")
    except Exception as e:
        print(f"  Could not get signature: {e}")
else:
    print("  enhance method not found")