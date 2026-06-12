from pathlib import Path
from typing import List, Tuple

import tensorflow as tf

from preprocessing.preprocessing import preprocess_tensor
from utils.config import CONFIG


def load_image_dataset(
    directory: Path,
    batch_size: int = CONFIG.batch_size,
    image_size: Tuple[int, int] = CONFIG.image_size,
    shuffle: bool = True,
) -> tf.data.Dataset:
    if not directory.exists():
        raise FileNotFoundError(f"Dataset directory not found: {directory}")

    dataset = tf.keras.utils.image_dataset_from_directory(
        directory,
        labels="inferred",
        label_mode="categorical",
        color_mode=CONFIG.color_mode,
        image_size=image_size,
        batch_size=batch_size,
        shuffle=shuffle,
        seed=CONFIG.random_seed,
    )
    return dataset.map(preprocess_tensor, num_parallel_calls=tf.data.AUTOTUNE).prefetch(tf.data.AUTOTUNE)


def load_train_val_test() -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset, List[str]]:
    train_dataset_raw = tf.keras.utils.image_dataset_from_directory(
        CONFIG.train_dir,
        labels="inferred",
        label_mode="categorical",
        color_mode=CONFIG.color_mode,
        image_size=CONFIG.image_size,
        batch_size=CONFIG.batch_size,
        shuffle=True,
        seed=CONFIG.random_seed,
    )
    class_names = list(train_dataset_raw.class_names)
    train_dataset = train_dataset_raw.map(preprocess_tensor, num_parallel_calls=tf.data.AUTOTUNE).prefetch(tf.data.AUTOTUNE)
    val_dataset = load_image_dataset(CONFIG.val_dir, shuffle=False)
    test_dataset = load_image_dataset(CONFIG.test_dir, shuffle=False)
    return train_dataset, val_dataset, test_dataset, class_names
