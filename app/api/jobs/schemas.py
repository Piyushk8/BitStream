from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime, timezone
from functools import partial


class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Job(BaseModel):
    job_id: str
    video_id: str
    status: JobStatus = JobStatus.QUEUED
    progress: float = 0.0
    saved_path: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    error: Optional[str] = None
