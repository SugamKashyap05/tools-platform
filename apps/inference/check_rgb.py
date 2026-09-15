import torchvision.transforms as T
print(hasattr(T, 'rgb_to_grayscale'))
if hasattr(T, 'rgb_to_grayscale'):
    print('Found in transforms')
    print(T.rgb_to_grayscale)
else:
    print('Not found in transforms')
    # Check submodules
    import torchvision.transforms.functional as TF
    print(hasattr(TF, 'rgb_to_grayscale'))
    if hasattr(TF, 'rgb_to_grayscale'):
        print('Found in transforms.functional')
        print(TF.rgb_to_grayscale)
    else:
        print('Not found in transforms.functional')
        # Check _functional
        try:
            import torchvision.transforms._functional_tensor as FTT
            print(hasattr(FTT, 'rgb_to_grayscale'))
            if hasattr(FTT, 'rgb_to_grayscale'):
                print('Found in transforms._functional_tensor')
                print(FTT.rgb_to_grayscale)
            else:
                print('Not found in transforms._functional_tensor')
        except Exception as e:
            print('Error importing _functional_tensor:', e)