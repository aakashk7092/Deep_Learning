from pathlib import Path
from threading import Lock
from typing import List

import tensorflow as tf

from utils.config import CONFIG
from utils.helpers import read_json


class ModelLoader:
    _model: tf.keras.Model | None = None
    _labels: List[str] | None = None
    _lock = Lock()

    @classmethod
    def load_model(cls, model_path: Path = CONFIG.best_model_keras_path) -> tf.keras.Model:
        if cls._model is None:
            with cls._lock:
                if cls._model is None:
                    if not model_path.exists() or model_path.stat().st_size == 0:
                        raise FileNotFoundError(f"Trained model not found or empty: {model_path}")
                    cls._model = tf.keras.models.load_model(model_path)
        return cls._model

    @classmethod
    def load_labels(cls, labels_path: Path = CONFIG.labels_path) -> List[str]:
        if cls._labels is None:
            with cls._lock:
                if cls._labels is None:
                    if not labels_path.exists() or labels_path.stat().st_size == 0:
                        raise FileNotFoundError(f"Labels file not found or empty: {labels_path}")
                    labels = read_json(labels_path)
                    if isinstance(labels, dict):
                        labels = [labels[str(index)] for index in range(len(labels))]
                    cls._labels = labels
        return cls._labels

    @classmethod
    def reset(cls) -> None:
        with cls._lock:
            cls._model = None
            cls._labels = None
