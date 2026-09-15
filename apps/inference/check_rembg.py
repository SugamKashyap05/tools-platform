import rembg
print("Available attributes in rembg:")
for attr in dir(rembg):
    if not attr.startswith('_'):
        print(f"  {attr}: {getattr(rembg, attr)}")
# Check for exceptions
print("\nChecking for exceptions:")
if hasattr(rembg, 'exceptions'):
    print("  rembg.exceptions exists")
    import rembg.exceptions
    print("  Attributes in rembg.exceptions:", [x for x in dir(rembg.exceptions) if not x.startswith('_')])
else:
    print("  rembg.exceptions does not exist")
    # Maybe the exceptions are in the main module?
    # Let's see if there are any exception classes in rembg
    for attr in dir(rembg):
        obj = getattr(rembg, attr)
        if isinstance(obj, type) and issubclass(obj, BaseException):
            print(f"  Found exception class: {attr}")