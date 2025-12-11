

from pydantic import BaseModel,Field
from enum import Enum
from typing import Optional
from datetime import datetime
from functools import partial
class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    Failed = "failed"

class Job(BaseModel):
    job_id:str
    video_id: str
    status: JobStatus = JobStatus.QUEUED
    progress : float = 0.0
    created_at: datetime = Field(default_factory=partial(datetime,tz="utc"))
    updated_at: datetime = Field(default_factory=partial(datetime,tz="utc"))
    error: Optional[str] = None

    