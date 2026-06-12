from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.config.settings import get_settings
from app.utils.response_handler import raise_http_error


class UploadValidator:
    @staticmethod
    async def validate_image(file: UploadFile) -> bytes:
        settings = get_settings()
        if file.content_type not in settings.allowed_image_types:
            raise_http_error(status.HTTP_400_BAD_REQUEST, "Only JPEG, PNG, and WEBP images are allowed")

        content = await file.read()
        await file.seek(0)
        if not content:
            raise_http_error(status.HTTP_400_BAD_REQUEST, "Uploaded file is empty")
        if len(content) > settings.max_upload_size_bytes:
            raise_http_error(status.HTTP_400_BAD_REQUEST, f"Image size must be {settings.max_upload_size_mb}MB or less")

        try:
            with Image.open(file.file) as image:
                image.verify()
        except (UnidentifiedImageError, OSError):
            raise_http_error(status.HTTP_400_BAD_REQUEST, "Uploaded file is not a valid image")
        finally:
            await file.seek(0)
        return content

    @staticmethod
    def secure_filename(original_name: str) -> str:
        extension = Path(original_name or "image.jpg").suffix.lower()
        if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
            extension = ".jpg"
        return f"{uuid4().hex}{extension}"
