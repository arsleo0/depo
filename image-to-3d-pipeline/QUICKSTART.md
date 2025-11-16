# Quick Start Guide

Get your image-to-3D pipeline running in 5 minutes!

## Installation (One-Time Setup)

### Option 1: Automated Setup (Recommended)
```bash
cd image-to-3d-pipeline
./setup.sh
```

### Option 2: Manual Setup
```bash
cd image-to-3d-pipeline
pip install -r requirements.txt
```

## Basic Usage

### Step 1: Add Your Images
```bash
# Copy your product photos to the input folder
cp ~/Downloads/product-photo.jpg input/
```

Supported formats: **JPG, PNG, HEIC** (iPhone photos), WebP

### Step 2: Run the Pipeline

#### Process a Single Image
```bash
python image_to_3d.py --image input/product-photo.jpg --category DECO
```

#### Process All Images (Batch Mode)
```bash
python image_to_3d.py --batch
```

### Step 3: Get Your Results

**STL Files** (ready for 3D printing):
```bash
ls output/stl/
# Example: 20231116-DECO-001.stl
```

**Preview Images**:
```bash
ls output/previews/
# Thumbnails and 4-angle previews for each model
```

**Business Report**:
```bash
cat output/reports/batch_report.csv
# Contains: SKU, costs, pricing, print time, profit margins
```

## What You Get

For each image processed, the pipeline automatically generates:

1. **Printable 3D Model** (STL file)
   - Watertight mesh
   - Optimized for minimal supports
   - Scaled to 100mm max dimension
   - Ready to load in your slicer

2. **Business Data**
   - Unique SKU (e.g., `20231116-DECO-001`)
   - Material cost calculation (PLA weight and price)
   - Print time estimation
   - Recommended retail price (5x markup by default)
   - Profit margin

3. **Visuals**
   - 512x512 marketplace thumbnail
   - 4 preview renders from different angles

4. **Metadata JSON**
   - Complete processing details
   - Mesh statistics
   - All business metrics

## Common Use Cases

### Use Case 1: Single Decorative Item
```bash
python image_to_3d.py --image input/vase.jpg --category DECO
```

### Use Case 2: Batch Process Product Line
```bash
# Add all product photos
cp ~/products/*.jpg input/

# Process everything
python image_to_3d.py --batch

# View report
cat output/reports/batch_report.csv
```

### Use Case 3: Different Product Categories
```bash
# Toys
python image_to_3d.py --image input/toy-car.jpg --category TOY

# Home decor
python image_to_3d.py --image input/lamp.jpg --category HOME

# Figurines
python image_to_3d.py --image input/statue.jpg --category FIG
```

## Understanding the Output

### Example Console Output
```
================================================================================
Processing: input/vase.jpg
================================================================================

[1/7] Preprocessing image...
[2/7] Estimating depth...
[3/7] Generating mesh...
[4/7] Optimizing for 3D printing...
[5/7] Calculating business metrics...
[6/7] Exporting files...
[7/7] Generating metadata...

================================================================================
PROCESSING COMPLETE
================================================================================
SKU: 20231116-DECO-001
Processing time: 47.3s
STL file: output/stl/20231116-DECO-001.stl
Volume: 45.72 cm³
Weight: 56.70g
Cost: €3.13
Retail price: €15.67
Print time: 4.2h
================================================================================
```

### CSV Report Columns
- **SKU**: Unique product identifier
- **Source Image**: Original photo filename
- **Processing Time**: How long it took to process
- **Volume**: Model volume in cm³
- **Weight**: Estimated PLA weight in grams
- **Material Cost**: Cost of PLA filament
- **Total Cost**: Material + fixed costs
- **Retail Price**: Recommended selling price
- **Profit**: Your profit margin
- **Print Time**: Estimated hours to print
- **STL File**: Path to the 3D model file

## Next Steps

### Load STL in Your Slicer
1. Open PrusaSlicer, Cura, or your preferred slicer
2. Load the STL file from `output/stl/`
3. Verify the model looks good
4. Slice and send to your 3D printer!

### Adjust Settings (Optional)
Edit `config.yaml` to customize:
- Model size: `printing.max_dimension_mm`
- Material costs: `business.pricing.pla_cost_per_gram`
- Retail markup: `business.pricing.retail_markup`
- Image quality: `preprocessing.target_resolution`

### Batch Processing Tips
- The pipeline saves progress automatically
- You can interrupt (Ctrl+C) and resume later
- Already processed images are skipped
- Get desktop notification when batch completes

## Troubleshooting

### "CUDA out of memory"
**Solution**: The pipeline will automatically retry with CPU. Or reduce resolution in config:
```yaml
preprocessing:
  target_resolution: 512  # Lower from 1024
```

### "No images found"
**Solution**: Check that images are in the `input/` folder with supported formats (jpg, png, heic)

### "Model has holes"
**Solution**: Increase Poisson depth in config:
```yaml
mesh_generation:
  poisson:
    depth: 10  # Higher = more detail
```

## Performance Expectations

### With GPU (NVIDIA with CUDA)
- **Single image**: 30-60 seconds
- **Batch (10 images)**: 5-10 minutes
- **Quality**: High (1024x1024 resolution)

### With CPU
- **Single image**: 2-5 minutes
- **Batch (10 images)**: 20-50 minutes
- **Quality**: Standard (automatically reduces to 512x512)

## Getting Help

1. Check `logs/pipeline.log` for detailed information
2. Read the full `README.md` for advanced features
3. Review example configurations in `examples.sh`

## Tips for Best Results

### Photography Tips
- **Good lighting**: Even, diffused light works best
- **Plain background**: White or neutral colors
- **Clear object**: Keep object in focus
- **Full view**: Capture the entire object
- **Center composition**: Object in center of frame

### Common Patterns
```bash
# Morning routine: Download photos from phone
adb pull /sdcard/DCIM/Camera/*.jpg input/

# Process new photos
python image_to_3d.py --batch

# Upload STLs to cloud storage for printing
rsync -av output/stl/ ~/Dropbox/3D-Models/

# Check profit margins
awk -F',' '{print $1, $9}' output/reports/batch_report.csv
```

## You're Ready!

That's it! You now have a production-ready image-to-3D pipeline for your business.

**Happy printing!** 🚀
