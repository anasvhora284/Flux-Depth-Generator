"""Depth map visualization and processing utilities."""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm


def apply_colormap(depth_map, colormap_name="viridis", invert=False):
    """Apply a colormap to depth data.
    
    Args:
        depth_map: Numpy array of depth values (should be normalized 0-1)
        colormap_name: Name of colormap (grayscale, viridis, plasma, inferno, turbo, jet, ocean, rainbow)
        invert: Whether to invert the colormap
    
    Returns:
        PIL Image with applied colormap
    """
    if depth_map.max() > 1.0:
        depth_normalized = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min() + 1e-6)
    else:
        depth_normalized = depth_map
    
    if invert:
        depth_normalized = 1.0 - depth_normalized
    
    if colormap_name == "grayscale":
        # Simple grayscale
        depth_colored = (depth_normalized * 255).astype(np.uint8)
        return Image.fromarray(depth_colored)
    
    # Use matplotlib colormaps
    cmap_mapping = {
        "viridis": "viridis",
        "plasma": "plasma",
        "inferno": "inferno",
        "turbo": "turbo",
        "jet": "jet",
        "ocean": "ocean",
        "rainbow": "rainbow",
    }
    
    cmap = cm.get_cmap(cmap_mapping.get(colormap_name, "viridis"))
    colored = cmap(depth_normalized)
    
    # Convert to 0-255 range
    rgb = (colored[:, :, :3] * 255).astype(np.uint8)
    return Image.fromarray(rgb)


def adjust_depth_range(depth_map, near_distance=None, far_distance=None):
    """Adjust depth map by clipping to near/far distance range.
    
    Args:
        depth_map: Numpy array of depth values
        near_distance: Near clipping distance (0-100, percentage)
        far_distance: Far clipping distance (0-100, percentage)
    
    Returns:
        Adjusted depth map
    """
    if near_distance is None:
        near_distance = 0
    if far_distance is None:
        far_distance = 100
    
    # Convert percentage to actual values
    min_val = depth_map.min()
    max_val = depth_map.max()
    range_val = max_val - min_val
    
    near_val = min_val + (range_val * near_distance / 100.0)
    far_val = min_val + (range_val * far_distance / 100.0)
    
    # Clip and normalize
    adjusted = np.clip(depth_map, near_val, far_val)
    adjusted = (adjusted - near_val) / (far_val - near_val + 1e-6)
    
    return adjusted


def create_heatmap_visualization(depth_map, invert=False):
    """Create a heat map visualization (red=near, blue=far).
    
    Args:
        depth_map: Numpy array of depth values
        invert: Whether to invert colors
    
    Returns:
        PIL Image with heatmap visualization
    """
    if depth_map.max() > 1.0:
        normalized = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min() + 1e-6)
    else:
        normalized = depth_map
    
    if invert:
        normalized = 1.0 - normalized
    
    # Create heatmap manually (blue -> green -> red)
    h, w = normalized.shape
    heatmap = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Blue (0) -> Cyan -> Green -> Yellow -> Red (1)
    for i in range(h):
        for j in range(w):
            val = normalized[i, j]
            if val < 0.25:
                # Blue to Cyan
                r = 0
                g = int(val * 4 * 255)
                b = 255
            elif val < 0.5:
                # Cyan to Green
                r = 0
                g = 255
                b = int((1 - (val - 0.25) * 4) * 255)
            elif val < 0.75:
                # Green to Yellow
                r = int((val - 0.5) * 4 * 255)
                g = 255
                b = 0
            else:
                # Yellow to Red
                r = 255
                g = int((1 - (val - 0.75) * 4) * 255)
                b = 0
            heatmap[i, j] = [r, g, b]
    
    return Image.fromarray(heatmap)


def create_edge_detection_visualization(depth_map):
    """Create edge detection visualization from depth map.
    
    Args:
        depth_map: Numpy array of depth values
    
    Returns:
        PIL Image with edge detection
    """
    # Simple edge detection using Sobel-like operator
    h, w = depth_map.shape
    edges = np.zeros_like(depth_map)
    
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            gx = (
                depth_map[i - 1, j - 1] + 2 * depth_map[i, j - 1] + depth_map[i + 1, j - 1] -
                depth_map[i - 1, j + 1] - 2 * depth_map[i, j + 1] - depth_map[i + 1, j + 1]
            )
            gy = (
                depth_map[i - 1, j - 1] + 2 * depth_map[i - 1, j] + depth_map[i - 1, j + 1] -
                depth_map[i + 1, j - 1] - 2 * depth_map[i + 1, j] - depth_map[i + 1, j + 1]
            )
            edges[i, j] = np.sqrt(gx ** 2 + gy ** 2)
    
    # Normalize
    if edges.max() > 0:
        edges = (edges / edges.max() * 255).astype(np.uint8)
    else:
        edges = edges.astype(np.uint8)
    
    return Image.fromarray(edges)


def blend_images(depth_image, colormap_image, alpha=0.7):
    """Blend original image with colormap visualization.
    
    Args:
        depth_image: Original depth PIL Image
        colormap_image: Colormap PIL Image
        alpha: Blend factor (0-1, where 0 is colormap only, 1 is depth only)
    
    Returns:
        Blended PIL Image
    """
    img1 = np.array(depth_image).astype(float) / 255.0
    img2 = np.array(colormap_image).astype(float) / 255.0
    
    blended = img1 * alpha + img2 * (1 - alpha)
    blended = (blended * 255).astype(np.uint8)
    
    return Image.fromarray(blended)
