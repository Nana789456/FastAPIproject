from fastapi import APIRouter, status

from app.schemas import VideoCreate, VideoResponse
from app.database import SessionLocal
from app import crud

from typing import Annotated
from fastapi import Query


router = APIRouter()


@router.post("/", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
async def create(
    obj_in: VideoCreate,
):
    return crud.create_video(SessionLocal, obj_in)


@router.get("/", response_model=VideoResponse, status_code=status.HTTP_200_OK)
async def get(
    video_name: str,
):
    return crud.get_video(SessionLocal, video_name)

@router.get("/list/", status_code=status.HTTP_200_OK)
async def get_last(
    number: Annotated[int, Query(gt=0, description="Кол-во видео")] = 5,
):
    return crud.get_last_video(SessionLocal, number)
