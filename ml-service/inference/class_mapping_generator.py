import argparse
from pathlib import Path

from utils.config import CONFIG
from utils.helpers import class_names_from_directory, write_json


def generate_class_mapping(dataset_dir: Path = CONFIG.train_dir) -> dict[str, str]:
    class_names = class_names_from_directory(dataset_dir)
    if not class_names:
        raise ValueError(f"No classes found in {dataset_dir}")
    mapping = {str(index): class_name for index, class_name in enumerate(class_names)}
    write_json(CONFIG.project_root / "inference" / "class_mapping.json", mapping)
    write_json(CONFIG.labels_path, class_names)
    return mapping


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate class mapping and labels from a dataset directory.")
    parser.add_argument("--dataset-dir", type=Path, default=CONFIG.train_dir)
    args = parser.parse_args()
    generate_class_mapping(args.dataset_dir)


if __name__ == "__main__":
    main()
