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