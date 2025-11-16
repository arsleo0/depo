#!/usr/bin/env python3
"""
Installation Verification Script
Checks if all required dependencies are properly installed
"""

import sys

def check_module(module_name, import_name=None):
    """Check if a module can be imported"""
    if import_name is None:
        import_name = module_name

    try:
        __import__(import_name)
        print(f"✓ {module_name}")
        return True
    except ImportError as e:
        print(f"✗ {module_name} - NOT FOUND")
        print(f"  Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Image-to-3D Pipeline - Installation Verification")
    print("=" * 60)
    print()

    all_ok = True

    # Core dependencies
    print("Checking core dependencies...")
    all_ok &= check_module("PyTorch", "torch")
    all_ok &= check_module("TorchVision", "torchvision")
    all_ok &= check_module("NumPy", "numpy")
    all_ok &= check_module("SciPy", "scipy")
    all_ok &= check_module("PyYAML", "yaml")
    print()

    # Image processing
    print("Checking image processing libraries...")
    all_ok &= check_module("Pillow (PIL)", "PIL")
    all_ok &= check_module("OpenCV", "cv2")
    all_ok &= check_module("rembg", "rembg")
    all_ok &= check_module("scikit-image", "skimage")
    print()

    # 3D processing
    print("Checking 3D processing libraries...")
    all_ok &= check_module("Open3D", "open3d")
    all_ok &= check_module("Trimesh", "trimesh")
    print()

    # Utilities
    print("Checking utility libraries...")
    all_ok &= check_module("tqdm", "tqdm")
    all_ok &= check_module("Matplotlib", "matplotlib")
    all_ok &= check_module("Pandas", "pandas")
    print()

    # Optional dependencies
    print("Checking optional dependencies...")
    check_module("HEIF support", "pillow_heif")
    check_module("Notifications", "plyer")
    print()

    # Check PyTorch CUDA
    print("Checking GPU support...")
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✓ CUDA available")
            print(f"  GPU: {torch.cuda.get_device_name(0)}")
            print(f"  VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        else:
            print("⚠ CUDA not available (will use CPU)")
            print("  For better performance, install CUDA-enabled PyTorch")
    except Exception as e:
        print(f"✗ Error checking CUDA: {e}")
        all_ok = False
    print()

    # Summary
    print("=" * 60)
    if all_ok:
        print("✓ ALL REQUIRED DEPENDENCIES INSTALLED")
        print()
        print("You're ready to use the pipeline!")
        print()
        print("Quick start:")
        print("  1. Place images in input/ folder")
        print("  2. Run: python image_to_3d.py --batch")
        print()
        return 0
    else:
        print("✗ SOME DEPENDENCIES ARE MISSING")
        print()
        print("Please install missing dependencies:")
        print("  pip install -r requirements.txt")
        print()
        return 1

if __name__ == '__main__':
    sys.exit(main())
