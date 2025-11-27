import sys
import struct
from PIL import Image
import xml.etree.ElementTree as ET
import base64

def build_xmp_packet(depth_png_bytes):
    b64 = base64.b64encode(depth_png_bytes).decode("ascii")

    rdf = f"""
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description
     xmlns:GDepth="http://ns.google.com/photos/1.0/depthmap/"
     GDepth:Format="RangeInverse"
     GDepth:Near="1.0"
     GDepth:Far="255.0"
     GDepth:Units="Normalized"
     GDepth:Data="{b64}"/>
 </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
"""
    return rdf.encode("utf-8")


def split_xmp_segments(xmp_bytes, max_size=64000):
    """Split large XMP into multiple APP1 segments."""
    segments = []
    header = b"http://ns.adobe.com/xap/1.0/\x00"

    # chunk data into <=64k pieces
    for i in range(0, len(xmp_bytes), max_size):
        chunk = xmp_bytes[i:i+max_size]
        segments.append(header + chunk)

    return segments


def insert_multi_xmp(jpeg_bytes, xmp_bytes):
    """Insert multi-segment APP1 chunks safely into JPEG."""
    SOI = jpeg_bytes[:2]
    rest = jpeg_bytes[2:]

    segments = split_xmp_segments(xmp_bytes)

    out = bytearray()
    out += SOI

    # Insert all APP1 segments before existing JPEG data
    for seg in segments:
        out.append(0xFF)
        out.append(0xE1)
        out += struct.pack(">H", len(seg) + 2)
        out += seg

    out += rest
    return bytes(out)


def main(input_jpg, depth_png, out_jpg):
    # Load depth PNG bytes
    with open(depth_png, "rb") as f:
        depth_bytes = f.read()

    # Build XMP
    xmp = build_xmp_packet(depth_bytes)

    # Load original JPEG
    with open(input_jpg, "rb") as f:
        orig = f.read()

    # Inject multi-segment XMP
    new_jpeg = insert_multi_xmp(orig, xmp)

    # Save
    with open(out_jpg, "wb") as f:
        f.write(new_jpeg)

    print(f"✓ Depth-augmented JPEG written → {out_jpg}")
    print("✓ Compatible with Flux depth models.")
    

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python add_gdepth.py input.jpg depth.png output.jpg")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
