import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

import numpy as np
import tensorflow as tf


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def ensure_directories(paths: Iterable[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def set_global_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)


def list_image_files(directory: Path) -> List[Path]:
    return sorted(path for path in directory.rglob("*") if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS)


def class_names_from_directory(directory: Path) -> List[str]:
    return sorted(path.name for path in directory.iterdir() if path.is_dir())


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def label_to_plant_disease(label: str) -> Dict[str, str]:
    cleaned = label.replace("___", "__").strip()
    if "__" in cleaned:
        plant, disease = cleaned.split("__", 1)
    elif "_" in cleaned:
        plant, disease = cleaned.split("_", 1)
    else:
        plant, disease = "Unknown Plant", cleaned
    return {
        "plant_name": plant.replace("_", " ").title(),
        "disease_name": disease.replace("_", " ").title(),
    }


def severity_from_prediction(disease_name: str, confidence: float) -> str:
    if disease_name.lower() == "healthy":
        return "Healthy"
    if confidence >= 0.90:
        return "Severe"
    if confidence >= 0.70:
        return "Moderate"
    return "Mild"
