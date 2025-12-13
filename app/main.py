from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.core.logging import logger
from app.api.ws import job_progress_ws
from app.api.routes.routes import router
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi.staticfiles import StaticFiles



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("init lifespan")
    logger.info("Hello, it's beautiful day!!")
    yield
    logger.info("Good Bye")
    print("clean up lifespan")


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
    app.include_router(router=router, prefix=settings.API_V1_PREFIX)
    return app


app = create_app()


@app.get("/")
async def health():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "name": settings.APP_NAME,
    }


@app.websocket("/ws/jobs/{job_id}")
async def websocket_endpoint(ws: WebSocket, job_id: str):
    await job_progress_ws(ws, job_id)

@app.get("/app")
def index():
    return HTMLResponse(Path("./FE/test.html").read_text())
app.mount("/videos", StaticFiles(directory="outputs"), name="videos")