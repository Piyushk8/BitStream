from fastapi import UploadFile, HTTPException
from app.api.schemas.schemas import UploadResponse, VideoJobResponse
from app.api.jobs.schemas import JobStatus
from uuid import uuid4
import os


UPLOAD_DIR = "uploads"

from app.queue.task import process_video_job
from app.api.controllers.jobs import create_new_job


async def handle_video_upload(file: UploadFile) -> UploadResponse:
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Invalid file type")

    video_id = str(uuid4())
    ext = os.path.splitext(file.filename)[1]

    save_path = os.path.join(UPLOAD_DIR, f"{video_id}{ext}")
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    with open(save_path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            buffer.write(chunk)

    # ---------- CREATE JOB ----------
    job = create_new_job(video_id=video_id, saved_path=save_path)

    # ---------- ENQUEUE WORK ----------
    process_video_job.send(job.job_id, save_path)

    return UploadResponse(
        video_id=video_id,
        file_name=file.filename,
        path=save_path,
        job_id=job.job_id,
        status=JobStatus.QUEUED,
    )
