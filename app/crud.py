from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session

from app.models import Course, Video
from app.schemas import VideoCreate

from time import time


def create_course(session: sessionmaker[Session], obj_in):
    with session() as s:
        obj = Course(**obj_in.model_dump())
        s.add(obj)
        s.commit()
        s.refresh(obj)
        return obj


def create_video(session: sessionmaker[Session], obj_in: VideoCreate):
    with session() as s:

        # Достаём название курса из входных данных
        course_name = obj_in.course

        # Получение курса по его названию
        stmt = select(Course).where(Course.name == course_name)
        # execute - выполнение запроса stmt, scalar_one_or_none - получение одного экземпляра модеои ИЛИ None 
        course: Course = s.execute(stmt).scalar_one_or_none() 

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
    