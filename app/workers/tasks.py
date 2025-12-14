# Import ALL actors so Dramatiq registers them
from app.queue.task import process_video_job
from app.queue.transcription_task import transcribe_video_job

