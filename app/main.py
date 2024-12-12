from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from .utils.logger import async_info
from .cache import setup_redis_cache
from .api.router import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await async_info("Application is starting up")
    setup_redis_cache(app)
    yield
    # Shutdown
    await async_info("Application is shutting down")


app = FastAPI(
    title="FastAPI App",
    description="FastAPI application with PostgreSQL and logging",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def home():
    return JSONResponse(content={"message": "Welcome to the FastAPI App", "docs": "/docs", "redoc": "/redoc"})


app.include_router(api_router, prefix="/api")
