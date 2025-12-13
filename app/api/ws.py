from fastapi import WebSocket, WebSocketDisconnect
from app.core.redis import async_redis_client
from app.api.jobs.store import job_store
import asyncio
import json


async def job_progress_ws(websocket: WebSocket, job_id: str):
    await websocket.accept()

    job = job_store.get_job(job_id)

    if job:
        await websocket.send_json(
            {"type": "state", "status": job.status, "progress": job.progress}
        )
    pubsub = async_redis_client.pubsub()
    await pubsub.subscribe("job_progress")

    try:
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            data = json.loads(message["data"])

            if data["job_id"] == job_id:
                await websocket.send_json(data)

    except WebSocketDisconnect:
        await pubsub.unsubscribe("job_progress")
