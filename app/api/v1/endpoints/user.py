from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_current_user
from app.models import User
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


@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
