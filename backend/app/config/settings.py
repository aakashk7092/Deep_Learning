from functools import lru_cache
from pathlib import Path
import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator


BASE_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = BASE_DIR.parent
load_dotenv(BASE_DIR / ".env")


class Settings(BaseModel):
    app_name: str = "Plant Disease Detection API"
    app_version: str = "1.0.0"
    environment: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    debug: bool = Field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")

    mongodb_uri: str = Field(default_factory=lambda: os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
    database_name: str = Field(default_factory=lambda: os.getenv("DATABASE_NAME", "plant_disease_detection"))

    jwt_secret: str = Field(default_factory=lambda: os.getenv("JWT_SECRET", "change-this-development-secret"))
    jwt_algorithm: str = Field(default_factory=lambda: os.getenv("JWT_ALGORITHM", "HS256"))
    access_token_expire_minutes: int = Field(default_factory=lambda: int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")))
    refresh_token_expire_days: int = Field(default_factory=lambda: int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")))

    model_path: Path = Field(default_factory=lambda: Path(os.getenv("MODEL_PATH", PROJECT_DIR / "ml-service" / "saved_models" / "best_model.keras")))
    labels_path: Path = Field(default_factory=lambda: Path(os.getenv("LABELS_PATH", PROJECT_DIR / "ml-service" / "saved_models" / "labels.json")))

    upload_dir: Path = Field(default_factory=lambda: Path(os.getenv("UPLOAD_DIR", BASE_DIR / "uploads")))
    max_upload_size_mb: int = Field(default_factory=lambda: int(os.getenv("MAX_UPLOAD_SIZE_MB", "10")))
    allowed_image_types: List[str] = Field(default_factory=lambda: ["image/jpeg", "image/png", "image/webp"])
    cors_origins: List[str] = Field(default_factory=lambda: [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",") if origin.strip()])

    @field_validator("model_path", "labels_path", "upload_dir")
    @classmethod
    def resolve_path(cls, value: Path) -> Path:
        return value if value.is_absolute() else (BASE_DIR / value).resolve()

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def original_upload_dir(self) -> Path:
        return self.upload_dir / "original"

    @property
    def processed_upload_dir(self) -> Path:
        return self.upload_dir / "processed"

    @property
    def prediction_upload_dir(self) -> Path:
        return self.upload_dir / "predictions"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    for directory in (settings.original_upload_dir, settings.processed_upload_dir, settings.prediction_upload_dir):
        directory.mkdir(parents=True, exist_ok=True)
    return settings
