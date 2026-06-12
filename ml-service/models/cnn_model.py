import tensorflow as tf
from keras import layers, models

from preprocessing.augmentations import build_augmentation_pipeline
from utils.config import CONFIG


def build_custom_cnn(num_classes: int, input_shape=(224, 224, 3), use_augmentation: bool = True) -> tf.keras.Model:
    inputs = layers.Input(shape=input_shape, name="image_input")
    x = build_augmentation_pipeline(CONFIG.random_seed)(inputs) if use_augmentation else inputs

    for filters in (32, 64, 128, 256):
        x = layers.Conv2D(filters, 3, padding="same", activation="relu")(x)
        x = layers.BatchNormalization()(x)
        x = layers.Conv2D(filters, 3, padding="same", activation="relu")(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D()(x)
        x = layers.Dropout(0.2)(x)

    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(512, activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.4)(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="predictions")(x)
    return models.Model(inputs, outputs, name="CustomCNN")
