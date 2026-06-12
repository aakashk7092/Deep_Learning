# preprocess_uploads.py
import os
from PIL import Image
import numpy as np

# Paths
original_dir = "uploads/original"
processed_dir = "uploads/processed"

# Create processed directory if it doesn't exist
os.makedirs(processed_dir, exist_ok=True)

# Loop through all images in original
for filename in os.listdir(original_dir):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        orig_path = os.path.join(original_dir, filename)
        # Load image
        img = Image.open(orig_path).convert("RGB")
        # Resize
        img = img.resize((224, 224))
        # Normalize
        img_array = np.array(img) / 255.0
        # Convert back to image for saving
        img_normalized = Image.fromarray((img_array * 255).astype(np.uint8))
        # Save
        save_path = os.path.join(processed_dir, os.path.splitext(filename)[0] + ".png")
        img_normalized.save(save_path)
        print(f"Processed: {filename} -> {save_path}")

print("All images processed successfully!")