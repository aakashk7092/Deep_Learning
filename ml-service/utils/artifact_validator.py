import argparse
from pathlib import Path
from typing import Dict

from utils.config import CONFIG
from utils.helpers import list_image_files, read_json, write_json


REQUIRED_REPORTS = [
    "accuracy_curve.png",
    "loss_curve.png",
    "confusion_matrix.png",
    "classification_report.txt",
    "roc_curves.png",
    "prediction_examples.png",
    "evaluation_metrics.json",
]


def file_ready(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def directory_has_images(path: Path) -> bool:
    return path.exists() and path.is_dir() and bool(list_image_files(path))


def validate_artifacts() -> Dict:
    report = {
        "raw_dataset_ready": directory_has_images(CONFIG.raw_dataset_dir),
        "processed_train_ready": directory_has_images(CONFIG.train_dir),
        "processed_val_ready": directory_has_images(CONFIG.val_dir),
        "processed_test_ready": directory_has_images(CONFIG.test_dir),
        "best_model_keras_ready": file_ready(CONFIG.best_model_keras_path),
        "best_model_h5_ready": file_ready(CONFIG.best_model_h5_path),
        "labels_ready": file_ready(CONFIG.labels_path),
        "metadata_ready": file_ready(CONFIG.metadata_path),
        "reports": {name: file_ready(CONFIG.reports_dir / name) for name in REQUIRED_REPORTS},
    }
    report["ready_for_training"] = report["raw_dataset_ready"]
    report["ready_for_inference"] = report["best_model_keras_ready"] and report["labels_ready"]
    report["ready_for_backend_predictions"] = report["ready_for_inference"]
    CONFIG.reports_dir.mkdir(parents=True, exist_ok=True)
    write_json(CONFIG.reports_dir / "artifact_status.json", report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate ML service datasets, models, labels, and report artifacts.")
    parser.parse_args()
    report = validate_artifacts()
    print(read_json(CONFIG.reports_dir / "artifact_status.json"))
    if not report["ready_for_inference"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
