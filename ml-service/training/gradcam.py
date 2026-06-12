from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
import tensorflow as tf

from preprocessing.preprocessing import load_rgb_image, preprocess_image_file
from utils.config import CONFIG


def _is_spatial_layer(layer: tf.keras.layers.Layer) -> bool:
    output_shape = getattr(layer, "output_shape", None)
    return (output_shape is not None and len(output_shape) == 4) or "conv" in layer.name.lower()


def find_last_conv_layer(model: tf.keras.Model) -> Tuple[tf.keras.Model, str]:
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.Model):
            try:
                return find_last_conv_layer(layer)
            except ValueError:
                continue
        if _is_spatial_layer(layer):
            return model, layer.name
    raise ValueError("No convolutional layer found for Grad-CAM")


def make_gradcam_heatmap(
    image_array: np.ndarray,
    model: tf.keras.Model,
    last_conv_layer_name: str | None = None,
    pred_index: int | None = None,
) -> np.ndarray:
    target_model, layer_name = (model, last_conv_layer_name) if last_conv_layer_name else find_last_conv_layer(model)
    if target_model is model:
        conv_output = model.get_layer(layer_name).output
        grad_model = tf.keras.models.Model([model.inputs], [conv_output, model.output])
    else:
        image_input = model.inputs[0]
        x = image_input
        conv_output = None
        for layer in model.layers[1:]:
            if layer is target_model:
                nested_layer_output_model = tf.keras.models.Model(layer.input, layer.get_layer(layer_name).output)
                conv_output = nested_layer_output_model(x)
                x = layer(x)
            else:
                x = layer(x)
        if conv_output is None:
            raise ValueError(f"Layer {layer_name} was not reachable from the model input")
        grad_model = tf.keras.models.Model([image_input], [conv_output, x])

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(image_array)
        if pred_index is None:
            pred_index = int(tf.argmax(predictions[0]))
        class_channel = predictions[:, pred_index]

    gradients = tape.gradient(class_channel, conv_outputs)
    pooled_gradients = tf.reduce_mean(gradients, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_gradients[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + tf.keras.backend.epsilon())
    return heatmap.numpy()


def save_gradcam_overlay(
    image_path: str | Path,
    model: tf.keras.Model,
    output_path: str | Path,
    alpha: float = 0.42,
) -> Tuple[Path, np.ndarray]:
    output_path = Path(output_path)
    image_array = preprocess_image_file(image_path)
    heatmap = make_gradcam_heatmap(image_array, model)
    image = np.array(load_rgb_image(image_path, CONFIG.image_size))
    heatmap_resized = cv2.resize(heatmap, CONFIG.image_size)
    heatmap_uint8 = np.uint8(255 * heatmap_resized)
    color_map = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(cv2.cvtColor(image, cv2.COLOR_RGB2BGR), 1 - alpha, color_map, alpha, 0)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), overlay)
    return output_path, heatmap
