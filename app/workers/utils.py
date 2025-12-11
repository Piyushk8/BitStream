# app/workers/utils.py
import time
import logging

logger = logging.getLogger("media-orchestrator.workers")

def exponential_backoff(attempt: int, base: float = 0.5, max_sleep: float = 10.0) -> float:
    """Compute backoff time in seconds."""
    sleep = min(max_sleep, base * (2 ** (attempt - 1)))
    jitter = sleep * 0.1
    return sleep + (jitter * (0.5 - (time.time() % 1)))  # a tiny deterministic jitter
