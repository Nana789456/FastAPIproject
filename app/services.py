from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.crud import _store_video_file
from app.models import Course, Video
from app.uow import UnitOfWork


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
"""
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
"""