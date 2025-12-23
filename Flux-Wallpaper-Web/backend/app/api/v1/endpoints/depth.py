from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import StreamingResponse, Response, FileResponse
from typing import Literal
from PIL import Image
import io
import os
import numpy as np
import cv2
import base64
import zipfile
from datetime import datetime
from app.services.depth import depth_service
from app.services.bulk_processor import bulk_processor
from app.api import deps
from app.models.user import User
from app.core.image_processing import apply_colormap, adjust_depth_range, create_gdepth_xmp, embed_xmp_jpeg

router = APIRouter()

@router.post("/generate")
async def generate_depth(
    files: list[UploadFile] = File(...),
    model_type: str = Form("vits"),
    output_mode: str = Form("embedded"),
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

    job_id = await bulk_processor.create_job(len(files), user_id=current_user.id)

    if len(files) > 4:
        upload_dir = os.path.join(bulk_processor.temp_dir, job_id, "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        
        file_paths = []
        for file in files:
            file_path = os.path.join(upload_dir, file.filename)
            with open(file_path, "wb") as f:
                while content := await file.read(1024 * 1024): 
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
    
    try:
        await bulk_processor._update_job(job_id, status="processing")

        processed_files = []
        
        for file in files:
            if not file.content_type or not file.content_type.startswith("image/"):
                continue
            
            contents = await file.read()
            image = Image.open(io.BytesIO(contents)).convert("RGB")
            base_filename = os.path.splitext(file.filename)[0]
            
            depth = await depth_service.generate_depth(image, model_type)
            depth_adjusted = adjust_depth_range(depth, near, far)
            
            if output_mode == "embedded":
                xmp_bytes = create_gdepth_xmp(depth_adjusted, image.width, image.height)
                result_bytes = embed_xmp_jpeg(image, xmp_bytes)
                processed_files.append((f"{base_filename}.jpg", result_bytes, "image/jpeg"))
            else:
                depth_img = apply_colormap(depth_adjusted, colormap, invert)
                img_buffer = io.BytesIO()
                depth_img.save(img_buffer, format="PNG")
                processed_files.append((f"{base_filename}_depth.png", img_buffer.getvalue(), "image/png"))
                
                if include_originals:
                    xmp_bytes = create_gdepth_xmp(depth_adjusted, image.width, image.height)
                    orig_bytes = embed_xmp_jpeg(image, xmp_bytes)
                    processed_files.append((f"{base_filename}.jpg", orig_bytes, "image/jpeg"))
        
        job_dir = os.path.join(bulk_processor.temp_dir, job_id)
        os.makedirs(job_dir, exist_ok=True)
        zip_path = os.path.join(job_dir, "depth_results.zip")
        
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for filename, data, content_type in processed_files:
                zip_file.writestr(filename, data)

        if processed_files:
            try:
                t_filename, t_data, t_type = processed_files[0]
                t_img = Image.open(io.BytesIO(t_data))
                t_img.thumbnail((300, 300))
                t_img = t_img.convert("RGB")
                t_img.save(os.path.join(job_dir, "thumbnail.jpg"), quality=70)
            except Exception as e:
                print(f"Failed to generate thumbnail for {job_id}: {e}")
        
        await bulk_processor._update_job(job_id, status="completed", file_path=zip_path, processed_files=len(processed_files))

        files_data = []
        for filename, data, content_type in processed_files:
            files_data.append({
                "filename": filename,
                "data": base64.b64encode(data).decode("ascii"),
                "content_type": content_type
            })
        
        return {
            "job_id": job_id,
            "files": files_data, 
            "download_type": "multiple" if len(processed_files) > 1 else "single"
        }
        
    except Exception as e:
        print(f"Error generating depth batch: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs")
async def get_user_jobs(current_user: User = Depends(deps.get_current_active_user)):
    return await bulk_processor.get_user_jobs(current_user.id)

@router.get("/status/{job_id}")
async def get_status(job_id: str, current_user: User = Depends(deps.get_current_active_user)):
    status = await bulk_processor.get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return status

@router.get("/download/{job_id}")
async def download_result(job_id: str, current_user: User = Depends(deps.get_current_active_user)):
    path = await bulk_processor.get_download_path(job_id)
    if not path:
        job = await bulk_processor.get_job_status(job_id)
        if job and job['status'] == 'processing':
             raise HTTPException(status_code=400, detail="Job is still processing")
        raise HTTPException(status_code=404, detail="File not found or expired")
        
    filename = os.path.basename(path)
    return FileResponse(path, filename=filename)

@router.get("/thumbnail/{job_id}")
async def get_thumbnail(job_id: str, current_user: User = Depends(deps.get_current_active_user)):
    job_dir = os.path.join(bulk_processor.temp_dir, job_id)
    thumb_path = os.path.join(job_dir, "thumbnail.jpg")
    
    if os.path.exists(thumb_path):
        return FileResponse(thumb_path, media_type="image/jpeg")
    
    raise HTTPException(status_code=404, detail="Thumbnail not found")

@router.get("/models")
async def list_models(current_user: User = Depends(deps.get_current_active_user)):
    return {
        "models": [
            {"id": "vits", "name": "ViT-S (Small)", "description": "Fastest, lower detail"},
            {"id": "vitb", "name": "ViT-B (Base)", "description": "Balanced speed and detail"},
            {"id": "vitl", "name": "ViT-L (Large)", "description": "High detail, slower"},
        ]
    }
