#!/bin/bash

# Example usage scripts for Image-to-3D Pipeline

echo "==========================================="
echo "Image-to-3D Pipeline - Usage Examples"
echo "==========================================="
echo ""

# Example 1: Process a single decorative item
echo "Example 1: Process single decorative vase"
echo "Command: python image_to_3d.py --image input/vase.jpg --category DECO"
echo ""

# Example 2: Process all images in batch
echo "Example 2: Batch process all product images"
echo "Command: python image_to_3d.py --batch"
echo ""

# Example 3: Process with custom config
echo "Example 3: Process with high quality settings"
echo "Command: python image_to_3d.py --image input/product.jpg --config config_highquality.yaml"
echo ""

# Example 4: Check outputs
echo "Example 4: View generated files"
echo "Command: ls -lh output/stl/"
echo "Command: ls -lh output/previews/"
echo "Command: cat output/reports/batch_report.csv"
echo ""

# Example 5: Validate STL file
echo "Example 5: Validate STL is printable"
echo "You can use various tools to validate:"
echo "  - Open in PrusaSlicer / Cura"
echo "  - Upload to your 3D printer management software"
echo "  - Use online validators"
echo ""

echo "==========================================="
echo "Quick Start"
echo "==========================================="
echo ""
echo "1. Add images to input folder:"
echo "   cp ~/Downloads/product-photo.jpg input/"
echo ""
echo "2. Run pipeline:"
echo "   python image_to_3d.py --batch"
echo ""
echo "3. Find your STL files:"
echo "   ls output/stl/"
echo ""
echo "4. Check the report:"
echo "   cat output/reports/batch_report.csv"
echo ""
echo "==========================================="
