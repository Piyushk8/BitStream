import os
import dramatiq
from app.api.jobs.store import job_store
from app.api.jobs.schemas import JobStatus
from app.workers.audio import extract_audio
from app.workers.transcription import transcribe_audio
from app.workers.progress import publish_event
from app.core.logging import logger
# Import ALL actors so Dramatiq registers them

@dramatiq.actor(max_retries=0)
def transcribe_video_job(job_id: str, audio_path: str):
    logger.info(f"Transcription started for job {job_id}")

    if not os.path.exists(audio_path):
        raise RuntimeError(f"Audio file missing: {audio_path}")

    try:
        def update_progress(p):
            publish_event(job_id, "transcription_progress", p)

        transcript = transcribe_audio(audio_path, update_progress)

        job = job_store.get_job(job_id)
        job.transcript = transcript
        job_store.update_job_status(job_id, JobStatus.COMPLETED)

        publish_event(job_id, "transcription_completed", 100)

        os.remove(audio_path)

    except Exception as e:
        publish_event(job_id, "transcription_failed", str(e))
        raise
