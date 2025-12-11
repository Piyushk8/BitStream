import sys
from typing import Any, Dict

from loguru import logger
from app.core.config import settings


def setup_logging() -> None:
    # Remove default loguru handler
    logger.remove()

    # In local/dev we can use pretty logs; in prod, JSON logs
    is_local = settings.ENVIRONMENT in ("local", "dev")

    if is_local:
        logger.add(
            sys.stderr,
            level=settings.LOG_LEVEL,
            backtrace=True,
            diagnose=True,
            enqueue=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>",
        )
    else:
        logger.add(
            sys.stdout,
            level=settings.LOG_LEVEL,
            backtrace=False,
            diagnose=False,
            enqueue=True,
            serialize=True,
        )


__all__ = ["logger", "setup_logging"]
