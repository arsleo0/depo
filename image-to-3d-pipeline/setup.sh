#!/bin/bash

# Image-to-3D Pipeline Setup Script
# Quick installation and setup

echo "==========================================="
echo "Image-to-3D Pipeline Setup"
echo "==========================================="
echo ""

# Check Python version
echo "[1/4] Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "ERROR: Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Create virtual environment (optional but recommended)
read -p "Create virtual environment? (recommended) [Y/n]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    echo "[2/4] Creating virtual environment..."
    python3 -m venv venv

    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies
echo "[3/4] Installing dependencies..."
echo "This may take a few minutes..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Verify installation
echo "[4/4] Verifying installation..."
python3 -c "import torch; print(f'PyTorch: {torch.__version__}')"
python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

echo ""
echo "==========================================="
echo "Setup Complete!"
echo "==========================================="
echo ""
echo "Next steps:"
echo "1. Place your product images in the 'input/' folder"
echo "2. Run: python image_to_3d.py --batch"
echo ""
echo "For single image:"
echo "  python image_to_3d.py --image input/your-image.jpg"
echo ""
echo "Check README.md for more information"
echo ""
