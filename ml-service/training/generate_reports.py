import argparse
from pathlib import Path

import tensorflow as tf

from preprocessing.data_loader import load_image_dataset
from training.evaluate import evaluate_model
from training.metrics import save_training_curves
from utils.config import CONFIG
from utils.helpers import class_names_from_directory, read_json


def generate_reports(model_path: Path = CONFIG.best_model_keras_path, test_dir: Path = CONFIG.test_dir) -> None:
    if not model_path.exists() or model_path.stat().st_size == 0:
        raise FileNotFoundError(f"Trained model not found or empty: {model_path}")
    model = tf.keras.models.load_model(model_path)
    class_names = read_json(CONFIG.labels_path) if CONFIG.labels_path.exists() and CONFIG.labels_path.stat().st_size else class_names_from_directory(test_dir)
    test_dataset = load_image_dataset(test_dir, shuffle=False)
    evaluate_model(model, test_dataset, class_names, CONFIG.reports_dir)
    if CONFIG.history_path.exists() and CONFIG.history_path.stat().st_size:
        save_training_curves(read_json(CONFIG.history_path), CONFIG.reports_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Regenerate evaluation reports from a trained model.")
    parser.add_argument("--model-path", type=Path, default=CONFIG.best_model_keras_path)
    parser.add_argument("--test-dir", type=Path, default=CONFIG.test_dir)
    args = parser.parse_args()
    generate_reports(args.model_path, args.test_dir)


if __name__ == "__main__":
    main()
