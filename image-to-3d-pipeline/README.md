# Image-to-3D Pipeline for 3D Printing Business

Production-ready pipeline for converting product images to printable 3D models with automatic business calculations (pricing, SKU generation, cost estimation).

## Features

### Technical Features
- **GPU/CPU Auto-Detection**: Automatically uses CUDA if available, falls back to CPU
- **Advanced Depth Estimation**: Uses MiDaS DPT-Large for high-quality depth maps
- **Professional Mesh Processing**: Poisson surface reconstruction with watertight mesh generation
- **3D Printing Optimization**: Auto-orientation, wall thickness checking, manifold fixing
- **Background Removal**: Automatic background removal with alpha matting
- **Batch Processing**: Process entire folders with progress tracking and resume capability

### Business Features
- **Automatic SKU Generation**: DATE-CATEGORY-NUMBER format
- **Cost Calculation**: Material usage (PLA), weight, and total cost
- **Pricing Recommendations**: Automatic retail price calculation with configurable markup
- **Print Time Estimation**: Based on geometry and print settings
- **Professional Exports**: STL files, preview renders, thumbnails, and metadata JSON
- **Batch Reports**: CSV reports with all metrics for batch operations

## Installation

### System Requirements
- Python 3.8+
- CUDA-capable GPU (optional, but recommended)
- 8GB+ RAM (16GB+ recommended)

### Quick Start

1. **Navigate to project directory**:
   ```bash
   cd image-to-3d-pipeline
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Place images in input folder**:
   ```bash
   cp your-product-image.jpg input/
   ```

4. **Run pipeline**:
   ```bash
   # Single image
   python image_to_3d.py --image input/your-product-image.jpg

   # Batch processing
   python image_to_3d.py --batch
   ```

## Usage

### Single Image Processing

```bash
python image_to_3d.py --image input/product.jpg --category DECO
```

**Arguments**:
- `--image`: Path to image file
- `--category`: Product category for SKU (default: PROD)
- `--config`: Custom config file (default: config.yaml)

### Batch Processing

```bash
python image_to_3d.py --batch --input-dir input
```

**Arguments**:
- `--batch`: Enable batch mode
- `--input-dir`: Input directory (default: input)

**Features**:
- Processes all supported images in the folder
- Shows progress bar with ETA
- Automatically resumes from last processed image on interruption
- Generates comprehensive CSV report
- Desktop notification on completion

### Supported Image Formats
- JPG/JPEG
- PNG
- HEIC (iPhone photos)
- WebP

## Output Files

For each processed image, the pipeline generates:

### 3D Model
- `output/stl/{SKU}.stl` - Printable STL file (binary, in millimeters)

### Visualizations
- `output/previews/{SKU}_thumbnail.png` - Marketplace thumbnail (512x512)
- `output/previews/{SKU}_preview_0.png` - 4 preview renders from different angles
- `output/previews/{SKU}_preview_1.png`
- `output/previews/{SKU}_preview_2.png`
- `output/previews/{SKU}_preview_3.png`

### Metadata
- `output/reports/{SKU}_metadata.json` - Complete processing metadata including:
  - Business metrics (cost, pricing, profit)
  - Mesh statistics (vertices, faces, dimensions)
  - Processing information (time, device, settings)
  - File paths to all outputs

### Batch Reports
- `output/reports/batch_report.csv` - Summary of all processed items with:
  - SKU, source image, processing time
  - Volume, weight, costs
  - Retail price, profit margin
  - Print time estimation

## Configuration

Edit `config.yaml` to customize:

### Processing Settings
```yaml
preprocessing:
  target_resolution: 1024  # 512, 1024, or 2048
  background_removal:
    enabled: true
    alpha_matting: true
```

### 3D Printing
```yaml
printing:
  max_dimension_mm: 100  # Scale all models to this size
  min_wall_thickness_mm: 2.0
  auto_orient: true  # Optimize for minimal supports
```

### Business Settings
```yaml
business:
  pricing:
    pla_cost_per_gram: 0.02  # EUR per gram
    retail_markup: 5.0  # 5x cost
    fixed_cost_per_print: 2.00  # EUR per print
  sku:
    default_category: "PROD"
```

### Performance
```yaml
system:
  device: "auto"  # auto, cuda, or cpu
  num_threads: 4  # CPU threads
