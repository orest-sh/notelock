from contextlib import asynccontextmanager

from app.core.settings import settings
from app.routers.notes import router as notes_router

import redis.asyncio as redis

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter


@asynccontextmanager
async def lifespan(_app: FastAPI):
    redis_connection = redis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(notes_router)
