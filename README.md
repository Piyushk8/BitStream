Phase 0 — Project Roadmap (Python version)

We go in this order:

Core FastAPI skeleton

Async architecture + dependency injection best practices

Local file upload + validation + streaming

Job system (in-memory first → Redis + Dramatiq)

FFmpeg workers (multi-processing vs multi-threading)

Worker orchestration, retries, dead-letter queues

Distributed event updates + dashboard (WebSockets)

Observability

AWS integration (S3, SQS, ECS/EKS, IAM)

Production deployment + CI/CD




FastAPI (API Service)
    |
    | Enqueue Job → Redis (Broker)
    v
Redis Queue
    |
    v
Dramatiq Worker Processes
    |
    | Runs ffmpeg, metadata extraction, chunk processing
    v
JobStore / DB (Progress updates)

Clients → poll API or subscribe via WebSockets for job status



1. User uploads file → FastAPI saves it.

2. FastAPI creates a job entry (job_id, status=queued).

3. FastAPI ENQUEUES the job:
      process_video_job.send(job_id, saved_path)
   This writes a message into Redis.

4. Dramatiq Worker (running in another terminal/machine)
   reads job from Redis automatically.

5. Worker runs `process_video_job()` on that job.

6. Worker updates job status → processing → completed.

7. User checks job status through:
      GET /jobs/<job_id>
