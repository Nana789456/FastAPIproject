from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models import Course, Video, User, RefreshToken


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

    def get_all(self):
            stmt = select(Course)
            return self.session.execute(stmt).all()


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


    def get_introductory(self) -> list[Video]:
        stmt = select(Video).where(
            Video.title.contains('ознакомительное')
        )
        return self.session.execute(stmt).scalars().all()
        

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: User) -> User:
        self.session.add(obj)
        return obj

    def get_by_login(self, login: str) -> User | None:
        stmt = select(User).where(User.login == login)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)


class RefreshTokenRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, obj: RefreshToken) -> RefreshToken:
        self.session.add(obj)
        return obj

    def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        return self.session.execute(stmt).scalar_one_or_none()

    def revoke(self, token_id: int, revoked_at: datetime) -> bool:
        # Условие revoked_at IS NULL не даёт двум параллельным запросам
        # обменять один и тот же токен дважды
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.id == token_id, RefreshToken.revoked_at.is_(None))
            .values(revoked_at=revoked_at)
        )
        return self.session.execute(stmt).rowcount == 1

