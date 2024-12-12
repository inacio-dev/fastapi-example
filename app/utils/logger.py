import sys
from loguru import logger
from pydantic import BaseModel


class LogConfig(BaseModel):
    LOGGER_NAME: str = "fastapi_app"
    LOG_FORMAT: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "loguru.logger",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 1000000,
            "backupCount": 3,
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default", "file"], "level": LOG_LEVEL},
    }


def async_log(level, message):
    """Asynchronous logging function."""
    logger.log(level, message)


# Configure loguru
config = LogConfig()
logger.remove()
logger.add(sys.stdout, format=config.LOG_FORMAT, level=config.LOG_LEVEL)
logger.add("app.log", rotation="500 MB", level=config.LOG_LEVEL)


# Create logging functions that work in both sync and async contexts
def log_debug(msg):
    async_log("DEBUG", msg)


def log_info(msg):
    async_log("INFO", msg)


def log_warning(msg):
    async_log("WARNING", msg)


def log_error(msg):
    async_log("ERROR", msg)


def log_critical(msg):
    async_log("CRITICAL", msg)


# Async versions for use in async contexts
async def async_debug(msg):
    log_debug(msg)


async def async_info(msg):
    log_info(msg)


async def async_warning(msg):
    log_warning(msg)


async def async_error(msg):
    log_error(msg)


async def async_critical(msg):
    log_critical(msg)
