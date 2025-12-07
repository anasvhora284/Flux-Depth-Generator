from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import StreamingResponse, Response, FileResponse
from typing import Literal
from PIL import Image
import io
import os
import numpy as np
import cv2
from app.services.depth import depth_service
from app.services.bulk_processor import bulk_processor
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.post("/generate")
async def generate_depth(
    files: list[UploadFile] = File(...),
    model_type: str = Form("vits"),
    output_mode: str = Form("embedded"),  # 'embedded' or 'depth'
    colormap: str = Form("grayscale"),
    invert: bool = Form(False),
    near: int = Form(0),
    far: int = Form(100),
    include_originals: bool = Form(False),
    current_user: User = Depends(deps.get_current_active_user)
):
    if model_type not in ["vits", "vitb", "vitl"]:
        raise HTTPException(status_code=400, detail="Invalid model type")
    if output_mode not in ["embedded", "depth"]:
        raise HTTPException(status_code=400, detail="Invalid output mode")

    # Use Bulk Processing for ALL requests to prevent timeouts on CPU instances
    # Use Bulk Processing for ALL requests to prevent timeouts on CPU instances
    if len(files) > 0:
        job_id = await bulk_processor.create_job(len(files), user_id=current_user.id)
        
        # Save files to temp disk to avoid OOM
        upload_dir = os.path.join(bulk_processor.temp_dir, job_id, "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        
        file_paths = []
        for file in files:
            file_path = os.path.join(upload_dir, file.filename)
            with open(file_path, "wb") as f:
                # Use shutil to copy spooled file to disk efficiently
                # or read in chunks
                while content := await file.read(1024 * 1024): # 1MB chunks
                    f.write(content)
            file_paths.append(file_path)
            
        await bulk_processor.start_processing(
            job_id, file_paths, model_type, output_mode, colormap, invert, near, far, include_originals
        )
        
        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Bulk processing started",
            "total_files": len(files)
        }
    
    # Sync Logic for small batches
    try:
        import zipfile
        from datetime import datetime
        from app.core.image_processing import apply_colormap, adjust_depth_range, create_gdepth_xmp, embed_xmp_jpeg
        
        # Process all files
        processed_files = []  # List of (filename, bytes, content_type)
        
        for file in files:
            if not file.content_type or not file.content_type.startswith("image/"):
                continue
            
            contents = await file.read()
            image = Image.open(io.BytesIO(contents)).convert("RGB")
            base_filename = os.path.splitext(file.filename)[0]
            
            # Generate depth
            depth = await depth_service.generate_depth(image, model_type)
            depth_adjusted = adjust_depth_range(depth, near, far)
            
            if output_mode == "embedded":
                # Embedded: Store depth as XMP metadata in JPEG (visually identical to original)
                xmp_bytes = create_gdepth_xmp(depth_adjusted, image.width, image.height)
                result_bytes = embed_xmp_jpeg(image, xmp_bytes)
                processed_files.append((f"{base_filename}.jpg", result_bytes, "image/jpeg"))
            else:
                # Depth Map Mode
                depth_img = apply_colormap(depth_adjusted, colormap, invert)
                img_buffer = io.BytesIO()
                depth_img.save(img_buffer, format="PNG")
                processed_files.append((f"{base_filename}_depth.png", img_buffer.getvalue(), "image/png"))
                
                if include_originals:
                    # Save original with embedded depth (XMP)
                    xmp_bytes = create_gdepth_xmp(depth_adjusted, image.width, image.height)
                    orig_bytes = embed_xmp_jpeg(image, xmp_bytes)
                    processed_files.append((f"{base_filename}.jpg", orig_bytes, "image/jpeg"))
        
        # Generate dynamic filename prefix
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        username = current_user.email.split("@")[0] if current_user.email else "user"
        
        # If only 1 file processed, return it directly (no zip)
        if len(processed_files) == 1:
            filename, data, content_type = processed_files[0]
            return Response(
                content=data, 
                media_type=content_type, 
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
        
        # For 2-4 files (small batch in sync mode), return JSON with base64 for individual downloads
        import base64
        files_data = []
        for filename, data, content_type in processed_files:
            files_data.append({
                "filename": filename,
                "data": base64.b64encode(data).decode("ascii"),
                "content_type": content_type
            })
        
        return {"files": files_data, "download_type": "multiple"}
        
        
    except Exception as e:
        print(f"Error generating depth batch: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs")
async def get_user_jobs(current_user: User = Depends(deps.get_current_active_user)):
    """Get all jobs for the current user."""
    return await bulk_processor.get_user_jobs(current_user.id)

@router.get("/status/{job_id}")
async def get_status(job_id: str, current_user: User = Depends(deps.get_current_active_user)):
    status = await bulk_processor.get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return status

@router.get("/download/{job_id}")
async def download_result(job_id: str, current_user: User = Depends(deps.get_current_active_user)):
    from datetime import datetime
    
    path = await bulk_processor.get_download_path(job_id)
    if not path:
        job = await bulk_processor.get_job_status(job_id)
        if job and job["status"] == "processing":
             raise HTTPException(status_code=400, detail="Job still processing")
        raise HTTPException(status_code=404, detail="File not found or expired")
    
    # Generate dynamic filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    username = current_user.email.split("@")[0] if current_user.email else "user"
    
    # Check if original request was single file to name correctly? 
    # For now, zip is fine, or we can inspect content.
    # But simplifying: always return zip for reliability.
    zip_filename = f"flux-depth-{username}_processed_{timestamp}.zip"
    
    return FileResponse(path, media_type="application/zip", filename=zip_filename)

@router.get("/models")
async def list_models(current_user: User = Depends(deps.get_current_active_user)):
    """List available model types."""
    return {
        "models": [
            {"id": "vits", "name": "ViT-S (Small)", "description": "Fastest, lower detail"},
            {"id": "vitb", "name": "ViT-B (Base)", "description": "Balanced speed and detail"},
            {"id": "vitl", "name": "ViT-L (Large)", "description": "High detail, slower"},
        ]
    }
