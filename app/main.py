import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.middleware import LoggingMiddleware
from app.routes import aclose_client, router

logger.remove()
logger.add(sys.stdout, level="INFO", enqueue=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await aclose_client()


app = FastAPI(title="expose-llm-api", lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
app.include_router(router)
