import redis
import json

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)

def publish_event(job_id: str,event_type:str ,value: float):
    payload = {
        "job_id": job_id,
        "type": event_type,
        "value": round(value, 2) if isinstance(value, (int, float)) else value,
    }
    redis_client.publish("job_progress", json.dumps(payload))
