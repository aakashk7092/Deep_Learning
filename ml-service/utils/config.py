from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class MLConfig:
    project_root: Path = Path(__file__).resolve().parents[1]
    image_size: Tuple[int, int] = (224, 224)
    color_mode: str = "rgb"
    batch_size: int = 32
    epochs: int = 50
    initial_learning_rate: float = 0.001
    train_split: float = 0.70
    val_split: float = 0.15
    test_split: float = 0.15
    random_seed: int = 42
    model_version: str = "1.0.0"
    production_architecture: str = "EfficientNetB0"

    @property
    def raw_dataset_dir(self) -> Path:
        return self.project_root / "datasets" / "raw"

    @property
    def processed_dataset_dir(self) -> Path:
        return self.project_root / "datasets" / "processed"

    @property
    def train_dir(self) -> Path:
        return self.processed_dataset_dir / "train"

    @property
    def val_dir(self) -> Path:
        return self.processed_dataset_dir / "val"

    @property
    def test_dir(self) -> Path:
        return self.processed_dataset_dir / "test"

    @property
    def saved_models_dir(self) -> Path:
        return self.project_root / "saved_models"

    @property
    def reports_dir(self) -> Path:
        return self.project_root / "reports"

    @property
    def logs_dir(self) -> Path:
        return self.project_root / "logs"

    @property
    def best_model_keras_path(self) -> Path:
        return self.saved_models_dir / "best_model.keras"

    @property
    def best_model_h5_path(self) -> Path:
        return self.saved_models_dir / "best_model.h5"

    @property
    def labels_path(self) -> Path:
        return self.saved_models_dir / "labels.json"

    @property
    def metadata_path(self) -> Path:
        return self.saved_models_dir / "model_metadata.json"

    @property
    def history_path(self) -> Path:
        return self.saved_models_dir / "history.json"

    @property
    def summary_path(self) -> Path:
        return self.saved_models_dir / "model_summary.txt"


CONFIG = MLConfig()
