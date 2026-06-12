import argparse
import json
from pathlib import Path

from inference.predictor import PlantDiseasePredictor


def predict_image(image_path: str | Path, explain: bool = True) -> dict:
    return PlantDiseasePredictor().predict(image_path, explain=explain)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run production plant disease inference.")
    parser.add_argument("image_path", type=Path)
    parser.add_argument("--no-explain", action="store_true", help="Disable Grad-CAM generation")
    args = parser.parse_args()
    result = predict_image(args.image_path, explain=not args.no_explain)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
