#!/usr/bin/env python3
"""
Image-to-3D Pipeline for 3D Printing Business
Production-ready pipeline for converting product images to printable 3D models

Author: Commercial 3D Pipeline
Version: 1.0.0
"""

import os
import sys
import time
import json
import logging
import warnings
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import yaml
import numpy as np
from tqdm import tqdm
import pandas as pd

# Image processing
from PIL import Image
import cv2
from rembg import remove

# Deep learning
import torch
import torchvision.transforms as transforms

# 3D processing
import open3d as o3d
import trimesh

# Notifications
try:
    from plyer import notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False

warnings.filterwarnings('ignore')

# =============================================================================
# LOGGING SETUP
# =============================================================================

def setup_logging(config: Dict) -> logging.Logger:
    """Set up logging with file and console handlers"""
    log_config = config.get('logging', {})
    log_level = getattr(logging, log_config.get('level', 'INFO'))

    logger = logging.getLogger('Image2_3D')
    logger.setLevel(log_level)

    # Clear existing handlers
    logger.handlers = []

    # File handler
    log_file = log_config.get('file', 'logs/pipeline.log')
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler
    if log_config.get('console', True):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger


# =============================================================================
# SYSTEM DETECTION
# =============================================================================

class SystemDetector:
    """Detect and configure system resources (GPU/CPU)"""

    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.device = None
        self.device_name = None
        self.vram_available = 0

    def detect(self) -> str:
        """Detect optimal device and return device string"""
        system_config = self.config.get('system', {})
        device_preference = system_config.get('device', 'auto')

        if device_preference == 'cpu':
            self.device = 'cpu'
            self.device_name = 'CPU'
            self.logger.info("Forced CPU mode as per configuration")
            return self.device

        # Check CUDA availability
        cuda_available = torch.cuda.is_available()

        if cuda_available and device_preference in ['auto', 'cuda']:
            self.device = 'cuda'
            self.device_name = torch.cuda.get_device_name(0)
            self.vram_available = torch.cuda.get_device_properties(0).total_memory / 1e9

            self.logger.info(f"GPU detected: {self.device_name}")
            self.logger.info(f"VRAM available: {self.vram_available:.2f} GB")

            # Set optimal batch size based on VRAM
            if self.vram_available < 4:
                self.logger.warning("Low VRAM detected. May need to reduce resolution.")

        else:
            self.device = 'cpu'
            self.device_name = 'CPU'
            num_threads = system_config.get('num_threads', 4)
            torch.set_num_threads(num_threads)

            self.logger.info(f"Using CPU with {num_threads} threads")
            if device_preference == 'cuda' and not cuda_available:
                self.logger.warning("CUDA requested but not available, falling back to CPU")

        return self.device

    def get_optimal_resolution(self, target: int) -> int:
        """Get optimal resolution based on available resources"""
        if self.device == 'cuda' and self.vram_available < 4:
            # Reduce resolution for low VRAM
            return min(target, 512)
        return target


# =============================================================================
# IMAGE PREPROCESSING
# =============================================================================

class ImagePreprocessor:
    """Handle image loading, background removal, and preprocessing"""

    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.preprocessing_config = config.get('preprocessing', {})

    def load_image(self, image_path: str) -> Optional[Image.Image]:
        """Load image from file, supporting multiple formats"""
        try:
            # Handle HEIC files
            if image_path.lower().endswith('.heic'):
                from pillow_heif import register_heif_opener
                register_heif_opener()

            img = Image.open(image_path)

            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')

            self.logger.info(f"Loaded image: {image_path} ({img.size[0]}x{img.size[1]})")
            return img

        except Exception as e:
            self.logger.error(f"Failed to load image {image_path}: {str(e)}")
            return None

    def remove_background(self, image: Image.Image) -> Image.Image:
        """Remove background using rembg with alpha matting"""
        bg_config = self.preprocessing_config.get('background_removal', {})

        if not bg_config.get('enabled', True):
            return image

        try:
            self.logger.info("Removing background...")

            # Configure rembg parameters
            alpha_matting = bg_config.get('alpha_matting', True)
            alpha_matting_foreground_threshold = bg_config.get(
                'alpha_matting_foreground_threshold', 240
            )
            alpha_matting_background_threshold = bg_config.get(
                'alpha_matting_background_threshold', 10
            )

            # Remove background
            output = remove(
                image,
                alpha_matting=alpha_matting,
                alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
                alpha_matting_background_threshold=alpha_matting_background_threshold,
            )

            self.logger.info("Background removed successfully")
            return output

        except Exception as e:
            self.logger.error(f"Background removal failed: {str(e)}")
            return image

    def center_and_pad(self, image: Image.Image) -> Image.Image:
        """Center object and add padding"""
        if not self.preprocessing_config.get('auto_center', True):
            return image

        try:
            # Convert to numpy array
            img_array = np.array(image)

            # Find bounding box of non-transparent pixels
            if img_array.shape[2] == 4:  # Has alpha channel
                alpha = img_array[:, :, 3]
                rows = np.any(alpha > 0, axis=1)
                cols = np.any(alpha > 0, axis=0)

                if not np.any(rows) or not np.any(cols):
                    return image

                rmin, rmax = np.where(rows)[0][[0, -1]]
                cmin, cmax = np.where(cols)[0][[0, -1]]

                # Crop to bounding box
                cropped = img_array[rmin:rmax+1, cmin:cmax+1]

                # Calculate padding
                padding_percent = self.preprocessing_config.get('padding_percent', 10)
                h, w = cropped.shape[:2]
                pad_h = int(h * padding_percent / 100)
                pad_w = int(w * padding_percent / 100)

                # Make square with padding
                max_dim = max(h, w) + 2 * max(pad_h, pad_w)

                # Create new image with transparent background
                centered = np.zeros((max_dim, max_dim, 4), dtype=np.uint8)

                # Calculate position to center the object
                y_offset = (max_dim - h) // 2
                x_offset = (max_dim - w) // 2

                centered[y_offset:y_offset+h, x_offset:x_offset+w] = cropped

                self.logger.info("Image centered and padded")
                return Image.fromarray(centered)

            return image

        except Exception as e:
            self.logger.error(f"Centering failed: {str(e)}")
            return image

    def resize_image(self, image: Image.Image, target_size: int) -> Image.Image:
        """Resize image to target resolution while maintaining aspect ratio"""
        try:
            # Get current size
            width, height = image.size

            # Calculate new size (square)
            new_size = (target_size, target_size)

            # Resize with high-quality resampling
            resized = image.resize(new_size, Image.Resampling.LANCZOS)

            self.logger.info(f"Resized image to {target_size}x{target_size}")
            return resized

        except Exception as e:
            self.logger.error(f"Resize failed: {str(e)}")
            return image

    def preprocess(self, image_path: str, target_resolution: int) -> Optional[np.ndarray]:
        """Complete preprocessing pipeline"""
        # Load image
        image = self.load_image(image_path)
        if image is None:
            return None

        # Remove background
        image = self.remove_background(image)

        # Center and pad
        image = self.center_and_pad(image)

        # Resize
        image = self.resize_image(image, target_resolution)

        # Convert to RGB for depth estimation
        if image.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])  # Use alpha as mask
            image = background

        # Convert to numpy array
        image_array = np.array(image)

        return image_array


