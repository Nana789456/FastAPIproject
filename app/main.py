from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.endpoints import course, video


app = FastAPI(title="Course Warehouse")

media_dir = Path("media")
media_dir.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=media_dir), name="media")

app.include_router(course.router, prefix="/v1/course", tags=["course"])
app.include_router(video.router, prefix="/v1/video", tags=["video"])
