from fastapi import APIRouter, status

from app.schemas import CourseCreate, CourseResponse
from app.database import SessionLocal
from app import crud

from typing import Annotated
from fastapi import Query


router = APIRouter()


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create(
    obj_in: CourseCreate,
):
    return crud.create_course(SessionLocal, obj_in)

@router.get("/", response_model=CourseResponse, status_code=status.HTTP_200_OK)
async def get(
    name: Annotated[str, Query(min_length=1, description="Поисковый запрос на кириллице")]
):
    return crud.get_course(SessionLocal, name)

@router.get("/list/", status_code=status.HTTP_200_OK)
async def get_last(
    number: Annotated[int, Query(gt=0, description="Кол-во курсов")] = 5,
):
    return crud.get_last_courses(SessionLocal, number)
