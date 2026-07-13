from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Course, Video


class CourseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, course: Course) -> Course:
        self.session.add(course)
        return course

    def get_by_name(self, course_name: str) -> Course | None:
        stmt = select(Course).where(Course.name == course_name)
        return self.session.execute(stmt).scalar_one_or_none()

    def list_last(self, number: int) -> list[Course]:
        return (
            self.session.query(Course)
            .order_by(Course.name)
            .limit(number)
            .all()
        )

class VideoRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, video: Video) -> Video:
        self.session.add(video)
        return video

    def get_by_title(self, title: str) -> Video | None:
        stmt = select(Video).where(Video.title == title)
        return self.session.execute(stmt).scalar_one_or_none()

    def list_last(self, number: int) -> list[Video]:
        return (
            self.session.query(Video)
            .order_by(Video.title)
            .limit(number)
            .all()
        )