from fastapi import APIRouter, UploadFile, HTTPException
from app.core.config import settings
from app.api.controllers.jobs import get_job_details, create_new_job
from app.api.jobs.schemas import Job

jobs_router = APIRouter()


@jobs_router.post("/create", response_model=Job)
async def enqueue_job(video_id: str):
    job = create_new_job(video_id)
    return job


@jobs_router.get("/{job_id}", response_model=Job)
async def fetch_job(job_id: str):
    job = get_job_details(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job Not Found")
    return job

