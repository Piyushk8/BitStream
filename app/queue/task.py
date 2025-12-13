import dramatiq
import os
from app.api.jobs.store import job_store
from app.api.jobs.schemas import JobStatus
# from app.workers.tasks import run_ffmpeg_with_progress
from app.core.logging import logger
from app.workers.progress import publish_event
from app.workers.hls.hls import generate_hls_from_source
import subprocess

def get_video_duration(input_path: str) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            input_path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


@dramatiq.actor(max_retries=3, min_backoff=2000)
def process_video_job(job_id: str, saved_path: str):

    logger.info(f"worker picked the job {job_id}")
    job_store.update_job_status(job_id, JobStatus.PROCESSING, progress=0.0)

    output_dir = f"outputs/{job_id}"
    hls_dir = f"{output_dir}/hls"
    os.makedirs(hls_dir, exist_ok=True)
    
    duration = get_video_duration(saved_path)
    job_store.set_duration(job_id, duration)

    def update_progress(ms):
        progress = min(99.0, (ms / (duration * 1_000_000)) * 100)
        job_store.update_job_status(job_id, JobStatus.PROCESSING, progress=progress)
        publish_event(job_id, "progress", progress)

    try:
        # run_ffmpeg_with_progress(saved_path, output_file, "720p", update_progress)
        generate_hls_from_source(
            input_path=saved_path,
            hls_dir=hls_dir,
            progress_callback=update_progress,
        )
        os.remove(saved_path)

        job_store.update_job_status(job_id, JobStatus.COMPLETED, progress=100.0)
        publish_event(job_id, "completed", 100)
        logger.info(f"Job {job_id} COMPLETED")

    except Exception as e:
        logger.error(f"Job {job_id} FAILED: {e}")
        job_store.update_job_status(job_id, JobStatus.FAILED, error=str(e))
        publish_event(job_id, "failed", str(e))
        raise
