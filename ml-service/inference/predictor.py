from pathlib import Path
from typing import Dict, List

import numpy as np

from inference.model_loader import ModelLoader
from preprocessing.preprocessing import preprocess_image_file
from training.gradcam import save_gradcam_overlay
from utils.config import CONFIG
from utils.helpers import label_to_plant_disease, severity_from_prediction


class PlantDiseasePredictor:
    def __init__(self, model_path: Path = CONFIG.best_model_keras_path, labels_path: Path = CONFIG.labels_path) -> None:
        self.model_path = model_path
        self.labels_path = labels_path
        self.model = ModelLoader.load_model(model_path)
        self.labels = ModelLoader.load_labels(labels_path)

    def predict(self, image_path: str | Path, explain: bool = True) -> Dict:
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        image_array = preprocess_image_file(image_path)
        probabilities = self.model.predict(image_array, verbose=0)[0]
        top_indices = np.argsort(probabilities)[::-1][:5]
        top_predictions = [self._format_prediction(index, probabilities) for index in top_indices]
        best = top_predictions[0]

        gradcam_path = None
        if explain:
            output_path = CONFIG.reports_dir / "gradcam" / f"{image_path.stem}_gradcam.jpg"
            gradcam_path, _ = save_gradcam_overlay(image_path, self.model, output_path)

        return {
            "plant_name": best["plant_name"],
            "disease_name": best["disease_name"],
            "confidence": best["confidence"],
            "severity": severity_from_prediction(best["disease_name"], best["confidence"]),
            "top_predictions": [
                {"label": item["label"], "confidence": item["confidence"]}
                for item in top_predictions
            ],
            "gradcam_image": str(gradcam_path) if gradcam_path else None,
        }

    def _format_prediction(self, index: int, probabilities: np.ndarray) -> Dict:
        label = self.labels[index]
        parsed = label_to_plant_disease(label)
        return {
            "label": label,
            "plant_name": parsed["plant_name"],
            "disease_name": parsed["disease_name"],
            "confidence": round(float(probabilities[index]), 4),
        }
