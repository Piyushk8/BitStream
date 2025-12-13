import dramatiq
import os
from app.api.jobs.store import job_store
from app.api.jobs.schemas import JobStatus
from app.workers.tasks import run_ffmpeg_with_progress
from app.core.logging import logger
from app.workers.progress import publish_event


@dramatiq.actor(max_retries=3, min_backoff=2000)
def process_video_job(job_id: str, saved_path: str):

    logger.info(f"worker picked the job {job_id}")
    job_store.update_job_status(job_id, JobStatus.PROCESSING, progress=0.0)

    output_dir = f"outputs/{job_id}"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/720p.mp4"

    def update_progress(p):
        job_store.update_job_status(job_id, JobStatus.PROCESSING, progress=p)
        publish_event(job_id, "progress", p)

    try:
        run_ffmpeg_with_progress(saved_path, output_file, "720p", update_progress)

        job_store.update_job_status(job_id, JobStatus.COMPLETED, progress=100.0)
        publish_event(job_id, "completed", 100)
        logger.info(f"Job {job_id} COMPLETED")

    except Exception as e:
        logger.error(f"Job {job_id} FAILED: {e}")
        job_store.update_job_status(job_id, JobStatus.FAILED, error=str(e))
        publish_event(job_id, "failed", str(e))
        raise
