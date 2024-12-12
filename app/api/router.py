from fastapi import APIRouter
from .endpoints import base

router = APIRouter()
router.include_router(base.router, prefix="/base", tags=["base"])
