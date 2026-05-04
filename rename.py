from pathlib import Path

folder = Path(r"F:\F\School\3\CS4391\Pro\real_objects\0502T161549Ph")

image_extensions = [".jpg"]

images = [
    f for f in folder.iterdir()
    if f.is_file() and f.suffix.lower() in image_extensions
]

images = sorted(images)

temp_files = []

for i, img in enumerate(images):
    temp_name = folder / f"temp_rename_{i:06d}{img.suffix.lower()}"
    img.rename(temp_name)
    temp_files.append(temp_name)

for i, img in enumerate(temp_files):
    new_name = folder / f"{i:06d}-color.jpg"
    img.rename(new_name)

print(f"Done. Renamed {len(images)} images.")