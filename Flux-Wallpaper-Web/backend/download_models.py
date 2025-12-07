import os
import sys
import httpx
import asyncio

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.depth import CHECKPOINT_URLS, DEPTH_ANYTHING_PATH

async def download_file(url: str, path: str):
    print(f"Downloading {url} to {path}...")
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.get(url, follow_redirects=True)
        response.raise_for_status()
        with open(path, "wb") as f:
            f.write(response.content)
    print(f"Downloaded {path}")

async def main():
    # Ensure checkpoints directory exists
    checkpoints_dir = os.path.join(DEPTH_ANYTHING_PATH, "checkpoints")
    os.makedirs(checkpoints_dir, exist_ok=True)
    
    # Download ViT-S model (Small) - optimal for deployment
    model_type = "vits"
    filename = f"depth_anything_v2_{model_type}.pth"
    path = os.path.join(checkpoints_dir, filename)
    
    if os.path.exists(path):
        print(f"Model {model_type} already exists at {path}")
        return

    url = CHECKPOINT_URLS.get(model_type)
    if not url:
        print(f"URL for {model_type} not found")
        sys.exit(1)
        
    try:
        await download_file(url, path)
        print("Model download completed successfully.")
    except Exception as e:
        print(f"Failed to download model: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
