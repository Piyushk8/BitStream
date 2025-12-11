from fastapi import UploadFile, HTTPException
from app.api.schemas.schemas import UploadResponse, VideoJobResponse
from uuid import uuid4
import os

UPLOAD_DIR = "uploads"
from app.api.services import generate_processing_job


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

    return UploadResponse(
        video_id=video_id,
        file_name=file.filename,
        path=save_path,
    )

