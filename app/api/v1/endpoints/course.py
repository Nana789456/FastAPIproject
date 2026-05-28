from fastapi import APIRouter, status

from app.schemas import CourseCreate, CourseResponse
from app.database import SessionLocal
from app import crud


router = APIRouter()


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    obj_in: CourseCreate,
):
    return crud.create_course(SessionLocal, obj_in)