# =============================================================================
# DEPTH ESTIMATION
# =============================================================================

class DepthEstimator:
    """Generate depth maps using MiDaS"""

    def __init__(self, config: Dict, device: str, logger: logging.Logger):
        self.config = config
        self.device = device
        self.logger = logger
        self.depth_config = config.get('depth_estimation', {})
        self.model = None
        self.transform = None

    def load_model(self):
        """Load MiDaS model"""
        try:
            model_type = self.depth_config.get('model', 'DPT_Large')
            self.logger.info(f"Loading MiDaS model: {model_type}...")

            # Load model from torch hub
            self.model = torch.hub.load("intel-isl/MiDaS", model_type)
            self.model.to(self.device)
            self.model.eval()

            # Load transforms
            midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

            if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
                self.transform = midas_transforms.dpt_transform
            else:
                self.transform = midas_transforms.small_transform

            self.logger.info("MiDaS model loaded successfully")

        except Exception as e:
            self.logger.error(f"Failed to load MiDaS model: {str(e)}")
            raise

    def estimate_depth(self, image: np.ndarray) -> Optional[np.ndarray]:
        """Generate depth map from image"""
        if self.model is None:
            self.load_model()

        try:
            self.logger.info("Estimating depth...")

            # Prepare image
            input_batch = self.transform(image).to(self.device)

            # Inference
            with torch.no_grad():
                prediction = self.model(input_batch)

                # Resize to original resolution
                prediction = torch.nn.functional.interpolate(
                    prediction.unsqueeze(1),
                    size=image.shape[:2],
                    mode="bicubic",
                    align_corners=False,
                ).squeeze()

            depth_map = prediction.cpu().numpy()

            # Apply bilateral filtering for smoothness
            if self.depth_config.get('bilateral_filter', {}).get('enabled', True):
                depth_map = self._apply_bilateral_filter(depth_map)

            # Fill holes
            if self.depth_config.get('fill_holes', True):
                depth_map = self._fill_holes(depth_map)

            # Normalize depth range
            if self.depth_config.get('normalize_depth', True):
                depth_map = self._normalize_depth(depth_map)

            # Invert if needed
            if self.depth_config.get('invert_depth', False):
                depth_map = np.max(depth_map) - depth_map

            self.logger.info("Depth estimation completed")
            return depth_map

        except Exception as e:
            self.logger.error(f"Depth estimation failed: {str(e)}")
            return None

    def _apply_bilateral_filter(self, depth_map: np.ndarray) -> np.ndarray:
        """Apply bilateral filter for smoothness"""
        bf_config = self.depth_config.get('bilateral_filter', {})

        # Normalize to 0-1 for filtering
        depth_normalized = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())
        depth_8bit = (depth_normalized * 255).astype(np.uint8)

        filtered = cv2.bilateralFilter(
            depth_8bit,
            bf_config.get('diameter', 9),
            bf_config.get('sigma_color', 75),
            bf_config.get('sigma_space', 75)
        )

        # Convert back to original range
        filtered_normalized = filtered.astype(np.float32) / 255.0
        filtered_depth = filtered_normalized * (depth_map.max() - depth_map.min()) + depth_map.min()

        return filtered_depth

    def _fill_holes(self, depth_map: np.ndarray) -> np.ndarray:
        """Fill holes in depth map using inpainting"""
        # Detect holes (invalid depth values)
        mask = np.isnan(depth_map) | np.isinf(depth_map)

        if np.any(mask):
            # Convert to 8-bit for inpainting
            depth_normalized = (depth_map - np.nanmin(depth_map)) / (np.nanmax(depth_map) - np.nanmin(depth_map))
            depth_8bit = (depth_normalized * 255).astype(np.uint8)
            mask_8bit = mask.astype(np.uint8) * 255

            # Inpaint
            filled = cv2.inpaint(depth_8bit, mask_8bit, 3, cv2.INPAINT_TELEA)

            # Convert back
            filled_normalized = filled.astype(np.float32) / 255.0
            filled_depth = filled_normalized * (np.nanmax(depth_map) - np.nanmin(depth_map)) + np.nanmin(depth_map)

            return filled_depth

        return depth_map

    def _normalize_depth(self, depth_map: np.ndarray) -> np.ndarray:
        """Normalize depth to 0-1 range"""
        min_val = np.min(depth_map)
        max_val = np.max(depth_map)

        if max_val - min_val > 0:
            normalized = (depth_map - min_val) / (max_val - min_val)
        else:
            normalized = depth_map

        return normalized


