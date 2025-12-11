import dramatiq
from app.api.jobs.store import job_store
from app.api.jobs.schemas import JobStatus, Job

from app.workers.tasks import extract_metadata_and_thumbnail
from app.core.logging import logger


@dramatiq.actor(max_retries=3, min_backoff=2000)
def process_video_job(job_id: str, saved_path: str):

    logger.info(f"worker picked the job {job_id}")

    job_store.update_job_status(job_id, JobStatus.PROCESSING, progress=0.0)

    try:
        output_dir = f"outputs/{job_id}"

        result = extract_metadata_and_thumbnail(saved_path, output_dir)
        job_store.update_job_status(job_id, JobStatus.COMPLETED, progress=100.0)
        logger.info(f"Job {job_id} COMPLETED")

    except Exception as e:
        logger.error(f"Job {job_id} FAILED: {e}")
        job_store.update_job_status(job_id, JobStatus.FAILED, error=str(e))
        raise e  
