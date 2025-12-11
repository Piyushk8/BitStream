from uuid import uuid4

from app.api.jobs.schemas import JobStatus, Job
from app.api.jobs.store import job_store


def create_new_job(video_id: str) -> Job:
    job_id = str(uuid4())

    job = Job(job_id=job_id, video_id=video_id, status=JobStatus.QUEUED)

    job_store.create_job(job)
    return job


def get_job_details(job_id: str) -> Job | None:
    return job_store.get_job(job_id)