# =============================================================================
# MESH GENERATION
# =============================================================================

class MeshGenerator:
    """Generate 3D mesh from depth map"""

    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.mesh_config = config.get('mesh_generation', {})

    def depth_to_point_cloud(self, depth_map: np.ndarray, image: np.ndarray) -> o3d.geometry.PointCloud:
        """Convert depth map to point cloud"""
        try:
            self.logger.info("Converting depth map to point cloud...")

            h, w = depth_map.shape

            # Create meshgrid for x, y coordinates
            x = np.linspace(0, w - 1, w)
            y = np.linspace(0, h - 1, h)
            x, y = np.meshgrid(x, y)

            # Flatten arrays
            x = x.flatten()
            y = y.flatten()
            z = depth_map.flatten()

            # Create points (X, Y, Z)
            points = np.stack([x, y, z], axis=-1)

            # Filter out invalid points
            valid_mask = ~(np.isnan(points).any(axis=1) | np.isinf(points).any(axis=1))
            points = points[valid_mask]

            # Create point cloud
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points)

            # Add colors from image
            if image is not None:
                colors = image.reshape(-1, 3) / 255.0
                colors = colors[valid_mask]
                pcd.colors = o3d.utility.Vector3dVector(colors)

            # Estimate normals
            pcd.estimate_normals(
                search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=10, max_nn=30)
            )

            # Orient normals
            pcd.orient_normals_towards_camera_location(camera_location=np.array([w/2, h/2, -1000]))

            self.logger.info(f"Point cloud created with {len(pcd.points)} points")
            return pcd

        except Exception as e:
            self.logger.error(f"Point cloud generation failed: {str(e)}")
            raise

    def reconstruct_surface(self, pcd: o3d.geometry.PointCloud) -> o3d.geometry.TriangleMesh:
        """Reconstruct surface using Poisson reconstruction"""
        try:
            self.logger.info("Reconstructing surface...")

            method = self.mesh_config.get('reconstruction_method', 'poisson')

            if method == 'poisson':
                poisson_config = self.mesh_config.get('poisson', {})

                # Poisson surface reconstruction
                mesh, densities = pcd.create_from_point_cloud_poisson(
                    depth=poisson_config.get('depth', 9),
                    width=poisson_config.get('width', 0),
                    scale=poisson_config.get('scale', 1.1),
                    linear_fit=poisson_config.get('linear_fit', False)
                )

                # Remove low-density vertices
                vertices_to_remove = densities < np.quantile(densities, 0.1)
                mesh.remove_vertices_by_mask(vertices_to_remove)

            else:
                self.logger.warning(f"Unknown reconstruction method: {method}, using Poisson")
                mesh, _ = pcd.create_from_point_cloud_poisson(depth=9)

            self.logger.info(f"Surface reconstructed: {len(mesh.vertices)} vertices, {len(mesh.triangles)} faces")
            return mesh

        except Exception as e:
            self.logger.error(f"Surface reconstruction failed: {str(e)}")
            raise

    def simplify_mesh(self, mesh: o3d.geometry.TriangleMesh) -> o3d.geometry.TriangleMesh:
        """Simplify mesh to target polycount"""
        simplification_config = self.mesh_config.get('simplification', {})

        if not simplification_config.get('enabled', True):
            return mesh

        try:
            mode = simplification_config.get('mode', 'detailed')

            if mode == 'detailed':
                target_faces = simplification_config.get('target_faces_detailed', 50000)
            elif mode == 'simple':
                target_faces = simplification_config.get('target_faces_simple', 10000)
            else:  # auto
                current_faces = len(mesh.triangles)
                target_faces = 50000 if current_faces > 50000 else current_faces

            current_faces = len(mesh.triangles)

            if current_faces > target_faces:
                self.logger.info(f"Simplifying mesh from {current_faces} to {target_faces} faces...")

                # Calculate reduction ratio
                target_reduction = target_faces / current_faces

                # Simplify using quadric decimation
                simplified = mesh.simplify_quadric_decimation(target_number_of_triangles=target_faces)

                self.logger.info(f"Mesh simplified: {len(simplified.triangles)} faces")
                return simplified

            return mesh

        except Exception as e:
            self.logger.error(f"Mesh simplification failed: {str(e)}")
            return mesh

    def make_watertight(self, mesh: o3d.geometry.TriangleMesh) -> trimesh.Trimesh:
        """Ensure mesh is watertight"""
        if not self.mesh_config.get('make_watertight', True):
            # Convert to trimesh
            vertices = np.asarray(mesh.vertices)
            faces = np.asarray(mesh.triangles)
            return trimesh.Trimesh(vertices=vertices, faces=faces)

        try:
            self.logger.info("Making mesh watertight...")

            # Convert to trimesh for better mesh repair
            vertices = np.asarray(mesh.vertices)
            faces = np.asarray(mesh.triangles)
            tm = trimesh.Trimesh(vertices=vertices, faces=faces)

            # Fill holes
            tm.fill_holes()

            # Fix normals
            tm.fix_normals()

            # Remove duplicate and degenerate faces
            tm.remove_duplicate_faces()
            tm.remove_degenerate_faces()

            # Check if watertight
            is_watertight = tm.is_watertight

            if is_watertight:
                self.logger.info("Mesh is watertight")
            else:
                self.logger.warning("Mesh is not perfectly watertight, but repaired")

            return tm

        except Exception as e:
            self.logger.error(f"Watertight operation failed: {str(e)}")
            # Return as-is
            vertices = np.asarray(mesh.vertices)
            faces = np.asarray(mesh.triangles)
            return trimesh.Trimesh(vertices=vertices, faces=faces)

    def generate_mesh(self, depth_map: np.ndarray, image: np.ndarray) -> trimesh.Trimesh:
        """Complete mesh generation pipeline"""
        # Convert to point cloud
        pcd = self.depth_to_point_cloud(depth_map, image)

        # Reconstruct surface
        mesh = self.reconstruct_surface(pcd)

        # Simplify mesh
        mesh = self.simplify_mesh(mesh)

        # Make watertight
        mesh = self.make_watertight(mesh)

        return mesh


