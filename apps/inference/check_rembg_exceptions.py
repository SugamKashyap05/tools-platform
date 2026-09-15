import rembg
# Check what exception classes are available in rembg
for attr in dir(rembg):
    obj = getattr(rembg, attr)
    if isinstance(obj, type) and issubclass(obj, BaseException):
        print(f"Found exception class in rembg: {attr}")