from fastapi import APIRouter
from app.core.config import settings
from app.api.routes.video_routes import videos_router
from app.api.routes.job_routes import jobs_router

router = APIRouter()

router.include_router(videos_router, prefix="/videos", tags=["vidoes"])
router.include_router(jobs_router, prefix="/jobs", tags=["Jobs"])
