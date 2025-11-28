"""Export format handlers for different depth map formats."""

import numpy as np
import io
from PIL import Image


def save_depth_as_png(depth_map, colormap_image=None):
    """Save depth map as PNG.
    
    Args:
        depth_map: Raw depth numpy array or PIL Image
        colormap_image: Optional colormap PIL Image (used if provided)
    
    Returns:
        BytesIO object with PNG data
    """
    if colormap_image:
        output_image = colormap_image
    elif isinstance(depth_map, np.ndarray):
        # Normalize and convert to 8-bit
        normalized = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min() + 1e-6)
        output_image = Image.fromarray((normalized * 255).astype(np.uint8))
    else:
        output_image = depth_map
    
    buffer = io.BytesIO()
    output_image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def save_depth_as_tiff(depth_map):
    """Save depth map as 16-bit TIFF (professional format).
    
    Args:
        depth_map: Raw depth numpy array (float32)
    
    Returns:
        BytesIO object with TIFF data
    """
    try:
        # Normalize to 16-bit range
        if depth_map.dtype == np.float32 or depth_map.dtype == np.float64:
            # Normalize float to 0-65535 range
            normalized = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min() + 1e-6)
            depth_16bit = (normalized * 65535).astype(np.uint16)
        else:
            depth_16bit = depth_map.astype(np.uint16)
        
        # Create PIL Image
        image = Image.fromarray(depth_16bit)
        
        buffer = io.BytesIO()
        image.save(buffer, format="TIFF", compression="tiff_deflate")
        buffer.seek(0)
        return buffer
    except Exception as e:
        raise ValueError(f"Failed to save as TIFF: {e}")


def save_depth_as_exr(depth_map):
    """Save depth map as OpenEXR (professional VFX format).
    
    Args:
        depth_map: Raw depth numpy array (float32)
    
    Returns:
        BytesIO object with EXR data
    """
    try:
        import OpenEXR
        import Imath
        
        # Prepare depth map
        if depth_map.dtype != np.float32:
            depth_float = depth_map.astype(np.float32)
        else:
            depth_float = depth_map
        
        # Normalize to 0-1 range
        normalized = (depth_float - depth_float.min()) / (depth_float.max() - depth_float.min() + 1e-6)
        
        # Create EXR file
        h, w = normalized.shape
        pixels_str = normalized.astype(np.float32).tobytes()
        
        exr = OpenEXR.OutputFile(io.BytesIO())
        pixel_type = Imath.PixelType.FLOAT
        
        exr.setFrameBuffer({
            "R": OpenEXR.Channel(pixel_type, pixels_str, w),
            "G": OpenEXR.Channel(pixel_type, pixels_str, w),
            "B": OpenEXR.Channel(pixel_type, pixels_str, w),
        })
        exr.writePixels({"R": pixels_str, "G": pixels_str, "B": pixels_str})
        
        buffer = io.BytesIO()
        exr.close()
        
        return buffer
    except ImportError:
        raise ImportError("OpenEXR module not installed. Install with: pip install openexr")
    except Exception as e:
        raise ValueError(f"Failed to save as EXR: {e}")


def save_depth_as_npy(depth_map):
    """Save depth map as numpy binary format (for data analysis).
    
    Args:
        depth_map: Raw depth numpy array
    
    Returns:
        BytesIO object with NPY data
    """
    buffer = io.BytesIO()
    np.save(buffer, depth_map)
    buffer.seek(0)
    return buffer


def save_depth_as_raw(depth_map):
    """Save depth map as raw binary float32.
    
    Args:
        depth_map: Raw depth numpy array
    
    Returns:
        BytesIO object with raw float32 data
    """
    buffer = io.BytesIO()
    buffer.write(depth_map.astype(np.float32).tobytes())
    buffer.seek(0)
    return buffer


def get_export_handlers():
    """Return dictionary of available export format handlers."""
    return {
        "PNG": {
            "name": "PNG (8-bit, compressed)",
            "handler": save_depth_as_png,
            "extension": ".png",
            "description": "Standard PNG format for depth visualization"
        },
        "TIFF": {
            "name": "TIFF (16-bit, lossless)",
            "handler": save_depth_as_tiff,
            "extension": ".tiff",
            "description": "Professional 16-bit depth map for image processing"
        },
        "EXR": {
            "name": "EXR (32-bit float, professional)",
            "handler": save_depth_as_exr,
            "extension": ".exr",
            "description": "Industry standard for VFX and professional 3D pipelines"
        },
        "NPY": {
            "name": "NPY (NumPy binary)",
            "handler": save_depth_as_npy,
            "extension": ".npy",
            "description": "NumPy format for machine learning and data analysis"
        },
        "RAW": {
            "name": "RAW (Float32 binary)",
            "handler": save_depth_as_raw,
            "extension": ".raw",
            "description": "Raw binary float32 data for custom processing"
        }
    }


class DepthExporter:
    """Helper class for exporting depth maps in multiple formats."""
    
    def __init__(self, depth_map, width, height):
        """Initialize exporter.
        
        Args:
            depth_map: Raw depth numpy array
            width: Image width
            height: Image height
        """
        self.depth_map = depth_map
        self.width = width
        self.height = height
        self.handlers = get_export_handlers()
    
    def export(self, format_name, **kwargs):
        """Export to specified format.
        
        Args:
            format_name: Name of export format (PNG, TIFF, EXR, NPY, RAW)
            **kwargs: Additional arguments for handler
        
        Returns:
            BytesIO object with exported data
        """
        if format_name not in self.handlers:
            raise ValueError(f"Unknown format: {format_name}")
        
        handler = self.handlers[format_name]["handler"]
        
        try:
            if format_name == "PNG":
                # Handle colormap if provided
                colormap_image = kwargs.get("colormap_image", None)
                return handler(self.depth_map, colormap_image)
            else:
                return handler(self.depth_map)
        except Exception as e:
            raise RuntimeError(f"Export to {format_name} failed: {e}")
