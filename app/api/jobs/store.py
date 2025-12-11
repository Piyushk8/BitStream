from typing import Dict, Optional
from app.api.jobs.schemas import Job, JobStatus
from app.core.logging import logger
from datetime import datetime

class JobStore:
    def __init__(self):
        self.jobs: Dict[str, Job] = {}

    def create_job(self, job: Job):
        logger.info(f"Creating job {job.job_id}")
        self.jobs[job.job_id] = job
        return job

    def get_job(self, job_id: str) -> Optional[Job]:
        return self.jobs.get(job_id)

    def update_job_status(self, job_id: str, status: JobStatus, progress: float = None, error: str = None):
        job = self.jobs.get(job_id)
        if not job:
            return None

        job.status = status
        if progress is not None:
            job.progress = progress
        if error:
            job.error = error

        job.updated_at = datetime.utcnow()
        self.jobs[job_id] = job
        return job

# Global shared store for now
job_store = JobStore()
