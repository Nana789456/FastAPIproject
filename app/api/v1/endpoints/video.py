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


"""
import shutil
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI()

# Папка для сохранения видео
UPLOAD_DIR = Path("media")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    # Проверка расширения файла
    if file.content_type != "video/mp4":
        raise HTTPException(status_code=400, detail="Только файлы .mp4 разрешены")

    file_path = UPLOAD_DIR / file.filename

    # Асинхронное сохранение файла на диск
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "message": "Файл успешно загружен"}
"""

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
