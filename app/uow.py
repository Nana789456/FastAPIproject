from typing import Callable

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.repositories import CourseRepository, VideoRepository


class UnitOfWork:
    def __init__(self, session_factory: Callable[[], Session] = SessionLocal):
        self.session_factory = session_factory
        self.session: Session | None = None
        self.courses: CourseRepository | None = None
        self.video: VideoRepository | None = None

    def __enter__(self):
        self.session = self.session_factory()
        self.courses = CourseRepository(self.session)
        self.video = VideoRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                self.rollback()
        finally:
            self.close()

    def commit(self):
        if self.session is None:
            raise RuntimeError("Сессия UoW не инициализирована")
        self.session.commit()

    def flush(self):
        if self.session is None:
            raise RuntimeError("Сессия UoW не инициализирована")
        self.session.flush()

    def rollback(self):
        if self.session is None:
            raise RuntimeError("Сессия UoW не инициализирована")
        self.session.rollback()

    def close(self):
        if self.session is not None:
            self.session.close()
            self.session = None
            self.courses = None
