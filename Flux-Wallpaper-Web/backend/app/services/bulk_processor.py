import os
import asyncio
import uuid
import shutil
import zipfile
import time
import io
from typing import Dict, Optional
from PIL import Image
from app.services.depth import depth_service
from app.core.config import settings
from app.core.image_processing import apply_colormap, adjust_depth_range, create_rgbd_image

class BulkProcessor:
    def __init__(self):
        self.jobs: Dict[str, Dict] = {}
        # Ensure base upload dir exists
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        self.temp_dir = os.path.join(settings.UPLOAD_DIR, "temp")
        os.makedirs(self.temp_dir, exist_ok=True)

    def create_job(self, total_files: int) -> str:
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {
            "id": job_id,
            "status": "processing",
            "progress": 0,
            "total": total_files,
            "completed": 0,
            "created_at": time.time(),
            "download_url": None,
            "error": None
        }
        # Create job directory
        job_dir = os.path.join(self.temp_dir, job_id)
        os.makedirs(job_dir, exist_ok=True)
        return job_id

    async def _process_batch(self, job_id: str, files_data: list, model_type: str, output_mode: str, colormap: str, invert: bool, near: int, far: int, include_originals: bool):
        try:
            job_dir = os.path.join(self.temp_dir, job_id)
            zip_path = os.path.join(job_dir, "depth_results.zip")
            
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for idx, (filename, content) in enumerate(files_data):
                    try:
                        image = Image.open(io.BytesIO(content)).convert("RGB")
                        base_filename = os.path.splitext(filename)[0]
                        
                        # Generate depth
                        depth = await depth_service.generate_depth(image, model_type)
                        depth_adjusted = adjust_depth_range(depth, near, far)
                        
                        if output_mode == "embedded":
                            from app.core.image_processing import create_gdepth_xmp, embed_xmp_jpeg
                            xmp_bytes = create_gdepth_xmp(depth_adjusted, image.width, image.height)
                            result_bytes = embed_xmp_jpeg(image, xmp_bytes)
                            zip_file.writestr(f"{base_filename}.jpg", result_bytes)
                        else:
                            depth_img = apply_colormap(depth_adjusted, colormap, invert)
                            img_buffer = io.BytesIO()
                            depth_img.save(img_buffer, format="PNG")
                            zip_file.writestr(f"{base_filename}_depth.png", img_buffer.getvalue())
                            
                            if include_originals:
                                # Save original with embedded depth (XMP)
                                from app.core.image_processing import create_gdepth_xmp, embed_xmp_jpeg
                                xmp_bytes = create_gdepth_xmp(depth_adjusted, image.width, image.height)
                                orig_bytes = embed_xmp_jpeg(image, xmp_bytes)
                                zip_file.writestr(f"{base_filename}.jpg", orig_bytes)
                        
                        # Update progress
                        if job_id in self.jobs:
                            self.jobs[job_id]["completed"] += 1
                            self.jobs[job_id]["progress"] = int((self.jobs[job_id]["completed"] / self.jobs[job_id]["total"]) * 100)
                            
                    except Exception as e:
                        print(f"Error processing file {filename} in job {job_id}: {e}")
            
            # Finalize
            if job_id in self.jobs:
                self.jobs[job_id]["status"] = "completed"
                self.jobs[job_id]["download_url"] = f"/depth/download/{job_id}"
                
        except Exception as e:
            print(f"Fatal error in job {job_id}: {e}")
            if job_id in self.jobs:
                self.jobs[job_id]["status"] = "failed"
                self.jobs[job_id]["error"] = str(e)

    async def start_processing(self, job_id: str, files_data: list, model_type: str, output_mode: str, colormap: str, invert: bool, near: int, far: int, include_originals: bool):
        asyncio.create_task(self._process_batch(job_id, files_data, model_type, output_mode, colormap, invert, near, far, include_originals))

    def get_job_status(self, job_id: str) -> Optional[Dict]:
        return self.jobs.get(job_id)

    def get_download_path(self, job_id: str) -> Optional[str]:
        path = os.path.join(self.temp_dir, job_id, "depth_results.zip")
        if os.path.exists(path):
            return path
        return None
        
    def cleanup_old_jobs(self, max_age_seconds: int = 3600):
        current_time = time.time()
        to_delete = []
        
        for job_id, job in self.jobs.items():
            if current_time - job["created_at"] > max_age_seconds:
                to_delete.append(job_id)
                
        for job_id in to_delete:
            try:
                # Remove from dict
                del self.jobs[job_id]
                # Remove files
                job_dir = os.path.join(self.temp_dir, job_id)
                if os.path.exists(job_dir):
                    shutil.rmtree(job_dir)
                print(f"Cleaned up job {job_id}")
            except Exception as e:
                print(f"Error cleaning up job {job_id}: {e}")

bulk_processor = BulkProcessor()
