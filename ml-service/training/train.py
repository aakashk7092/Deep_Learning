import argparse
from pathlib import Path

import tensorflow as tf

from models.cnn_model import build_custom_cnn
from models.efficientnetb0 import build_efficientnetb0
from models.mobilenetv2 import build_mobilenetv2
from models.resnet50 import build_resnet50
from preprocessing.data_loader import load_train_val_test
from training.callbacks import build_callbacks
from training.evaluate import evaluate_model
from training.metrics import save_training_curves
from utils.config import CONFIG
from utils.helpers import ensure_directories, set_global_seed, utc_now_iso, write_json
from utils.logger import get_logger


logger = get_logger(__name__, CONFIG.logs_dir / "training.log")


MODEL_BUILDERS = {
    "cnn": build_custom_cnn,
    "mobilenetv2": build_mobilenetv2,
    "resnet50": build_resnet50,
    "efficientnetb0": build_efficientnetb0,
}


def compile_model(model: tf.keras.Model) -> tf.keras.Model:
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=CONFIG.initial_learning_rate),
        loss=tf.keras.losses.CategoricalCrossentropy(),
        metrics=[
            "accuracy",
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall"),
            tf.keras.metrics.AUC(name="auc"),
        ],
    )
    return model


def train_model(architecture: str = "efficientnetb0", epochs: int = CONFIG.epochs) -> tf.keras.Model:
    if architecture not in MODEL_BUILDERS:
        raise ValueError(f"Unsupported architecture '{architecture}'. Choose from {sorted(MODEL_BUILDERS)}")

    set_global_seed(CONFIG.random_seed)
    ensure_directories([CONFIG.saved_models_dir, CONFIG.reports_dir, CONFIG.logs_dir])
    train_dataset, val_dataset, test_dataset, class_names = load_train_val_test()
    write_json(CONFIG.labels_path, class_names)
    write_json(CONFIG.project_root / "inference" / "class_mapping.json", {str(index): label for index, label in enumerate(class_names)})

    model = compile_model(MODEL_BUILDERS[architecture](num_classes=len(class_names)))
    with CONFIG.summary_path.open("w", encoding="utf-8") as summary_file:
        model.summary(print_fn=lambda line: summary_file.write(line + "\n"))

    logger.info("Starting %s training for %s classes", architecture, len(class_names))
    history = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=epochs,
        callbacks=build_callbacks(),
    )

    history_dict = {key: [float(value) for value in values] for key, values in history.history.items()}
    write_json(CONFIG.history_path, history_dict)
    save_training_curves(history_dict, CONFIG.reports_dir)

    best_model = tf.keras.models.load_model(CONFIG.best_model_keras_path)
    best_model.save(CONFIG.best_model_h5_path)
    evaluation = evaluate_model(best_model, test_dataset, class_names, CONFIG.reports_dir)

    metadata = {
        "version": CONFIG.model_version,
        "created_at": utc_now_iso(),
        "accuracy": evaluation["accuracy"],
        "architecture": architecture,
        "image_size": list(CONFIG.image_size),
        "num_classes": len(class_names),
        "classes": class_names,
    }
    write_json(CONFIG.metadata_path, metadata)
    logger.info("Training complete. Metadata saved to %s", CONFIG.metadata_path)
    return best_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train plant disease detection model.")
    parser.add_argument("--architecture", choices=sorted(MODEL_BUILDERS), default="efficientnetb0")
    parser.add_argument("--epochs", type=int, default=CONFIG.epochs)
    args = parser.parse_args()
    train_model(args.architecture, args.epochs)


if __name__ == "__main__":
    main()
