import os
import asyncio
import uuid
import shutil
import zipfile
import time
import datetime
import io
import gc
from typing import Dict, Optional
from PIL import Image
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.depth import depth_service
from app.core.config import settings
from app.core.database import async_session_factory
from app.models.job import Job, JobStatus
from app.core.image_processing import apply_colormap, adjust_depth_range

class BulkProcessor:
    def __init__(self):
        # Ensure base upload dir exists
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        self.temp_dir = os.path.join(settings.UPLOAD_DIR, "temp")
        os.makedirs(self.temp_dir, exist_ok=True)

    async def create_job(self, total_files: int, user_id: Optional[uuid.UUID] = None) -> str:
        async with async_session_factory() as session:
            job = Job(
                total_files=total_files,
                user_id=user_id,
                status=JobStatus.PENDING
            )
            session.add(job)
            await session.commit()
            await session.refresh(job)
            
            # Create job directory
            job_dir = os.path.join(self.temp_dir, str(job.id))
            os.makedirs(job_dir, exist_ok=True)
            
            return str(job.id)

    async def _update_job(self, job_id: str, **kwargs):
        async with async_session_factory() as session:
            result = await session.execute(select(Job).where(Job.id == uuid.UUID(job_id)))
            job = result.scalar_one_or_none()
            if job:
                for key, value in kwargs.items():
                    setattr(job, key, value)
                await session.commit()

    async def _process_batch(self, job_id: str, file_paths: list, model_type: str, output_mode: str, colormap: str, invert: bool, near: int, far: int, include_originals: bool):
        try:
            await self._update_job(job_id, status=JobStatus.PROCESSING)
            
            job_dir = os.path.join(self.temp_dir, job_id)
            zip_path = os.path.join(job_dir, "depth_results.zip")
            
            processed_count = 0
            
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for idx, file_path in enumerate(file_paths):
                    try:
                        filename = os.path.basename(file_path)
                        
                        # Read from disk
                        with open(file_path, "rb") as f:
                            content = f.read()
                        
                        image = Image.open(io.BytesIO(content)).convert("RGB")
                        base_filename = os.path.splitext(filename)[0]
                        del content
                        
                        # Generate depth
                        depth = await depth_service.generate_depth(image, model_type)
                        depth_adjusted = adjust_depth_range(depth, near, far)
                        
                        if output_mode == "embedded":
                            from app.core.image_processing import create_gdepth_xmp, embed_xmp_jpeg
                            xmp_bytes = create_gdepth_xmp(depth_adjusted, image.width, image.height)
                            result_bytes = embed_xmp_jpeg(image, xmp_bytes)
                            zip_file.writestr(f"{base_filename}.jpg", result_bytes)
                            del result_bytes
                        else:
                            depth_img = apply_colormap(depth_adjusted, colormap, invert)
                            img_buffer = io.BytesIO()
                            depth_img.save(img_buffer, format="PNG")
                            zip_file.writestr(f"{base_filename}_depth.png", img_buffer.getvalue())
                            
                            if include_originals:
                                from app.core.image_processing import create_gdepth_xmp, embed_xmp_jpeg
                                xmp_bytes = create_gdepth_xmp(depth_adjusted, image.width, image.height)
                                orig_bytes = embed_xmp_jpeg(image, xmp_bytes)
                                zip_file.writestr(f"{base_filename}.jpg", orig_bytes)
                                del orig_bytes
                        
                        del image
                        del depth
                        del depth_adjusted
                        gc.collect()
                        
                        processed_count += 1
                        # Update progress periodically to Db? or just at end? 
                        # Updating DB every file might be heavy. Let's do it every 10% or at least a few times.
                        if idx % 5 == 0 or idx == len(file_paths) - 1:
                             await self._update_job(job_id, processed_files=processed_count)

                    except Exception as e:
                        print(f"Error processing file {filename} in job {job_id}: {e}")
            
            # Clean up upload directory
            upload_dir = os.path.join(job_dir, "uploads")
            if os.path.exists(upload_dir):
                shutil.rmtree(upload_dir)
            
            # Finalize
            await self._update_job(job_id, status=JobStatus.COMPLETED, file_path=zip_path, processed_files=processed_count)
                
        except Exception as e:
            print(f"Fatal error in job {job_id}: {e}")
            await self._update_job(job_id, status=JobStatus.FAILED, error_message=str(e))

    async def start_processing(self, job_id: str, files_data: list, model_type: str, output_mode: str, colormap: str, invert: bool, near: int, far: int, include_originals: bool):
        asyncio.create_task(self._process_batch(job_id, files_data, model_type, output_mode, colormap, invert, near, far, include_originals))

    async def get_job_status(self, job_id: str) -> Optional[Dict]:
        async with async_session_factory() as session:
            try:
                result = await session.execute(select(Job).where(Job.id == uuid.UUID(job_id)))
                job = result.scalar_one_or_none()
                if not job:
                    return None
                
                return {
                    "id": str(job.id),
                    "status": job.status.value,
                    "progress": int((job.processed_files / job.total_files) * 100) if job.total_files > 0 else 0,
                    "total": job.total_files,
                    "completed": job.processed_files,
                    "created_at": job.created_at,
                    "download_url": f"/depth/download/{job.id}" if job.status == JobStatus.COMPLETED else None,
                    "error": job.error_message
                }
            except Exception as e:
                print(f"Error checking job status: {e}")
                return None

    async def get_user_jobs(self, user_id: uuid.UUID) -> list[Dict]:
        async with async_session_factory() as session:
            try:
                # Query jobs for user, newest first
                result = await session.execute(
                    select(Job)
                    .where(Job.user_id == user_id)
                    .order_by(Job.created_at.desc())
                )
                jobs = result.scalars().all()
                
                job_list = []
                for job in jobs:
                    # Calculate progress
                    progress = 0
                    if job.total_files > 0:
                         progress = int((job.processed_files / job.total_files) * 100)
                    
                    job_data = {
                        "id": str(job.id),
                        "status": job.status.value,
                        "progress": progress,
                        "total": job.total_files,
                        "completed": job.processed_files,
                        "created_at": job.created_at.isoformat() if job.created_at else None, # Return ISO string for frontend
                        "download_url": f"/depth/download/{job.id}" if job.status == JobStatus.COMPLETED else None,
                        "error": job.error_message
                    }
                    job_list.append(job_data)
                    
                return job_list
            except Exception as e:
                print(f"Error fetching user jobs: {e}")
                return []

    async def get_download_path(self, job_id: str) -> Optional[str]:
        async with async_session_factory() as session:
             result = await session.execute(select(Job).where(Job.id == uuid.UUID(job_id)))
             job = result.scalar_one_or_none()
             if job and job.status == JobStatus.COMPLETED and job.file_path and os.path.exists(job.file_path):
                 return job.file_path
             return None
        
    async def cleanup_old_jobs(self, max_age_seconds: int = 3600):
        try:
            cutoff_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=max_age_seconds)
            
            async with async_session_factory() as session:
                # Find expired jobs
                result = await session.execute(select(Job).where(Job.created_at < cutoff_time))
                expired_jobs = result.scalars().all()
                
                for job in expired_jobs:
                    job_id = str(job.id)
                    try:
                        # 1. Delete temp directory
                        job_dir = os.path.join(self.temp_dir, job_id)
                        if os.path.exists(job_dir):
                            shutil.rmtree(job_dir)
                            
                        # 2. Delete DB record
                        await session.delete(job)
                        print(f"Cleaned up expired job {job_id}")
                        
                    except Exception as e:
                        print(f"Error cleaning up job {job_id}: {e}")
                
                await session.commit()
                
        except Exception as e:
            print(f"Global cleanup error: {e}")

bulk_processor = BulkProcessor()