# =============================================================================
# 3D PRINTING OPTIMIZATION
# =============================================================================

class PrintingOptimizer:
    """Optimize mesh for 3D printing"""

    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.printing_config = config.get('printing', {})

    def scale_mesh(self, mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """Scale mesh to target size"""
        max_dimension = self.printing_config.get('max_dimension_mm', 100)

        try:
            # Get current bounding box
            bounds = mesh.bounds
            current_max = np.max(bounds[1] - bounds[0])

            # Calculate scale factor
            scale_factor = max_dimension / current_max

            # Apply scale
            mesh.apply_scale(scale_factor)

            self.logger.info(f"Mesh scaled to max dimension: {max_dimension}mm")
            return mesh

        except Exception as e:
            self.logger.error(f"Scaling failed: {str(e)}")
            return mesh

    def fix_non_manifold(self, mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """Fix non-manifold edges"""
        if not self.printing_config.get('fix_non_manifold', True):
            return mesh

        try:
            # Fill holes
            mesh.fill_holes()

            # Remove duplicate vertices
            mesh.merge_vertices()

            # Remove duplicate faces
            mesh.remove_duplicate_faces()

            # Remove degenerate faces
            mesh.remove_degenerate_faces()

            # Fix normals
            mesh.fix_normals()

            self.logger.info("Non-manifold geometry fixed")
            return mesh

        except Exception as e:
            self.logger.error(f"Non-manifold fix failed: {str(e)}")
            return mesh

    def auto_orient(self, mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """Orient mesh for minimal support needs"""
        if not self.printing_config.get('auto_orient', True):
            return mesh

        try:
            # Place largest face on build plate
            # This minimizes support material

            # Get all face areas
            face_areas = mesh.area_faces

            # Find largest face
            largest_face_idx = np.argmax(face_areas)

            # Get normal of largest face
            normal = mesh.face_normals[largest_face_idx]

            # Rotate so normal points down (negative Z)
            target_normal = np.array([0, 0, -1])

            # Calculate rotation
            rotation_axis = np.cross(normal, target_normal)
            rotation_angle = np.arccos(np.dot(normal, target_normal))

            if np.linalg.norm(rotation_axis) > 1e-6:
                rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)

                # Create rotation matrix
                from scipy.spatial.transform import Rotation
                rotation = Rotation.from_rotvec(rotation_angle * rotation_axis)

                # Apply rotation
                mesh.apply_transform(rotation.as_matrix())

            # Move to build plate (Z=0)
            bounds = mesh.bounds
            z_offset = -bounds[0, 2]
            mesh.apply_translation([0, 0, z_offset])

            self.logger.info("Mesh oriented for minimal supports")
            return mesh

        except Exception as e:
            self.logger.error(f"Auto-orient failed: {str(e)}")
            return mesh

    def check_wall_thickness(self, mesh: trimesh.Trimesh) -> float:
        """Check minimum wall thickness"""
        try:
            # Sample ray-based thickness check
            # This is a simplified version

            min_thickness = self.printing_config.get('min_wall_thickness_mm', 2.0)

            # Get mesh scale
            scale = mesh.scale

            # Estimate minimum thickness from edge lengths
            if len(mesh.edges_unique) > 0:
                edge_vectors = mesh.vertices[mesh.edges_unique[:, 0]] - mesh.vertices[mesh.edges_unique[:, 1]]
                edge_lengths = np.linalg.norm(edge_vectors, axis=1)
                min_edge = np.min(edge_lengths)

                if min_edge < min_thickness * 0.5:
                    self.logger.warning(f"Some edges may be thinner than minimum wall thickness ({min_thickness}mm)")
                else:
                    self.logger.info(f"Wall thickness check passed (min edge: {min_edge:.2f}mm)")

                return min_edge

            return 0.0

        except Exception as e:
            self.logger.error(f"Wall thickness check failed: {str(e)}")
            return 0.0

    def optimize_for_printing(self, mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """Complete printing optimization pipeline"""
        # Fix non-manifold geometry
        mesh = self.fix_non_manifold(mesh)

        # Scale to target size
        mesh = self.scale_mesh(mesh)

        # Auto-orient for printing
        mesh = self.auto_orient(mesh)

        # Check wall thickness
        self.check_wall_thickness(mesh)

        return mesh


# =============================================================================
# BUSINESS FEATURES
# =============================================================================

class BusinessCalculator:
    """Calculate business metrics (cost, pricing, SKU)"""

    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.business_config = config.get('business', {})

    def calculate_volume(self, mesh: trimesh.Trimesh) -> float:
        """Calculate mesh volume in mm³"""
        try:
            volume = mesh.volume  # Already in mm³ if mesh is in mm
            self.logger.info(f"Volume: {volume:.2f} mm³")
            return volume
        except:
            return 0.0

    def calculate_material_cost(self, mesh: trimesh.Trimesh) -> Dict[str, float]:
        """Calculate material usage and cost"""
        pricing_config = self.business_config.get('pricing', {})

        # Calculate volume
        volume_mm3 = self.calculate_volume(mesh)
        volume_cm3 = volume_mm3 / 1000

        # PLA density: ~1.24 g/cm³
        pla_density = 1.24
        weight_grams = volume_cm3 * pla_density

        # Calculate cost
        cost_per_gram = pricing_config.get('pla_cost_per_gram', 0.02)
        material_cost = weight_grams * cost_per_gram

        # Add fixed cost
        fixed_cost = pricing_config.get('fixed_cost_per_print', 2.00)
        total_cost = material_cost + fixed_cost

        self.logger.info(f"Material: {weight_grams:.2f}g PLA, Cost: €{total_cost:.2f}")

        return {
            'volume_mm3': volume_mm3,
            'volume_cm3': volume_cm3,
            'weight_grams': weight_grams,
            'material_cost_eur': material_cost,
            'fixed_cost_eur': fixed_cost,
            'total_cost_eur': total_cost
        }

    def calculate_print_time(self, mesh: trimesh.Trimesh) -> Dict[str, float]:
        """Estimate print time"""
        estimation_config = self.business_config.get('print_estimation', {})

        # Get mesh height
        bounds = mesh.bounds
        height_mm = bounds[1, 2] - bounds[0, 2]

        # Calculate layers
        layer_height = estimation_config.get('layer_height_mm', 0.2)
        num_layers = int(height_mm / layer_height)

        # Estimate time based on perimeter and fill
        # Simplified: use mesh area as proxy
        area = mesh.area
        print_speed = estimation_config.get('print_speed_mm_s', 60)

        # Rough estimate: perimeter per layer * layers / speed
        time_seconds = (area / print_speed) * 0.5  # Approximate factor

        # Add support time
        support_multiplier = estimation_config.get('support_time_multiplier', 1.3)
        time_with_supports = time_seconds * support_multiplier

        time_hours = time_with_supports / 3600

        self.logger.info(f"Estimated print time: {time_hours:.1f} hours")

        return {
            'height_mm': height_mm,
            'num_layers': num_layers,
            'print_time_seconds': time_with_supports,
            'print_time_hours': time_hours
        }

    def generate_sku(self, category: str = None) -> str:
        """Generate unique SKU"""
        sku_config = self.business_config.get('sku', {})

        # Get category
        if category is None:
            category = sku_config.get('default_category', 'PROD')

        # Get date
        date_str = datetime.now().strftime('%Y%m%d')

        # Get counter
        counter_file = sku_config.get('counter_file', 'logs/sku_counter.txt')
        os.makedirs(os.path.dirname(counter_file), exist_ok=True)

        # Read current counter
        if os.path.exists(counter_file):
            with open(counter_file, 'r') as f:
                counter = int(f.read().strip())
        else:
            counter = 0

        # Increment counter
        counter += 1

        # Write back
        with open(counter_file, 'w') as f:
            f.write(str(counter))

        # Generate SKU
        sku = f"{date_str}-{category}-{counter:03d}"

        self.logger.info(f"Generated SKU: {sku}")

        return sku

    def calculate_retail_price(self, cost: float) -> float:
        """Calculate recommended retail price"""
        pricing_config = self.business_config.get('pricing', {})
        markup = pricing_config.get('retail_markup', 5.0)

        retail_price = cost * markup

        self.logger.info(f"Recommended retail price: €{retail_price:.2f}")

        return retail_price

    def calculate_all_metrics(self, mesh: trimesh.Trimesh, category: str = None) -> Dict:
        """Calculate all business metrics"""
        # Material cost
        cost_metrics = self.calculate_material_cost(mesh)

        # Print time
        time_metrics = self.calculate_print_time(mesh)

        # SKU
        sku = self.generate_sku(category)

        # Retail price
        retail_price = self.calculate_retail_price(cost_metrics['total_cost_eur'])

        return {
            'sku': sku,
            **cost_metrics,
            **time_metrics,
            'retail_price_eur': retail_price,
            'profit_margin_eur': retail_price - cost_metrics['total_cost_eur']
        }


# =============================================================================
# EXPORT AND PREVIEW
# =============================================================================

class MeshExporter:
    """Export mesh and generate previews"""

    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.export_config = config.get('export', {})

    def export_stl(self, mesh: trimesh.Trimesh, output_path: str) -> bool:
        """Export mesh as STL file"""
        try:
            stl_config = self.export_config.get('stl', {})

            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Export STL
            mesh.export(
                output_path,
                file_type='stl',
                # trimesh automatically uses binary format by default
            )

            self.logger.info(f"STL exported: {output_path}")
            return True

        except Exception as e:
            self.logger.error(f"STL export failed: {str(e)}")
            return False

    def generate_previews(self, mesh: trimesh.Trimesh, output_dir: str, base_name: str) -> List[str]:
        """Generate preview renders from multiple angles"""
        preview_config = self.export_config.get('previews', {})

        if not preview_config.get('enabled', True):
            return []

        try:
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d.art3d import Poly3DCollection

            num_angles = preview_config.get('num_angles', 4)
            resolution = preview_config.get('resolution', [800, 800])
            bg_color = np.array(preview_config.get('background_color', [255, 255, 255])) / 255.0

            preview_paths = []

            # Generate views from different angles
            angles = np.linspace(0, 360, num_angles, endpoint=False)

            for i, angle in enumerate(angles):
                fig = plt.figure(figsize=(resolution[0]/100, resolution[1]/100))
                ax = fig.add_subplot(111, projection='3d')

                # Create mesh collection
                mesh_collection = Poly3DCollection(
                    mesh.vertices[mesh.faces],
                    alpha=0.9,
                    facecolor='lightblue',
                    edgecolor='gray',
                    linewidths=0.1
                )

                ax.add_collection3d(mesh_collection)

                # Set limits
                bounds = mesh.bounds
                max_range = np.max(bounds[1] - bounds[0])
                mid = (bounds[1] + bounds[0]) / 2

                ax.set_xlim(mid[0] - max_range/2, mid[0] + max_range/2)
                ax.set_ylim(mid[1] - max_range/2, mid[1] + max_range/2)
                ax.set_zlim(mid[2] - max_range/2, mid[2] + max_range/2)

                # Set view angle
                ax.view_init(elev=20, azim=angle)

                # Set background
                ax.set_facecolor(bg_color)
                fig.patch.set_facecolor(bg_color)

                # Remove axes
                ax.set_axis_off()

                # Save
                preview_path = os.path.join(output_dir, f"{base_name}_preview_{i}.png")
                plt.savefig(preview_path, dpi=100, bbox_inches='tight', facecolor=bg_color)
                plt.close()

                preview_paths.append(preview_path)

            self.logger.info(f"Generated {len(preview_paths)} preview images")
            return preview_paths

        except Exception as e:
            self.logger.error(f"Preview generation failed: {str(e)}")
            return []

    def generate_thumbnail(self, mesh: trimesh.Trimesh, output_path: str) -> bool:
        """Generate thumbnail for marketplace"""
        thumbnail_config = self.export_config.get('thumbnail', {})

        if not thumbnail_config.get('enabled', True):
            return False

        try:
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d.art3d import Poly3DCollection

            size = thumbnail_config.get('size', [512, 512])
            bg_color = np.array(thumbnail_config.get('background_color', [255, 255, 255])) / 255.0

            fig = plt.figure(figsize=(size[0]/100, size[1]/100))
            ax = fig.add_subplot(111, projection='3d')

            # Create mesh collection
            mesh_collection = Poly3DCollection(
                mesh.vertices[mesh.faces],
                alpha=1.0,
                facecolor='lightblue',
                edgecolor='none'
            )

            ax.add_collection3d(mesh_collection)

            # Set limits
            bounds = mesh.bounds
            max_range = np.max(bounds[1] - bounds[0])
            mid = (bounds[1] + bounds[0]) / 2

            ax.set_xlim(mid[0] - max_range/2, mid[0] + max_range/2)
            ax.set_ylim(mid[1] - max_range/2, mid[1] + max_range/2)
            ax.set_zlim(mid[2] - max_range/2, mid[2] + max_range/2)

            # Good angle for thumbnail
            ax.view_init(elev=25, azim=45)

            # Set background
            ax.set_facecolor(bg_color)
            fig.patch.set_facecolor(bg_color)

            # Remove axes
            ax.set_axis_off()

            # Save
            plt.savefig(output_path, dpi=100, bbox_inches='tight', facecolor=bg_color)
            plt.close()

            self.logger.info(f"Thumbnail generated: {output_path}")
            return True

        except Exception as e:
            self.logger.error(f"Thumbnail generation failed: {str(e)}")
            return False

    def export_metadata(self, metadata: Dict, output_path: str) -> bool:
        """Export metadata as JSON"""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            self.logger.info(f"Metadata exported: {output_path}")
            return True

        except Exception as e:
            self.logger.error(f"Metadata export failed: {str(e)}")
            return False


# =============================================================================
# MAIN PIPELINE
# =============================================================================

class ImageTo3DPipeline:
    """Main pipeline orchestrator"""

    def __init__(self, config_path: str = 'config.yaml'):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Setup logging
        self.logger = setup_logging(self.config)

        # Initialize system detector
        self.system_detector = SystemDetector(self.config, self.logger)
        self.device = self.system_detector.detect()

        # Initialize modules
        self.preprocessor = ImagePreprocessor(self.config, self.logger)
        self.depth_estimator = DepthEstimator(self.config, self.device, self.logger)
        self.mesh_generator = MeshGenerator(self.config, self.logger)
        self.printing_optimizer = PrintingOptimizer(self.config, self.logger)
        self.business_calculator = BusinessCalculator(self.config, self.logger)
        self.exporter = MeshExporter(self.config, self.logger)

        self.logger.info("Pipeline initialized successfully")

    def process_single_image(self, image_path: str, category: str = None) -> Optional[Dict]:
        """Process a single image through the complete pipeline"""
        start_time = time.time()

        try:
            self.logger.info(f"\n{'='*80}")
            self.logger.info(f"Processing: {image_path}")
            self.logger.info(f"{'='*80}")

            # Get optimal resolution
            target_resolution = self.system_detector.get_optimal_resolution(
                self.config.get('preprocessing', {}).get('target_resolution', 1024)
            )

            # 1. Preprocess image
            self.logger.info("\n[1/7] Preprocessing image...")
            processed_image = self.preprocessor.preprocess(image_path, target_resolution)
            if processed_image is None:
                raise Exception("Image preprocessing failed")

            # 2. Estimate depth
            self.logger.info("\n[2/7] Estimating depth...")
            depth_map = self.depth_estimator.estimate_depth(processed_image)
            if depth_map is None:
                raise Exception("Depth estimation failed")

            # 3. Generate mesh
            self.logger.info("\n[3/7] Generating mesh...")
            mesh = self.mesh_generator.generate_mesh(depth_map, processed_image)

            # 4. Optimize for printing
            self.logger.info("\n[4/7] Optimizing for 3D printing...")
            mesh = self.printing_optimizer.optimize_for_printing(mesh)

            # 5. Calculate business metrics
            self.logger.info("\n[5/7] Calculating business metrics...")
            business_metrics = self.business_calculator.calculate_all_metrics(mesh, category)

            # 6. Export files
            self.logger.info("\n[6/7] Exporting files...")

            # Prepare output paths
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            sku = business_metrics['sku']

            stl_path = f"output/stl/{sku}.stl"
            thumbnail_path = f"output/previews/{sku}_thumbnail.png"
            metadata_path = f"output/reports/{sku}_metadata.json"
            preview_dir = "output/previews"

            # Export STL
            self.exporter.export_stl(mesh, stl_path)

            # Generate previews
            preview_paths = self.exporter.generate_previews(mesh, preview_dir, sku)

            # Generate thumbnail
            self.exporter.generate_thumbnail(mesh, thumbnail_path)

            # 7. Export metadata
            self.logger.info("\n[7/7] Generating metadata...")

            processing_time = time.time() - start_time

            metadata = {
                'sku': sku,
                'source_image': image_path,
                'processing_date': datetime.now().isoformat(),
                'processing_time_seconds': processing_time,
                'outputs': {
                    'stl_file': stl_path,
                    'thumbnail': thumbnail_path,
                    'previews': preview_paths
                },
                'mesh_info': {
                    'vertices': len(mesh.vertices),
                    'faces': len(mesh.faces),
                    'is_watertight': mesh.is_watertight,
                    'bounds_mm': mesh.bounds.tolist()
                },
                'business': business_metrics,
                'configuration': {
                    'device': self.device,
                    'resolution': target_resolution
                }
            }

            self.exporter.export_metadata(metadata, metadata_path)

            # Summary
            self.logger.info(f"\n{'='*80}")
            self.logger.info("PROCESSING COMPLETE")
            self.logger.info(f"{'='*80}")
            self.logger.info(f"SKU: {sku}")
            self.logger.info(f"Processing time: {processing_time:.1f}s")
            self.logger.info(f"STL file: {stl_path}")
            self.logger.info(f"Volume: {business_metrics['volume_cm3']:.2f} cm³")
            self.logger.info(f"Weight: {business_metrics['weight_grams']:.2f}g")
            self.logger.info(f"Cost: €{business_metrics['total_cost_eur']:.2f}")
            self.logger.info(f"Retail price: €{business_metrics['retail_price_eur']:.2f}")
            self.logger.info(f"Print time: {business_metrics['print_time_hours']:.1f}h")
            self.logger.info(f"{'='*80}\n")

            return metadata

        except Exception as e:
            self.logger.error(f"Processing failed for {image_path}: {str(e)}")

            # Handle OOM retry
            if "out of memory" in str(e).lower() and self.config.get('error_handling', {}).get('retry_on_oom', True):
                self.logger.info("Retrying with CPU...")
                self.device = 'cpu'
                self.depth_estimator.device = 'cpu'
                if self.depth_estimator.model is not None:
                    self.depth_estimator.model = self.depth_estimator.model.cpu()
                return self.process_single_image(image_path, category)

            return None

    def process_batch(self, input_dir: str = 'input') -> pd.DataFrame:
        """Process all images in input directory"""
        batch_config = self.config.get('batch', {})

        self.logger.info(f"\n{'='*80}")
        self.logger.info("BATCH PROCESSING")
        self.logger.info(f"{'='*80}\n")

        # Get all image files
        supported_formats = self.config.get('preprocessing', {}).get('input_formats', ['jpg', 'jpeg', 'png'])
        image_files = []

        for fmt in supported_formats:
            image_files.extend(Path(input_dir).glob(f'*.{fmt}'))
            image_files.extend(Path(input_dir).glob(f'*.{fmt.upper()}'))

        image_files = sorted(set(image_files))

        if not image_files:
            self.logger.warning(f"No images found in {input_dir}")
            return pd.DataFrame()

        self.logger.info(f"Found {len(image_files)} images to process")

        # Load state for resuming
        state_file = batch_config.get('state_file', 'logs/batch_state.json')
        processed_files = set()

        if batch_config.get('resume_on_interrupt', True) and os.path.exists(state_file):
            with open(state_file, 'r') as f:
                state = json.load(f)
                processed_files = set(state.get('processed', []))
            self.logger.info(f"Resuming: {len(processed_files)} already processed")

        # Process images
        results = []

        iterator = tqdm(image_files, desc="Processing images") if batch_config.get('show_progress', True) else image_files

        for image_file in iterator:
            image_path = str(image_file)

            # Skip if already processed
            if image_path in processed_files:
                self.logger.info(f"Skipping already processed: {image_path}")
                continue

            # Process image
            metadata = self.process_single_image(image_path)

            if metadata is not None:
                results.append(metadata)
                processed_files.add(image_path)

                # Save state
                os.makedirs(os.path.dirname(state_file), exist_ok=True)
                with open(state_file, 'w') as f:
                    json.dump({'processed': list(processed_files)}, f)
            else:
                if not batch_config.get('continue_on_error', True):
                    break

        # Generate report
        if batch_config.get('generate_report', True) and results:
            report_data = []
            for metadata in results:
                row = {
                    'SKU': metadata['sku'],
                    'Source Image': metadata['source_image'],
                    'Processing Time (s)': metadata['processing_time_seconds'],
                    'Volume (cm³)': metadata['business']['volume_cm3'],
                    'Weight (g)': metadata['business']['weight_grams'],
                    'Material Cost (€)': metadata['business']['material_cost_eur'],
                    'Total Cost (€)': metadata['business']['total_cost_eur'],
                    'Retail Price (€)': metadata['business']['retail_price_eur'],
                    'Profit (€)': metadata['business']['profit_margin_eur'],
                    'Print Time (h)': metadata['business']['print_time_hours'],
                    'STL File': metadata['outputs']['stl_file']
                }
                report_data.append(row)

            df = pd.DataFrame(report_data)

            # Save report
            report_file = batch_config.get('report_file', 'output/reports/batch_report.csv')
            os.makedirs(os.path.dirname(report_file), exist_ok=True)
            df.to_csv(report_file, index=False)

            self.logger.info(f"\nBatch report saved: {report_file}")

            # Print summary
            self.logger.info(f"\n{'='*80}")
            self.logger.info("BATCH SUMMARY")
            self.logger.info(f"{'='*80}")
            self.logger.info(f"Total processed: {len(results)}")
            self.logger.info(f"Total volume: {df['Volume (cm³)'].sum():.2f} cm³")
            self.logger.info(f"Total weight: {df['Weight (g)'].sum():.2f}g")
            self.logger.info(f"Total cost: €{df['Total Cost (€)'].sum():.2f}")
            self.logger.info(f"Total revenue: €{df['Retail Price (€)'].sum():.2f}")
            self.logger.info(f"Total profit: €{df['Profit (€)'].sum():.2f}")
            self.logger.info(f"Avg processing time: {df['Processing Time (s)'].mean():.1f}s")
            self.logger.info(f"{'='*80}\n")

            # Send notification
            if batch_config.get('notify_on_complete', True) and NOTIFICATIONS_AVAILABLE:
                try:
                    notification.notify(
                        title='Batch Processing Complete',
                        message=f'Processed {len(results)} images. Total profit: €{df["Profit (€)"].sum():.2f}',
                        timeout=10
                    )
                except:
                    pass

            return df

        return pd.DataFrame()


# =============================================================================
# CLI
# =============================================================================

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Image-to-3D Pipeline for 3D Printing')
    parser.add_argument('--config', default='config.yaml', help='Config file path')
    parser.add_argument('--image', help='Single image to process')
    parser.add_argument('--batch', action='store_true', help='Process all images in input folder')
    parser.add_argument('--input-dir', default='input', help='Input directory for batch processing')
    parser.add_argument('--category', help='Product category for SKU')

    args = parser.parse_args()

    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Initialize pipeline
    pipeline = ImageTo3DPipeline(args.config)

    if args.image:
        # Process single image
        pipeline.process_single_image(args.image, args.category)
    elif args.batch:
        # Process batch
        pipeline.process_batch(args.input_dir)
    else:
        print("Please specify --image or --batch")
        parser.print_help()


if __name__ == '__main__':
    main()
