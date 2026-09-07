from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import Token, UserCreate, UserResponse
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


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return service.login(form_data.username, form_data.password)
