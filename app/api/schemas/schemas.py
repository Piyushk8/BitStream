from pydantic import BaseModel

class UploadResponse(BaseModel):
    video_id:str
    file_name:str
    path:str

class VideoJobResponse(BaseModel):
    job_id:str
    status:str
    progress: float

