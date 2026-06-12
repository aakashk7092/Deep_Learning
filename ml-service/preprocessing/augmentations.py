import tensorflow as tf
from keras import layers


def build_augmentation_pipeline(seed: int = 42) -> tf.keras.Sequential:
    return tf.keras.Sequential(
        [
            layers.RandomFlip("horizontal_and_vertical", seed=seed),
            layers.RandomRotation(0.12, seed=seed),
            layers.RandomZoom(height_factor=0.15, width_factor=0.15, seed=seed),
            layers.RandomContrast(0.15, seed=seed),
            layers.RandomBrightness(0.12, seed=seed),
            layers.RandomTranslation(height_factor=0.08, width_factor=0.08, seed=seed),
        ],
        name="data_augmentation",
    )
