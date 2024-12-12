import os
import redis
from fastapi import FastAPI

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"), port=int(os.getenv("REDIS_PORT", 6379)), db=0, decode_responses=True
)


def setup_redis_cache(app: FastAPI):
    app.state.redis = redis_client
