from fastapi import APIRouter

from rest_api.controller import file_upload, update_embeddings
from rest_api.controller import search, feedback, health

router = APIRouter()

router.include_router(health.router, tags=["health"])
router.include_router(search.router, tags=["search"])
router.include_router(feedback.router, tags=["feedback"])
router.include_router(file_upload.router, tags=["file-upload"])
router.include_router(update_embeddings.router, tags=["update-embeddings"])
