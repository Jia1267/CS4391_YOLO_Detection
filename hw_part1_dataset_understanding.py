#!/usr/bin/env python3
"""
HW Part 1 — Dataset Understanding

Dataset structure:

real_objects/
    object_folder_000/
        000000-color.jpg
        ...
        000008-color.jpg
        name.txt
    object_folder_001/
        ...

Each folder = one class.
name.txt contains the class name.

------------------------------------------------------
Your tasks:

1) Print:
   - number of classes
   - total number of images
   - number of images per class (min / max / mean)

2) Create a mapping:
   class_id -> class_name

3) Visualize:
   - 5 random training images
   - show image + class name as title
------------------------------------------------------
"""

import argparse
import random
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


IMG_SUFFIX = "-color.jpg"


# --------------------------------------------------
# TODO 1: Index the dataset
# --------------------------------------------------
def index_dataset(root: Path):
    """
    Return:
        classes: list of dicts with keys:
            {
                "id": int,
                "name": str,
                "images": list[Path]
            }
    """

    classes = []

    # Only keep folders, so class_id will not skip numbers
    folders = [f for f in sorted(root.iterdir()) if f.is_dir()]

    for class_id, folder in enumerate(folders):
        # Read class name from name.txt
        name_file = folder / "name.txt"

        if name_file.exists():
            class_name = name_file.read_text(encoding="utf-8").strip()
        else:
            class_name = folder.name

        # Collect all color images
        images = sorted(folder.glob(f"*{IMG_SUFFIX}"))

        classes.append({
            "id": class_id,
            "name": class_name,
            "images": images
        })

    return classes


# --------------------------------------------------
# TODO 2: Print dataset statistics
# --------------------------------------------------
def print_dataset_stats(classes):
    """
    Print:
        - number of classes
        - total images
        - min / max / mean images per class
    """

    num_classes = len(classes)

    counts = [len(c["images"]) for c in classes]
    total_images = int(np.sum(counts)) if counts else 0

    min_imgs = int(np.min(counts)) if counts else 0
    max_imgs = int(np.max(counts)) if counts else 0
    mean_imgs = float(np.mean(counts)) if counts else 0.0

    print("========== Dataset Statistics ==========")
    print(f"Number of classes: {num_classes}")
    print(f"Total number of images: {total_images}")
    print(f"Images per class: min={min_imgs}, max={max_imgs}, mean={mean_imgs:.2f}")


# --------------------------------------------------
# TODO 3: Print class mapping
# --------------------------------------------------
def print_class_mapping(classes):
    """
    Print:
        class_id -> class_name
    """

    print("\n========== Class Mapping ==========")

    for c in classes:
        print(f'{c["id"]}: {c["name"]}')


# --------------------------------------------------
# Extra: Print images per class
# --------------------------------------------------
def print_images_per_class(classes):
    """
    Print:
        class_id, class_name, number of images
    """

    print("\n========== Images Per Class ==========")

    for c in classes:
        print(f'{c["id"]}: {c["name"]} | images: {len(c["images"])}')


# --------------------------------------------------
# TODO 4: Visualize random samples
# --------------------------------------------------
def visualize_random_samples(classes, num_samples=5):
    """
    Randomly select num_samples images from the dataset
    and display them with class name as title.
    """

    all_images = []

    for c in classes:
        for img_path in c["images"]:
            all_images.append((img_path, c["name"]))

    if len(all_images) == 0:
        print("No images found. Cannot visualize samples.")
        return

    # Avoid error if dataset has fewer than 5 images
    num_samples = min(num_samples, len(all_images))

    samples = random.sample(all_images, num_samples)

    plt.figure(figsize=(15, 3))

    for i, (img_path, class_name) in enumerate(samples):
        img = Image.open(img_path)

        plt.subplot(1, num_samples, i + 1)
        plt.imshow(img)
        plt.title(class_name)
        plt.axis("off")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=str,
        required=True,
        help='Path to "real_objects" folder'
    )

    args = parser.parse_args()

    root = Path(args.root)

    if not root.exists():
        raise RuntimeError(f"Root folder does not exist: {root}")

    if not root.is_dir():
        raise RuntimeError(f"Root path is not a folder: {root}")

    # 1. Index dataset
    classes = index_dataset(root)

    # 2. Print statistics
    print_dataset_stats(classes)

    # 3. Print class_id -> class_name
    print_class_mapping(classes)

    # 4. Print number of images for every class
    print_images_per_class(classes)

    # 5. Visualize 5 random samples
    visualize_random_samples(classes, num_samples=5)


if __name__ == "__main__":
    main()