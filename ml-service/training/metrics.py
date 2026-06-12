from pathlib import Path
from typing import Dict, Iterable, List

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support, roc_curve, auc
from sklearn.preprocessing import label_binarize

from utils.config import CONFIG


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted", zero_division=0)
    return {
        "accuracy": float(np.mean(y_true == y_pred)),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
    }


def save_training_curves(history: Dict[str, Iterable[float]], output_dir: Path = CONFIG.reports_dir) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.plot(history.get("accuracy", []), label="Train Accuracy")
    plt.plot(history.get("val_accuracy", []), label="Validation Accuracy")
    plt.title("Accuracy Curve")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "accuracy_curve.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(history.get("loss", []), label="Train Loss")
    plt.plot(history.get("val_loss", []), label="Validation Loss")
    plt.title("Loss Curve")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "loss_curve.png", dpi=160)
    plt.close()


def save_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, class_names: List[str], output_dir: Path = CONFIG.reports_dir) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    matrix = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(max(10, len(class_names) * 0.55), max(8, len(class_names) * 0.45)))
    sns.heatmap(matrix, annot=False, cmap="Blues", xticklabels=class_names, yticklabels=class_names)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_dir / "confusion_matrix.png", dpi=180)
    plt.close()


def save_classification_report(y_true: np.ndarray, y_pred: np.ndarray, class_names: List[str], output_dir: Path = CONFIG.reports_dir) -> str:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = classification_report(y_true, y_pred, target_names=class_names, zero_division=0)
    (output_dir / "classification_report.txt").write_text(report, encoding="utf-8")
    return report


def save_roc_curves(y_true: np.ndarray, y_prob: np.ndarray, class_names: List[str], output_dir: Path = CONFIG.reports_dir) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    if len(class_names) < 2:
        return

    y_true_bin = label_binarize(y_true, classes=np.arange(len(class_names)))
    plt.figure(figsize=(10, 8))
    for class_index, class_name in enumerate(class_names):
        if y_true_bin[:, class_index].sum() == 0:
            continue
        false_positive_rate, true_positive_rate, _ = roc_curve(y_true_bin[:, class_index], y_prob[:, class_index])
        roc_auc = auc(false_positive_rate, true_positive_rate)
        plt.plot(false_positive_rate, true_positive_rate, lw=1.5, label=f"{class_name} (AUC={roc_auc:.2f})")

    plt.plot([0, 1], [0, 1], "k--", lw=1)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curves")
    plt.legend(loc="lower right", fontsize="small")
    plt.tight_layout()
    plt.savefig(output_dir / "roc_curves.png", dpi=160)
    plt.close()


def save_prediction_examples(
    images: np.ndarray,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    class_names: List[str],
    output_dir: Path = CONFIG.reports_dir,
    max_examples: int = 12,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    count = min(max_examples, len(images))
    if count == 0:
        return

    cols = min(4, count)
    rows = int(np.ceil(count / cols))
    plt.figure(figsize=(cols * 4, rows * 4))
    for index in range(count):
        ax = plt.subplot(rows, cols, index + 1)
        ax.imshow(np.clip(images[index], 0, 1))
        true_label = class_names[int(y_true[index])]
        pred_label = class_names[int(y_pred[index])]
        ax.set_title(f"T: {true_label}\nP: {pred_label} ({confidences[index]:.2f})", fontsize=8)
        ax.axis("off")
    plt.tight_layout()
    plt.savefig(output_dir / "prediction_examples.png", dpi=160)
    plt.close()
