# ML Reports

This directory is populated by the training and evaluation pipeline.

Generated files:

- `accuracy_curve.png`
- `loss_curve.png`
- `confusion_matrix.png`
- `classification_report.txt`
- `roc_curves.png`
- `prediction_examples.png`
- `evaluation_metrics.json`
- `artifact_status.json`

Run from `ml-service`:

```powershell
python training/train.py --architecture efficientnetb0
python utils/artifact_validator.py
```
