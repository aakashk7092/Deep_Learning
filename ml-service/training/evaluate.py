import argparse
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import tensorflow as tf

from preprocessing.data_loader import load_image_dataset
from training.metrics import (
    calculate_metrics,
    save_classification_report,
    save_confusion_matrix,
    save_prediction_examples,
    save_roc_curves,
)
from utils.config import CONFIG
from utils.helpers import class_names_from_directory, read_json, write_json


def collect_predictions(model: tf.keras.Model, dataset: tf.data.Dataset) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    probabilities = model.predict(dataset, verbose=1)
    predicted = np.argmax(probabilities, axis=1)
    actual_batches = []
    for _, labels in dataset:
        actual_batches.append(np.argmax(labels.numpy(), axis=1))
    actual = np.concatenate(actual_batches)
    return actual, predicted, probabilities


def collect_example_images(dataset: tf.data.Dataset, max_examples: int = 12) -> np.ndarray:
    images = []
    for image_batch, _ in dataset:
        for image in image_batch.numpy():
            images.append(image)
            if len(images) >= max_examples:
                return np.asarray(images)
    return np.asarray(images)


def evaluate_model(
    model: tf.keras.Model,
    test_dataset: tf.data.Dataset,
    class_names: List[str],
    output_dir: Path = CONFIG.reports_dir,
) -> Dict[str, float]:
    y_true, y_pred, y_prob = collect_predictions(model, test_dataset)
    metrics = calculate_metrics(y_true, y_pred)
    example_images = collect_example_images(test_dataset)
    save_confusion_matrix(y_true, y_pred, class_names, output_dir)
    save_classification_report(y_true, y_pred, class_names, output_dir)
    save_roc_curves(y_true, y_prob, class_names, output_dir)
    save_prediction_examples(
        example_images,
        y_true[: len(example_images)],
        y_pred[: len(example_images)],
        np.max(y_prob[: len(example_images)], axis=1),
        class_names,
        output_dir,
    )
    write_json(output_dir / "evaluation_metrics.json", metrics)
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a saved plant disease model.")
    parser.add_argument("--model-path", type=Path, default=CONFIG.best_model_keras_path)
    parser.add_argument("--test-dir", type=Path, default=CONFIG.test_dir)
    args = parser.parse_args()

    if not args.model_path.exists():
        raise FileNotFoundError(f"Model not found: {args.model_path}")
    model = tf.keras.models.load_model(args.model_path)
    class_names = read_json(CONFIG.labels_path) if CONFIG.labels_path.exists() else class_names_from_directory(args.test_dir)
    test_dataset = load_image_dataset(args.test_dir, shuffle=False)
    evaluate_model(model, test_dataset, class_names, CONFIG.reports_dir)


if __name__ == "__main__":
    main()
