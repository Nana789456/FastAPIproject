from fastapi import FastAPI
from app.api.v1.endpoints import course, video


app = FastAPI(title="Course Warehouse")

app.include_router(course.router, prefix="/v1/course", tags=["course"])
app.include_router(video.router, prefix="/v1/video", tags=["video"])
