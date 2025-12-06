import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm
import cv2
import io
import base64

def apply_colormap(depth_map: np.ndarray, colormap_name: str = "viridis", invert: bool = False) -> Image.Image:
    """Apply a colormap to depth data."""
    # Normalize
    if depth_map.max() > 1.0:
        depth_normalized = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min() + 1e-6)
    else:
        depth_normalized = depth_map
    
    if invert:
        depth_normalized = 1.0 - depth_normalized
    
    if colormap_name == "grayscale":
        depth_colored = (depth_normalized * 255).astype(np.uint8)
        return Image.fromarray(depth_colored)
    
    if colormap_name == "edges":
        return create_edge_detection(depth_normalized)
        
    if colormap_name == "heatmap":
        cmap = cm.get_cmap("jet")
    else:
        cmap_mapping = {
            "viridis": "viridis",
            "plasma": "plasma",
            "inferno": "inferno",
            "turbo": "turbo",
            "jet": "jet",
            "ocean": "ocean",
            "rainbow": "rainbow",
        }
        cmap_name = cmap_mapping.get(colormap_name, "viridis")
        try:
            cmap = cm.get_cmap(cmap_name)
        except:
            cmap = cm.get_cmap("viridis")

    colored = cmap(depth_normalized)
    rgb = (colored[:, :, :3] * 255).astype(np.uint8)
    return Image.fromarray(rgb)

def create_edge_detection(depth_norm: np.ndarray) -> Image.Image:
    """Simple edge detection."""
    img_u8 = (depth_norm * 255).astype(np.uint8)
    edges = cv2.Canny(img_u8, 50, 150)
    return Image.fromarray(edges)

def adjust_depth_range(depth_map: np.ndarray, near_distance: int = 0, far_distance: int = 100) -> np.ndarray:
    """Adjust depth map by clipping to near/far distance range (percentages)."""
    min_val = depth_map.min()
    max_val = depth_map.max()
    range_val = max_val - min_val
    
    near_val = min_val + (range_val * near_distance / 100.0)
    far_val = min_val + (range_val * far_distance / 100.0)
    
    adjusted = np.clip(depth_map, near_val, far_val)
    adjusted = (adjusted - near_val) / (far_val - near_val + 1e-6)
    
    return adjusted

def create_rgbd_image(original_image: Image.Image, depth_map: np.ndarray) -> Image.Image:
    """
    Create an RGBD image by embedding the depth map into the alpha channel of the original image.
    """
    if depth_map.max() > 1.0:
        depth_normalized = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min() + 1e-6)
    else:
        depth_normalized = depth_map
        
    depth_uint8 = (depth_normalized * 255).astype(np.uint8)
    depth_img = Image.fromarray(depth_uint8, mode='L')
    
    original = original_image.convert("RGB")
    
    if original.size != depth_img.size:
        depth_img = depth_img.resize(original.size, Image.Resampling.LANCZOS)
        
    original.putalpha(depth_img)
    return original


# ============ XMP Depth Embedding Functions ============

def encode_depth_to_bytes(depth_array: np.ndarray) -> bytes:
    """Encodes depth array to PNG bytes for XMP, resizing if necessary."""
    depth_min, depth_max = np.min(depth_array), np.max(depth_array)
    norm = (depth_array - depth_min) / (depth_max - depth_min + 1e-6)
    
    depth_uint8 = (norm * 255).astype(np.uint8)
    img = Image.fromarray(depth_uint8)
    
    if img.width > 1024 or img.height > 1024:
        img.thumbnail((1024, 1024))
        
    buffer = io.BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    data = buffer.getvalue()
    
    MAX_SIZE = 45000  # JPEG APP1 segment limit
    
    while len(data) > MAX_SIZE:
        w, h = img.size
        if w < 64 or h < 64:
            break
        img = img.resize((w // 2, h // 2), Image.Resampling.BILINEAR)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG", optimize=True)
        data = buffer.getvalue()
        
    return data

def create_gdepth_xmp(depth_array: np.ndarray, width: int, height: int) -> bytes:
    """Creates Google Depth XMP metadata."""
    depth_bytes = encode_depth_to_bytes(depth_array)
    depth_base64 = base64.b64encode(depth_bytes).decode("ascii")

    xmp = f"""
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description xmlns:GDepth="http://ns.google.com/photos/1.0/depthmap/"
     GDepth:Format="RangeLinear"
     GDepth:Near="0"
     GDepth:Far="1"
     GDepth:Mime="image/png">
      <GDepth:Data>{depth_base64}</GDepth:Data>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
""".strip()
    return xmp.encode("utf-8")

def embed_xmp_jpeg(image_pil: Image.Image, xmp_bytes: bytes, original_bytes: bytes = None) -> bytes:
    """Embeds XMP metadata into a JPEG image. Image looks identical to original."""
    jpeg_bytes = None
    
    if original_bytes and original_bytes.startswith(b"\xff\xd8"):
        jpeg_bytes = original_bytes
    else:
        buffer = io.BytesIO()
        image_pil.save(buffer, format="JPEG", quality=100, subsampling=0)
        jpeg_bytes = buffer.getvalue()

    insert_marker = b"http://ns.adobe.com/xap/1.0/\x00"
    if insert_marker not in jpeg_bytes:
        xmp_block = b"\xff\xe1" + (len(xmp_bytes) + 29).to_bytes(2, "big") + insert_marker + xmp_bytes
        return jpeg_bytes[:2] + xmp_block + jpeg_bytes[2:]
    return jpeg_bytes

