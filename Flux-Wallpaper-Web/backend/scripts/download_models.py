import sys
import os
import asyncio

# Add backend directory to python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.services.depth import depth_service

async def download_all():
    print("Starting model download...")
    models = ['vits', 'vitb', 'vitl']
    
    for model in models:
        try:
            print(f"Checking/Downloading {model}...")
            path = await depth_service.ensure_weights(model)
            print(f"✅ {model} ready at {path}")
        except Exception as e:
            print(f"❌ Failed to download {model}: {e}")

if __name__ == "__main__":
    asyncio.run(download_all())
