import tensorflow as tf
from keras import layers, models

from preprocessing.augmentations import build_augmentation_pipeline
from utils.config import CONFIG


def build_efficientnetb0(num_classes: int, input_shape=(224, 224, 3), train_backbone: bool = False) -> tf.keras.Model:
    inputs = layers.Input(shape=input_shape, name="image_input")
    x = build_augmentation_pipeline(CONFIG.random_seed)(inputs)
    backbone = tf.keras.applications.EfficientNetB0(
        include_top=False,
        weights="imagenet",
        input_shape=input_shape,
        include_preprocessing=False,
    )
    backbone.trainable = train_backbone
    x = backbone(x, training=False)
    x = layers.GlobalAveragePooling2D(name="global_average_pooling")(x)
    x = layers.BatchNormalization(name="classification_batch_norm")(x)
    x = layers.Dropout(0.3, name="classification_dropout_1")(x)
    x = layers.Dense(512, activation="relu", name="classification_dense")(x)
    x = layers.Dropout(0.3, name="classification_dropout_2")(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="predictions")(x)
    return models.Model(inputs, outputs, name="EfficientNetB0_PlantDisease")


def unfreeze_top_layers(model: tf.keras.Model, trainable_layers: int = 30) -> tf.keras.Model:
    backbone = next((layer for layer in model.layers if isinstance(layer, tf.keras.Model) and "efficientnet" in layer.name.lower()), None)
    if backbone is None:
        return model
    backbone.trainable = True
    for layer in backbone.layers[:-trainable_layers]:
        layer.trainable = False
    return model
