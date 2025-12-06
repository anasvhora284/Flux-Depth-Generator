import os
import sys
import torch
import cv2
import numpy as np
import httpx
from PIL import Image
from typing import Optional, Literal

# Add DepthAnythingV2 to path just in case, though we will try relative import
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEPTH_ANYTHING_PATH = os.path.join(os.path.dirname(CURRENT_DIR), "core", "Depth_Anything_V2")
sys.path.append(DEPTH_ANYTHING_PATH)

try:
    from app.core.Depth_Anything_V2.depth_anything_v2.dpt import DepthAnythingV2
except ImportError:
    # Fallback if the above fails (e.g. if installed via submodule differently)
    try:
        from depth_anything_v2.dpt import DepthAnythingV2
    except ImportError as e:
        print(f"Failed to import DepthAnythingV2: {e}")
        DepthAnythingV2 = None

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# Model Configuration
MODEL_CONFIGS = {
    'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
    'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
    'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
}

# Checkpoint URLs (Example URLs - in a real scenario, these would be robust links)
CHECKPOINT_URLS = {
    'vits': 'https://huggingface.co/depth-anything/Depth-Anything-V2-Small/resolve/main/depth_anything_v2_vits.pth',
    'vitb': 'https://huggingface.co/depth-anything/Depth-Anything-V2-Base/resolve/main/depth_anything_v2_vitb.pth',
    'vitl': 'https://huggingface.co/depth-anything/Depth-Anything-V2-Large/resolve/main/depth_anything_v2_vitl.pth',
}

class DepthService:
    def __init__(self):
        self.models = {}
        self.checkpoints_dir = os.path.join(DEPTH_ANYTHING_PATH, "checkpoints")
        os.makedirs(self.checkpoints_dir, exist_ok=True)

    async def ensure_weights(self, model_type: str):
        """Checks if weights exist, downloads them if not."""
        filename = f"depth_anything_v2_{model_type}.pth"
        path = os.path.join(self.checkpoints_dir, filename)
        
        if not os.path.exists(path):
            print(f"Weights for {model_type} not found at {path}. Downloading...")
            url = CHECKPOINT_URLS.get(model_type)
            if not url:
                raise ValueError(f"No download URL for model type: {model_type}")
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()
                with open(path, "wb") as f:
                    f.write(response.content)
            print(f"Downloaded weights to {path}")
        return path

    async def load_model(self, model_type: str = 'vits'):
        if model_type not in MODEL_CONFIGS:
            raise ValueError(f"Invalid model type: {model_type}")
        
        if model_type in self.models:
            return self.models[model_type]
        
        # Ensure weights are present
        checkpoint_path = await self.ensure_weights(model_type)
        
        # Initialize model
        model = DepthAnythingV2(**MODEL_CONFIGS[model_type])
        model.load_state_dict(torch.load(checkpoint_path, map_location=DEVICE))
        model = model.to(DEVICE).eval()
        
        self.models[model_type] = model
        return model

    async def generate_depth(self, image: Image.Image, model_type: str = 'vits'):
        model = await self.load_model(model_type)
        
        # Prepare image
        image_np = np.array(image) # RGB
        
        # Model expects BGR
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # Inference
        with torch.no_grad():
            depth = model.infer_image(image_bgr)
            
        return depth

depth_service = DepthService()
