from fastapi import APIRouter, File, Form, Query, UploadFile, status

from app.schemas import VideoResponse
from app.database import SessionLocal
from app import crud

from typing import Annotated


router = APIRouter()


@router.post("/", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
async def create(
    title: Annotated[str, Form(...)],
    author: Annotated[str, Form(...)],
    course: Annotated[str, Form(...)],
    file: Annotated[UploadFile, File(...)],
):
    return crud.create_video(SessionLocal, title, author, course, file)


@router.post("/upload/", response_model=VideoResponse, status_code=status.HTTP_200_OK)
async def upload(
    video_name: Annotated[str, Form(...)],
    file: Annotated[UploadFile, File(...)],
):
    return crud.update_video_file(SessionLocal, video_name, file)


@router.get("/", response_model=VideoResponse, status_code=status.HTTP_200_OK)
async def get(
    video_name: str,
):
    return crud.get_video(SessionLocal, video_name)


@router.get("/file/", status_code=status.HTTP_200_OK)
async def get_file(
    video_name: Annotated[str, Query(min_length=1, description="Название видео")],
    download: Annotated[bool, Query(description="true - скачать, false - открыть в браузере")] = False,
):
    video = crud.get_video(SessionLocal, video_name)
    return crud.build_video_file_response(video, download=download)


@router.get("/list/", status_code=status.HTTP_200_OK)
async def get_last(
    number: Annotated[int, Query(gt=0, description="Кол-во видео")] = 5,
):
    return crud.get_last_video(SessionLocal, number)
