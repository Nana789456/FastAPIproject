from fastapi import HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.crud import _delete_file, _store_video_file, build_video_file_response
from app.config import settings
from app.models import Course, Video, User, RefreshToken
from app.schemas import Token
from app.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from app.uow import UnitOfWork
from datetime import datetime, timedelta, timezone
import json


class CourseService:
    def __init__(self, uow_factory=UnitOfWork):
        self.uow_factory = uow_factory

    def create_course(self, obj_in):
        try:
            with self.uow_factory() as uow:
                if uow.courses is None or uow.session is None:
                    raise RuntimeError("UoW не инициализирован")
                course = Course(**obj_in.model_dump())
                uow.courses.add(course)
                uow.flush()
                uow.commit()
                uow.session.refresh(course)
                return course
        except HTTPException:
            raise
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Такой курс уже есть",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Необработанная ошибка: {e}",
            )


    def get_course(self, course_name: str):
        with self.uow_factory() as uow:
            if uow.courses is None:
                raise RuntimeError("UoW не инициализирован")
            course = uow.courses.get_by_name(course_name)

            if not course:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Курс с таким названием не найден",
                )

            return course

    def get_last_courses(self, number: int):
        with self.uow_factory() as uow:
            if uow.courses is None:
                raise RuntimeError("UoW не инициализирован")
            courses = uow.courses.list_last(number)

            if not courses:
                raise HTTPException(
                    status_code=404,
                    detail="В базе НЕТ курсов",
                )

            names = [course.name for course in courses]
            return ", ".join(names)


class VideoService:
    def __init__(self, uow_factory=UnitOfWork):
        self.uow_factory = uow_factory

    def create(self, title, author, course, file):
        try:
            with self.uow_factory() as uow:
                if uow.video is None or uow.courses is None or uow.session is None:
                    raise RuntimeError("UoW не инициализирован")

                course_obj = uow.courses.get_by_name(course)
                if not course_obj:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Курс с таким названием не найден, поэтому создать видео нельзя",
                    )

                file_path = _store_video_file(file)

                video = Video(
                    title=title,
                    author=author,
                    file_path=file_path,
                    course_id=course_obj.id,
                )
                uow.video.add(video)
                uow.commit()
                uow.session.refresh(video)
                return video
        except HTTPException:
            raise
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Такое видео уже есть",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Необработанная ошибка: {e}",
            )

    def upload(self, video_name: str, file: UploadFile):
        try:
            with self.uow_factory() as uow:
                if uow.video is None or uow.session is None:
                    raise RuntimeError("UoW не инициализирован")

                video = uow.video.get_by_title(video_name)
                if not video:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Видео с таким названием не найдено",
                    )

                old_file_path = video.file_path
                video.file_path = _store_video_file(file)

                uow.commit()
                uow.session.refresh(video)

            _delete_file(old_file_path)
            return video
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Необработанная ошибка: {e}",
            )

    def get(self, video_name: str) -> Video:
        with self.uow_factory() as uow:
            if uow.video is None:
                raise RuntimeError("UoW не инициализирован")
            video = uow.video.get_by_title(video_name)

            if not video:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Видео с таким названием не найдено",
                )

            return video

    def get_file(self, video_name: str, download: bool = False) -> FileResponse:
        video = self.get(video_name)
        return build_video_file_response(video, download=download)

    def get_last(self, number: int):
        with self.uow_factory() as uow:
            if uow.video is None:
                raise RuntimeError("UoW не инициализирован")
            videos = uow.video.list_last(number)

            if not videos:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="В базе НЕТ видео",
                )

            titles = [video.title for video in videos]
            return ", ".join(titles)
        
class UserService:
    def __init__(self, uow_factory=UnitOfWork):
        self.uow_factory = uow_factory

    def create(self, obj_in):
        try:
            with self.uow_factory() as uow:
                if uow.user is None or uow.session is None:
                    raise RuntimeError("UoW не инициализирован")

                videos: list[Video] = uow.video.get_introductory()
                videos_names = json.dumps([video.title for video in videos], ensure_ascii=False)

                user_data = obj_in.model_dump(exclude={"password"})
                user_data["accessible_videos"] = videos_names
                user = User(**user_data, hashed_password=hash_password(obj_in.password))
                uow.user.add(user)
                uow.commit()
                uow.session.refresh(user)
                return user
        except HTTPException:
            raise
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Такой пользователь уже есть",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Необработанная ошибка: {e}",
            )

    def login(self, login: str, password: str) -> tuple[Token, str]:
        """Возвращает access-токен (для тела ответа) и refresh-токен (для cookie)."""
        with self.uow_factory() as uow:
            if uow.user is None or uow.refresh_tokens is None:
                raise RuntimeError("UoW не инициализирован")

            user = uow.user.get_by_login(login)
            if user is None or not verify_password(password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверный логин или пароль",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            tokens = self._issue_tokens(uow, user)
            uow.commit()
            return tokens

    def refresh(self, raw_refresh_token: str | None) -> tuple[Token, str]:
        """Обменивает refresh-токен на новую пару; старый refresh-токен отзывается (ротация)."""
        invalid_token_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh-токен недействителен",
        )
        if not raw_refresh_token:
            raise invalid_token_exception

        with self.uow_factory() as uow:
            if uow.user is None or uow.refresh_tokens is None:
                raise RuntimeError("UoW не инициализирован")

            now = datetime.now(timezone.utc)
            stored = uow.refresh_tokens.get_by_hash(hash_refresh_token(raw_refresh_token))
            if stored is None or stored.revoked_at is not None:
                raise invalid_token_exception

            expires_at = stored.expires_at
            # SQLite не хранит часовой пояс и возвращает naive datetime
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            if expires_at <= now:
                raise invalid_token_exception

            if not uow.refresh_tokens.revoke(stored.id, now):
                raise invalid_token_exception

            user = uow.user.get_by_id(stored.user_id)
            if user is None:
                raise invalid_token_exception

            tokens = self._issue_tokens(uow, user)
            uow.commit()
            return tokens

    def logout(self, raw_refresh_token: str | None) -> None:
        if not raw_refresh_token:
            return

        with self.uow_factory() as uow:
            if uow.refresh_tokens is None:
                raise RuntimeError("UoW не инициализирован")

            stored = uow.refresh_tokens.get_by_hash(hash_refresh_token(raw_refresh_token))
            if stored is None:
                return

            uow.refresh_tokens.revoke(stored.id, datetime.now(timezone.utc))
            uow.commit()

    @staticmethod
    def _issue_tokens(uow: UnitOfWork, user: User) -> tuple[Token, str]:
        raw_refresh_token = create_refresh_token()
        uow.refresh_tokens.add(
            RefreshToken(
                user_id=user.id,
                token_hash=hash_refresh_token(raw_refresh_token),
                expires_at=datetime.now(timezone.utc)
                + timedelta(days=settings.refresh_token_expire_days),
            )
        )
        access_token = create_access_token(subject=user.login)
        return Token(access_token=access_token), raw_refresh_token