import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from app.models import Video

SUPPORTED_VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".webm"}
SUPPORTED_VIDEO_MEDIA_TYPES = {
    ".mp4": "video/mp4",
    ".mkv": "video/x-matroska",
    ".mov": "video/quicktime",
    ".webm": "video/webm",
}


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
