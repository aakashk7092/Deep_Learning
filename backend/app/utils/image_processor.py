import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from PIL import Image

from app.config.settings import get_settings
from app.schemas.prediction_schema import ModelPrediction


logger = logging.getLogger(__name__)


class ImageProcessor:
    image_size: Tuple[int, int] = (224, 224)
    _model = None
    _labels: List[str] | Dict[str, str] | None = None

    @classmethod
    def preprocess_image(cls, source_path: Path, processed_path: Path | None = None) -> np.ndarray:
        with Image.open(source_path) as image:
            image = image.convert("RGB").resize(cls.image_size)
            if processed_path:
                processed_path.parent.mkdir(parents=True, exist_ok=True)
                image.save(processed_path, format="JPEG", quality=92)
            array = np.asarray(image, dtype=np.float32) / 255.0
        return np.expand_dims(array, axis=0)

    @classmethod
    def predict(cls, image_array: np.ndarray) -> ModelPrediction:
        model = cls._load_model()
        labels = cls._load_labels()
        raw_prediction = model.predict(image_array, verbose=0)
        scores = np.asarray(raw_prediction)[0]
        class_index = int(np.argmax(scores))
        confidence = float(scores[class_index])
        label = cls._label_for_index(labels, class_index)
        plant_name, disease_name = cls._parse_label(label)
        return ModelPrediction(
            plant_name=plant_name,
            disease_name=disease_name,
            confidence=round(confidence, 4),
            severity=cls._severity(confidence, disease_name),
        )

    @classmethod
    def _load_model(cls):
        if cls._model is None:
            settings = get_settings()
            if not settings.model_path.exists():
                raise FileNotFoundError(f"TensorFlow model not found at {settings.model_path}")
            import tensorflow as tf

            cls._model = tf.keras.models.load_model(settings.model_path)
            logger.info("Loaded TensorFlow model from %s", settings.model_path)
        return cls._model

    @classmethod
    def _load_labels(cls):
        if cls._labels is None:
            settings = get_settings()
            if not settings.labels_path.exists():
                raise FileNotFoundError(f"Labels file not found at {settings.labels_path}")
            with settings.labels_path.open("r", encoding="utf-8") as file:
                cls._labels = json.load(file)
            logger.info("Loaded model labels from %s", settings.labels_path)
        return cls._labels

    @staticmethod
    def _label_for_index(labels: List[str] | Dict[str, str], index: int) -> str:
        if isinstance(labels, list):
            return labels[index]
        return labels.get(str(index)) or labels.get(index) or labels.get(f"class_{index}") or str(index)

    @staticmethod
    def _parse_label(label: str) -> Tuple[str, str]:
        cleaned = label.replace("___", "__").replace("-", " ").strip()
        if "__" in cleaned:
            plant, disease = cleaned.split("__", 1)
        elif "_" in cleaned:
            plant, disease = cleaned.split("_", 1)
        else:
            plant, disease = "Unknown Plant", cleaned
        return plant.replace("_", " ").title(), disease.replace("_", " ").title()

    @staticmethod
    def _severity(confidence: float, disease_name: str) -> str:
        if disease_name.lower() == "healthy":
            return "Healthy"
        if confidence >= 0.90:
            return "Severe"
        if confidence >= 0.70:
            return "Moderate"
        return "Mild"
