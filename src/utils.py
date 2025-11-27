import os
import io
import base64
import psutil
import numpy as np
from PIL import Image

def get_system_metrics():
    """Returns CPU %, RAM %, and current process memory in MB"""
    try:
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        proc = psutil.Process(os.getpid())
        proc_mem_mb = proc.memory_info().rss / (1024 * 1024)
        return cpu, mem.percent, round(proc_mem_mb, 1)
    except Exception:
        return 0, 0, 0

def encode_depth_to_bytes(depth_array):
    """Encodes depth array to PNG bytes for XMP, resizing if necessary."""
    depth_min, depth_max = np.min(depth_array), np.max(depth_array)
    norm = (depth_array - depth_min) / (depth_max - depth_min + 1e-6)
    
    # Use 8-bit for better compression (usually sufficient for web 3D)
    depth_uint8 = (norm * 255).astype(np.uint8)
    img = Image.fromarray(depth_uint8)
    
    # Initial resize if very large
    if img.width > 1024 or img.height > 1024:
        img.thumbnail((1024, 1024))
        
    buffer = io.BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    data = buffer.getvalue()
    
    # Ensure it fits in a single JPEG APP1 segment (~64KB limit)
    # Base64 overhead is ~1.33x, so we need PNG < ~48KB
    # We leave some margin for XMP wrapper
    MAX_SIZE = 45000 
    
    while len(data) > MAX_SIZE:
        w, h = img.size
        if w < 64 or h < 64: # Safety break
            break
        img = img.resize((w // 2, h // 2), Image.Resampling.BILINEAR)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG", optimize=True)
        data = buffer.getvalue()
        
    return data

def create_gdepth_xmp(depth_array, width, height):
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

def embed_xmp_jpeg(image_pil, xmp_bytes, original_bytes=None):
    """Embeds XMP metadata into a JPEG image.
    
    Args:
        image_pil: PIL Image object (used if re-encoding is needed)
        xmp_bytes: The XMP metadata bytes to embed
        original_bytes: Optional bytes of the original file. If provided and valid JPEG,
                       we insert XMP into these bytes to preserve original quality.
    """
    jpeg_bytes = None
    
    # Try to use original bytes if they are a valid JPEG
    if original_bytes and original_bytes.startswith(b"\xff\xd8"):
        jpeg_bytes = original_bytes
    else:
        # Re-encode: Use high quality to preserve detail
        buffer = io.BytesIO()
        image_pil.save(buffer, format="JPEG", quality=100, subsampling=0)
        jpeg_bytes = buffer.getvalue()

    insert_marker = b"http://ns.adobe.com/xap/1.0/\x00"
    if insert_marker not in jpeg_bytes:
        xmp_block = b"\xff\xe1" + (len(xmp_bytes) + 29).to_bytes(2, "big") + insert_marker + xmp_bytes
        # Find the position to insert (after SOI marker)
        return jpeg_bytes[:2] + xmp_block + jpeg_bytes[2:]
    return jpeg_bytes
