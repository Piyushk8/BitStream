from fastapi import APIRouter, UploadFile
from app.core.config import settings
from app.api.controllers.videos import handle_video_upload

videos_router = APIRouter()


@videos_router.post("/upload")
async def upload_video(file: UploadFile):
    return await handle_video_upload(file)
