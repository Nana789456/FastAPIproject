from fastapi import APIRouter, status

from app.schemas import VideoCreate, VideoResponse
from app.database import SessionLocal
from app import crud


router = APIRouter()


@router.post("/", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
async def create(
    obj_in: VideoCreate,
):
    return crud.create_video(SessionLocal, obj_in)
