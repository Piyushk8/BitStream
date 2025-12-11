from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import logger
from app.api.routes.routes import router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("init lifespan")
    logger.info("Hello, it's beautiful day!!")
    yield
    logger.info("Good Bye")
    print("clean up lifespan")


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
    app.include_router(router=router,prefix=settings.API_V1_PREFIX)
    return app


app = create_app()


@app.get("/")
async def health():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "name": settings.APP_NAME,
    }
