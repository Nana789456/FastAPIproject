from fastapi import FastAPI
from app.api.v1.endpoints import course


app = FastAPI(title="Course Warehouse")

app.include_router(course.router, prefix="/v1/course", tags=["course"])