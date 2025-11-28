import sys
import os
import torch
import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Add the submodule to path
# Assumes src/core.py is one level deep from root, and Depth_Anything_V2 is in root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Root directory: {ROOT_DIR}", file=sys.stderr)
DEPTH_ANYTHING_PATH = os.path.join(ROOT_DIR, "Depth_Anything_V2")
print(f"Depth Anything V2 path: {DEPTH_ANYTHING_PATH}", file=sys.stderr)

if DEPTH_ANYTHING_PATH not in sys.path:
    sys.path.append(DEPTH_ANYTHING_PATH)
    print(f"Added {DEPTH_ANYTHING_PATH} to sys.path", file=sys.stderr)

try:
    from depth_anything_v2.dpt import DepthAnythingV2
except ImportError as e:
    print(f"ImportError: {e}", file=sys.stderr)
    try:
        contents = os.listdir(DEPTH_ANYTHING_PATH)
        print(f"Contents of {DEPTH_ANYTHING_PATH}: {contents}", file=sys.stderr)
    except Exception as list_e:
        print(f"Error listing directory: {list_e}", file=sys.stderr)
    DepthAnythingV2 = None

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

@st.cache_resource
def load_model(model_type="vits"):
    """Loads the DepthAnythingV2 model."""
    if DepthAnythingV2 is None:
        st.error("Failed to import DepthAnythingV2. Please check the submodule.")
        return None
    
    try:
        model_configs = {
            'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
            'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
            'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
            'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
        }
        
        if model_type not in model_configs:
            st.error(f"Unknown model type: {model_type}")
            return None

        model = DepthAnythingV2(**model_configs[model_type]).to(DEVICE)
        
        checkpoint_path = os.path.join(DEPTH_ANYTHING_PATH, "checkpoints", f"depth_anything_v2_{model_type}.pth")
        
        if os.path.exists(checkpoint_path):
            model.load_state_dict(torch.load(checkpoint_path, map_location=DEVICE))
        else:
            st.warning(f"Checkpoint not found at {checkpoint_path}. Using random weights (not recommended).")
            
        model.eval()
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def infer_depth(model, image):
    """Runs inference on a single image.
    
    Args:
        model: DepthAnythingV2 model
        image: PIL Image or numpy array (RGB)
        
    Returns:
        depth: numpy array of depth map
    """
    # Convert PIL to numpy (RGB)
    if isinstance(image, Image.Image):
        image = np.array(image)
    
    # infer_image expects BGR because it does cv2.cvtColor(..., cv2.COLOR_BGR2RGB)
    # So we need to convert RGB -> BGR
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    depth = model.infer_image(image_bgr)
    return depth
