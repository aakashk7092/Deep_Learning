from pathlib import Path
from typing import Tuple

import numpy as np
import tensorflow as tf
from PIL import Image

from utils.config import CONFIG


def preprocess_tensor(image: tf.Tensor, label: tf.Tensor | None = None):
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, CONFIG.image_size)
    if label is None:
        return image
    return image, label


def preprocess_image_file(image_path: str | Path, image_size: Tuple[int, int] = CONFIG.image_size) -> np.ndarray:
    with Image.open(image_path) as image:
        image = image.convert("RGB").resize(image_size)
        array = np.asarray(image, dtype=np.float32) / 255.0
    return np.expand_dims(array, axis=0)


def load_rgb_image(image_path: str | Path, image_size: Tuple[int, int] = CONFIG.image_size) -> Image.Image:
    with Image.open(image_path) as image:
        return image.convert("RGB").resize(image_size)