```

## Business Calculations

### Material Cost
```
Volume (cm³) = Mesh volume / 1000
Weight (g) = Volume × PLA density (1.24 g/cm³)
Material Cost = Weight × Cost per gram
Total Cost = Material Cost + Fixed Cost
```

### Pricing
```
Retail Price = Total Cost × Markup (default: 5x)
Profit = Retail Price - Total Cost
```

### Print Time
```
Layers = Height / Layer Height
Print Time = (Perimeter Length × Layers) / Speed × Support Multiplier
```

## Workflow Example

```bash
# 1. Add product images
cp photos/*.jpg input/

# 2. Run batch processing
python image_to_3d.py --batch

# 3. Check results
cat output/reports/batch_report.csv

# 4. Upload STL files to your 3D printer
ls output/stl/

# 5. Use thumbnails for your online store
ls output/previews/*thumbnail.png
```

## Output Example

```
================================================================================
Processing: input/vase.jpg
================================================================================

[1/7] Preprocessing image...
INFO: Loaded image: input/vase.jpg (2048x2048)
INFO: Removing background...
INFO: Background removed successfully
INFO: Image centered and padded
INFO: Resized image to 1024x1024

[2/7] Estimating depth...
INFO: Loading MiDaS model: DPT_Large...
INFO: MiDaS model loaded successfully
INFO: Estimating depth...
INFO: Depth estimation completed

[3/7] Generating mesh...
INFO: Converting depth map to point cloud...
INFO: Point cloud created with 1048576 points
INFO: Reconstructing surface...
INFO: Surface reconstructed: 52847 vertices, 105234 faces
INFO: Simplifying mesh from 105234 to 50000 faces...
INFO: Mesh simplified: 50000 faces
INFO: Making mesh watertight...
INFO: Mesh is watertight

[4/7] Optimizing for 3D printing...
INFO: Non-manifold geometry fixed
INFO: Mesh scaled to max dimension: 100mm
INFO: Mesh oriented for minimal supports
INFO: Wall thickness check passed (min edge: 2.34mm)

[5/7] Calculating business metrics...
INFO: Volume: 45723.45 mm³
INFO: Material: 56.70g PLA, Cost: €3.13
INFO: Estimated print time: 4.2 hours
INFO: Generated SKU: 20231116-PROD-001
INFO: Recommended retail price: €15.67

[6/7] Exporting files...
INFO: STL exported: output/stl/20231116-PROD-001.stl
INFO: Generated 4 preview images
INFO: Thumbnail generated: output/previews/20231116-PROD-001_thumbnail.png

[7/7] Generating metadata...
INFO: Metadata exported: output/reports/20231116-PROD-001_metadata.json

================================================================================
PROCESSING COMPLETE
================================================================================
SKU: 20231116-PROD-001
Processing time: 47.3s
STL file: output/stl/20231116-PROD-001.stl
Volume: 45.72 cm³
Weight: 56.70g
Cost: €3.13
Retail price: €15.67
Print time: 4.2h
================================================================================
```

## Error Handling

The pipeline includes robust error handling:

### GPU Out of Memory
- Automatically retries with CPU
- Reduces resolution if needed
- Configurable in `config.yaml`

### Corrupted Images
- Logs error and continues with next image
- Skips corrupted files in batch mode
- Saves error report to `logs/errors.json`

### Resume Capability
- Batch processing can be interrupted (Ctrl+C)
- Automatically resumes from last processed image
- State saved in `logs/batch_state.json`

## Logging

Logs are saved to:
- `logs/pipeline.log` - Detailed processing log
- `logs/sku_counter.txt` - SKU counter for unique IDs
- `logs/batch_state.json` - Batch processing state
- `logs/errors.json` - Error reports

## Project Structure

```
image-to-3d-pipeline/
├── input/                  # Place images here
├── processing/             # Temporary processing files
├── output/
│   ├── stl/               # Exported STL files
│   ├── previews/          # Thumbnails and preview renders
│   └── reports/           # Metadata JSON and batch CSV
├── logs/                   # Log files and state
├── config.yaml            # Configuration file
├── requirements.txt       # Python dependencies
├── image_to_3d.py        # Main pipeline script
└── README.md             # This file
```

## Performance Tips

### For Best Quality
```yaml
preprocessing:
  target_resolution: 2048

mesh_generation:
  simplification:
    mode: "detailed"
    target_faces_detailed: 100000
```

### For Speed
```yaml
preprocessing:
  target_resolution: 512

mesh_generation:
  simplification:
    mode: "simple"
    target_faces_simple: 10000
```

### For Low VRAM GPUs (<4GB)
```yaml
preprocessing:
  target_resolution: 512

depth_estimation:
  model: "DPT_Hybrid"  # Smaller model
```

## Troubleshooting

### Issue: "CUDA out of memory"
**Solution**: Reduce `target_resolution` to 512 or use CPU mode

### Issue: "Mesh not watertight"
**Solution**: Increase `poisson.depth` to 10-11 for more detail

### Issue: "Model too small/large"
**Solution**: Adjust `printing.max_dimension_mm` in config

### Issue: "Background not removed properly"
**Solution**: Adjust `background_removal` thresholds in config

## License

Commercial use allowed. Modify as needed for your business.

## Support

For issues and feature requests, check the logs in `logs/pipeline.log`

## Version

1.0.0 - Production Release
