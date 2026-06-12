from pathlib import Path
from typing import Dict, List

from utils.config import CONFIG
from utils.helpers import read_json, write_json


class LabelEncoder:
    def __init__(self, labels: List[str]) -> None:
        if not labels:
            raise ValueError("Labels cannot be empty")
        self.labels = labels
        self.label_to_index = {label: index for index, label in enumerate(labels)}
        self.index_to_label = {index: label for index, label in enumerate(labels)}

    def encode(self, label: str) -> int:
        if label not in self.label_to_index:
            raise KeyError(f"Unknown label: {label}")
        return self.label_to_index[label]

    def decode(self, index: int) -> str:
        if index not in self.index_to_label:
            raise KeyError(f"Unknown label index: {index}")
        return self.index_to_label[index]

    def to_mapping(self) -> Dict[str, str]:
        return {str(index): label for index, label in self.index_to_label.items()}

    def save(self, path: Path = CONFIG.labels_path) -> None:
        write_json(path, self.labels)

    @classmethod
    def load(cls, path: Path = CONFIG.labels_path) -> "LabelEncoder":
        labels = read_json(path)
        if isinstance(labels, dict):
            labels = [labels[str(index)] for index in range(len(labels))]
        return cls(labels)
