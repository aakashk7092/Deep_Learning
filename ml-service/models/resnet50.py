import tensorflow as tf
from keras import layers, models

from preprocessing.augmentations import build_augmentation_pipeline
from utils.config import CONFIG


def build_resnet50(num_classes: int, input_shape=(224, 224, 3), train_backbone: bool = False) -> tf.keras.Model:
    inputs = layers.Input(shape=input_shape, name="image_input")
    x = build_augmentation_pipeline(CONFIG.random_seed)(inputs)
    x = tf.keras.applications.resnet50.preprocess_input(x * 255.0)
    backbone = tf.keras.applications.ResNet50(
        include_top=False,
        weights="imagenet",
        input_shape=input_shape,
    )
    backbone.trainable = train_backbone
    x = backbone(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.35)(x)
    x = layers.Dense(512, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="predictions")(x)
    return models.Model(inputs, outputs, name="ResNet50_PlantDisease")
