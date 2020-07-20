
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_root():
    return {"Hello": "Universe"}

@router.get("/healthz")
async def healthz():
    return "OK"
