import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.models import Course, Video

SUPPORTED_VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov"}
SUPPORTED_VIDEO_MEDIA_TYPES = {
    ".mp4": "video/mp4",
    ".mkv": "video/x-matroska",
    ".mov": "video/quicktime",
}


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
            status_code=status.HTTP_409_CONFLICT,
            detail="Такой курс уже есть",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Необработанная ошибка: {e}",
        )


def get_course(session: sessionmaker[Session], course_name: str):
    with session() as s:
        stmt = select(Course).where(Course.name == course_name)
        obj: Course = s.execute(stmt).scalar_one_or_none()

        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Курс с таким названием не найден",
            )
    return obj


def get_last_courses(session: sessionmaker[Session], number: int):
    with session() as s:
        objs: list[Course] = s.query(Course).order_by(Course.name).limit(number).all()

        if not objs:
            raise HTTPException(
                status_code=404,
                detail="В базе НЕТ курсов",
            )

        names_str = objs[0].name
        if len(objs) > 1:
            for obj in objs[1:]:
                names_str += ", " + obj.name

        return names_str


def _video_suffix(file: UploadFile) -> str:
    suffix = Path(file.filename or "").suffix.lower()

    if suffix not in SUPPORTED_VIDEO_EXTENSIONS:
        allowed = ", ".join(sorted(ext.lstrip(".") for ext in SUPPORTED_VIDEO_EXTENSIONS))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Разрешены только видео в форматах: {allowed}",
        )

    return suffix


def _media_type_for_path(file_path: str) -> str | None:
    suffix = Path(file_path).suffix.lower()
    return SUPPORTED_VIDEO_MEDIA_TYPES.get(suffix)


def _store_video_file(file: UploadFile) -> str:
    suffix = _video_suffix(file)

    upload_dir = Path("media")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{uuid4().hex}{suffix}"
    file_path = upload_dir / file_name

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(file_path)


def _delete_file(file_path: str) -> None:
    Path(file_path).unlink(missing_ok=True)


def create_video(
    session: sessionmaker[Session],
    title: str,
    author: str,
    course_name: str,
    file: UploadFile,
):
    with session() as s:
        stmt = select(Course).where(Course.name == course_name)
        course: Course = s.execute(stmt).scalar_one_or_none()

        if not course:
            raise HTTPException(
                status_code=404,
                detail="Курс с таким названием не найден, поэтому создать видео нельзя",
            )

        file_path = _store_video_file(file)

        obj = Video(
            title=title,
            author=author,
            file_path=file_path,
            course_id=course.id,
        )
        s.add(obj)
        s.commit()
        s.refresh(obj)
        return obj


def update_video_file(
    session: sessionmaker[Session],
    video_name: str,
    file: UploadFile,
):
    with session() as s:
        stmt = select(Video).where(Video.title == video_name)
        video: Video = s.execute(stmt).scalar_one_or_none()

        if not video:
            raise HTTPException(
                status_code=404,
                detail="Видео с таким названием не найдено",
            )

        old_file_path = video.file_path
        new_file_path = _store_video_file(file)

        video.file_path = new_file_path
        s.add(video)
        s.commit()
        s.refresh(video)

    _delete_file(old_file_path)
    return video


def get_video(session: sessionmaker[Session], video_name: str):
    with session() as s:
        stmt = select(Video).where(Video.title == video_name)
        video: Video = s.execute(stmt).scalar_one_or_none()

        if not video:
            raise HTTPException(
                status_code=404,
                detail="Видео с таким названием не найден",
            )

    return video


def get_last_video(session: sessionmaker[Session], number: int):
    with session() as s:
        objs: list[Video] = s.query(Video).order_by(Video.title).limit(number).all()

        if not objs:
            raise HTTPException(
            status_code = 404,
            detail = 'В базе НЕТ видео'
        )

        titles_str = objs[0].title
        if len(objs) > 1:
            for obj in objs[1:]:
                titles_str += ", " + obj.title

        return titles_str


def build_video_file_response(video: Video, download: bool = False) -> FileResponse:
    file_path = Path(video.file_path)
    media_type = _media_type_for_path(video.file_path)
    disposition = "attachment" if download else "inline"

    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=file_path.name,
        content_disposition_type=disposition,
    )
