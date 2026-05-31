from app.models import Course


def create_course(session, obj_in):
    with session() as s:
        obj = Course(**obj_in.model_dump())
        s.add(obj)
        s.commit()
        s.refresh(obj)
        return obj
