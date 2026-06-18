from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models import Course, Video
from app.schemas import VideoCreate

from time import time


def create_course(session: sessionmaker[Session], obj_in):
    try:
        with session() as s:
            obj = Course(**obj_in.model_dump())
            s.add(obj)
            s.commit()
            s.refresh(obj)
            return obj
    except IntegrityError:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = 'Такой курс уже есть'
        )
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Необработанная ошибка: {e}"
        )

def get_course(session: sessionmaker[Session], course_name: str):
    with session() as s:
        stmt = select(Course).where(Course.name == course_name)
        obj: Course = s.execute(stmt).scalar_one_or_none()

        if not obj:
            raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Курс с таким названием не найден'
            )
    return obj

def get_course(session: sessionmaker[Session], course_name: str):
    with session() as s:
        stmt = select(Course).where(Course.name == course_name)
        obj: Course = s.execute(stmt).scalar_one_or_none()

        if not obj:
            raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Курс с таким названием не найден'
            )
    return obj

def get_last_courses(session: sessionmaker[Session], number: int):
    with session() as s:

        objs: list[Course] = s.query(Course).order_by(Course.name).limit(number).all()

        if not objs:
            raise HTTPException(
            status_code = 404,
            detail = 'В базе НЕТ курсов'
        )

        names_str = objs[0].name
        if len(objs) > 1:
            for obj in objs[1:]:
                names_str += ', ' + obj.name

        return names_str
    

def create_video(session: sessionmaker[Session], obj_in: VideoCreate):
    with session() as s:

        # Достаём название курса из входных данных
        course_name = obj_in.course

        # Получение курса по его названию
        stmt = select(Course).where(Course.name == course_name)
        # execute - выполнение запроса stmt, scalar_one_or_none - получение одного экземпляра модеои ИЛИ None 
        course: Course = s.execute(stmt).scalar_one_or_none() 

        if not course:
            raise HTTPException(
               status_code = 404,
               detail = 'Курс с таким названием не найден, поэтому создать видео нельзя'
            )

        obj = Video(
            title=obj_in.title,
            author=obj_in.author,
            file_path=f"{course_name}_{time()}.mp3",
            course_id=course.id,
        )
        s.add(obj)
        s.commit()
        s.refresh(obj)
        return obj

def get_video(session: sessionmaker[Session], video_name: str):
    with session() as s:
        stmt = select(Video).where(Video.title == video_name)
        video: Video = s.execute(stmt).scalar_one_or_none()

        if not video:
            raise HTTPException(
            status_code = 404,
            detail = 'Видео с таким названием не найден'
            )
        

    return video

def get_last_video(session: sessionmaker[Session], number: int):
    with session() as s:

        objs: list[Video] = s.query(Video).order_by(Video.title).limit(number).all()

        if not objs:
            raise HTTPException(
            status_code = 404,
            detail = 'В базе НЕТ курсов'
        )

        titles_str = objs[0].title
        if len(objs) > 1:
            for obj in objs[1:]:
                titles_str += ', ' + obj.title

        return titles_str

