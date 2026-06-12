import argparse
import shutil
from collections import defaultdict
from pathlib import Path

from sklearn.model_selection import train_test_split
from tqdm import tqdm

from utils.config import CONFIG
from utils.helpers import ensure_directories, list_image_files, set_global_seed
from utils.logger import get_logger


logger = get_logger(__name__)


def split_dataset(raw_dir: Path = CONFIG.raw_dataset_dir, output_dir: Path = CONFIG.processed_dataset_dir) -> None:
    if not raw_dir.exists():
        raise FileNotFoundError(f"Raw dataset directory not found: {raw_dir}")

    set_global_seed(CONFIG.random_seed)
    class_dirs = sorted(path for path in raw_dir.iterdir() if path.is_dir())
    if not class_dirs:
        raise ValueError(f"No class directories found in {raw_dir}")

    if output_dir.exists():
        shutil.rmtree(output_dir)

    split_dirs = [output_dir / "train", output_dir / "val", output_dir / "test"]
    ensure_directories(split_dirs)
    summary = defaultdict(dict)

    for class_dir in tqdm(class_dirs, desc="Splitting classes"):
        images = list_image_files(class_dir)
        if len(images) < 3:
            raise ValueError(f"Class '{class_dir.name}' must contain at least 3 images")

        train_files, temp_files = train_test_split(
            images,
            train_size=CONFIG.train_split,
            random_state=CONFIG.random_seed,
            shuffle=True,
        )
        val_ratio_adjusted = CONFIG.val_split / (CONFIG.val_split + CONFIG.test_split)
        val_files, test_files = train_test_split(
            temp_files,
            train_size=val_ratio_adjusted,
            random_state=CONFIG.random_seed,
            shuffle=True,
        )

        for split_name, files in {"train": train_files, "val": val_files, "test": test_files}.items():
            target_class_dir = output_dir / split_name / class_dir.name
            target_class_dir.mkdir(parents=True, exist_ok=True)
            for image_path in files:
                shutil.copy2(image_path, target_class_dir / image_path.name)
            summary[class_dir.name][split_name] = len(files)

    logger.info("Dataset split complete: %s", dict(summary))


def main() -> None:
    parser = argparse.ArgumentParser(description="Split PlantVillage dataset into train/val/test folders.")
    parser.add_argument("--raw-dir", type=Path, default=CONFIG.raw_dataset_dir)
    parser.add_argument("--output-dir", type=Path, default=CONFIG.processed_dataset_dir)
    args = parser.parse_args()
    split_dataset(args.raw_dir, args.output_dir)


if __name__ == "__main__":
    main()
