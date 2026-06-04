from app.models import Course, Video
from sqlalchemy import select

def create_course(session, obj_in):
    with session() as s:
        obj = Course(**obj_in.model_dump())
        s.add(obj)
        s.commit()
        s.refresh(obj)
        return obj


def create_video(session, obj_in):
    with session() as s:
        stmt 


        obj = Video(**obj_in.model_dump())
        s.add(obj)
        s.commit()
        s.refresh(obj)
        return obj