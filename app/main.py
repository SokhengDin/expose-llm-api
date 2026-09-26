import sys

from fastapi import FastAPI
from loguru import logger

from app.middleware import LoggingMiddleware
from app.routes import router

logger.remove()
logger.add(sys.stdout, level="INFO", enqueue=True)

app = FastAPI(title="expose-llm-api")
app.add_middleware(LoggingMiddleware)
app.include_router(router)
