import argparse
from pathlib import Path
from typing import Dict

import pandas as pd

from utils.config import CONFIG
from utils.helpers import list_image_files, write_json


def generate_dataset_statistics(dataset_dir: Path = CONFIG.processed_dataset_dir) -> Dict:
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

    stats = {"dataset_dir": str(dataset_dir), "splits": {}, "total_images": 0}
    rows = []
    for split_dir in sorted(path for path in dataset_dir.iterdir() if path.is_dir()):
        split_total = 0
        stats["splits"][split_dir.name] = {}
        for class_dir in sorted(path for path in split_dir.iterdir() if path.is_dir()):
            count = len(list_image_files(class_dir))
            stats["splits"][split_dir.name][class_dir.name] = count
            split_total += count
            rows.append({"split": split_dir.name, "class_name": class_dir.name, "image_count": count})
        stats["splits"][split_dir.name]["total"] = split_total
        stats["total_images"] += split_total

    CONFIG.reports_dir.mkdir(parents=True, exist_ok=True)
    write_json(CONFIG.reports_dir / "dataset_stats.json", stats)
    pd.DataFrame(rows).to_csv(CONFIG.reports_dir / "dataset_stats.csv", index=False)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate dataset statistics.")
    parser.add_argument("--dataset-dir", type=Path, default=CONFIG.processed_dataset_dir)
    args = parser.parse_args()
    generate_dataset_statistics(args.dataset_dir)


if __name__ == "__main__":
    main()
