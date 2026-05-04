#!/usr/bin/env python3
import argparse
import json
import random
from pathlib import Path

IMG_SUFFIX = "-color.jpg"


def read_class_name(folder: Path) -> str:
    f = folder / "name.txt"
    if f.exists():
        txt = f.read_text(encoding="utf-8").strip()
        if txt:
            return txt
    return folder.name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=str, required=True, help='Path to "objects" folder')

    # Percentage split
    ap.add_argument("--train_ratio", type=float, default=0.70)
    ap.add_argument("--val_ratio", type=float, default=0.15)
    ap.add_argument("--test_ratio", type=float, default=0.15)

    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", type=str, default="split.json")
    args = ap.parse_args()

    root = Path(args.root)
    rng = random.Random(args.seed)

    # Check ratio
    total_ratio = args.train_ratio + args.val_ratio + args.test_ratio
    if abs(total_ratio - 1.0) > 1e-6:
        raise RuntimeError(
            f"Ratios must add up to 1.0, but got {total_ratio}"
        )

    folders = sorted([p for p in root.iterdir() if p.is_dir()], key=lambda p: p.name)
    if not folders:
        raise RuntimeError(f"No subfolders found under {root}")

    label_map = {}
    splits = {"train": [], "val": [], "test": []}

    class_id = 0

    for folder in folders:
        imgs = sorted([p for p in folder.glob(f"*{IMG_SUFFIX}") if p.is_file()])

        if not imgs:
            continue

        name = read_class_name(folder)
        label_map[str(class_id)] = name

        imgs_rel = [str(p.relative_to(root)) for p in imgs]
        rng.shuffle(imgs_rel)

        n = len(imgs_rel)

        train_count = int(n * args.train_ratio)
        val_count = int(n * args.val_ratio)

        # Put the remaining images into test
        test_count = n - train_count - val_count

        train = imgs_rel[:train_count]
        val = imgs_rel[train_count: train_count + val_count]
        test = imgs_rel[train_count + val_count:]

        for r in train:
            splits["train"].append({"path": r, "y": class_id})
        for r in val:
            splits["val"].append({"path": r, "y": class_id})
        for r in test:
            splits["test"].append({"path": r, "y": class_id})

        print(
            f"{class_id}: {name} | total={n}, "
            f"train={len(train)}, val={len(val)}, test={len(test)}"
        )

        class_id += 1

    out = {
        "root": str(root),
        "seed": args.seed,
        "train_ratio": args.train_ratio,
        "val_ratio": args.val_ratio,
        "test_ratio": args.test_ratio,
        "num_classes": class_id,
        "label_map": label_map,
        "splits": splits,
    }

    out_path = Path(args.out)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print("\nWrote:", out_path.resolve())
    print(f"Classes: {class_id}")
    print(f"Train/Val/Test: {len(splits['train'])}/{len(splits['val'])}/{len(splits['test'])}")


if __name__ == "__main__":
    main()