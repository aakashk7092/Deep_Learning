from datetime import datetime

import tensorflow as tf

from utils.config import CONFIG


def build_callbacks() -> list[tf.keras.callbacks.Callback]:
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_dir = CONFIG.logs_dir / run_id
    CONFIG.saved_models_dir.mkdir(parents=True, exist_ok=True)
    tensorboard_dir.mkdir(parents=True, exist_ok=True)

    return [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=8,
            restore_best_weights=True,
            verbose=1,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=3,
            min_lr=1e-7,
            verbose=1,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(CONFIG.best_model_keras_path),
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=1,
        ),
        tf.keras.callbacks.TensorBoard(
            log_dir=str(tensorboard_dir),
            histogram_freq=1,
            write_graph=True,
            update_freq="epoch",
        ),
    ]
