import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from app.models import User
from app.security import decode_access_token
from app.uow import UnitOfWork

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/user/login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учётные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        login = payload.get("sub")
        if login is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    with UnitOfWork() as uow:
        user = uow.user.get_by_login(login)
        if user is None:
            raise credentials_exception
        uow.session.expunge(user)
        return user
