from fastapi import APIRouter, File, Form, Query, UploadFile, status

from app.schemas import UserCreate, UserResponse
from app.services import UserService

from typing import Annotated


router = APIRouter()
service = UserService()


@router.post("/", 
             response_model=UserResponse, 
             status_code=status.HTTP_201_CREATED
        )
async def create(
    obj_in: UserCreate,
):
    return service.create(obj_in)
