import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.database import engine, Base

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    import asyncio
    asyncio.create_task(cleanup_files_periodically())

async def cleanup_files_periodically():
    import os
    import time
    from app.services.bulk_processor import bulk_processor
    
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    while True:
        try:
            await bulk_processor.cleanup_old_jobs(3600)
        except Exception as e:
            print(f"Cleanup error: {e}")
        
        await asyncio.sleep(3600)

@app.get("/")
def root():
    return {"message": "Welcome to Flux Depth Generator API"}
