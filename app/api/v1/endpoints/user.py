from fastapi import APIRouter, Cookie, Depends, File, Form, Query, Response, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings
from app.dependencies import get_current_user
from app.models import User
from app.schemas import Token, UserCreate, UserResponse
from app.services import UserService

from typing import Annotated


router = APIRouter()
service = UserService()

REFRESH_COOKIE_NAME = "refresh_token"
# Должен совпадать с префиксом роутера в main.py: cookie уходит только на /v1/user/*,
# а не с каждым запросом к API
REFRESH_COOKIE_PATH = "/v1/user"


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        path=REFRESH_COOKIE_PATH,
        httponly=True,
        secure=settings.refresh_cookie_secure,
        samesite="strict",
    )


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
    response: Response,
):
    token, refresh_token = service.login(form_data.username, form_data.password)
    _set_refresh_cookie(response, refresh_token)
    return token


@router.post("/refresh", response_model=Token)
async def refresh(
    response: Response,
    refresh_token: Annotated[str | None, Cookie(alias=REFRESH_COOKIE_NAME)] = None,
):
    token, new_refresh_token = service.refresh(refresh_token)
    _set_refresh_cookie(response, new_refresh_token)
    return token


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    response: Response,
    refresh_token: Annotated[str | None, Cookie(alias=REFRESH_COOKIE_NAME)] = None,
):
    service.logout(refresh_token)
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path=REFRESH_COOKIE_PATH,
        httponly=True,
        secure=settings.refresh_cookie_secure,
        samesite="strict",
    )


@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
