import os
import numpy as np
import shutil
from itertools import accumulate
from tqdm import tqdm

src = "dataset_augmented/"
dst = "dataset_splitted/"
folder_names = ("train", "test", "valid")
split_ratio = (0.7, 0.2, )

all_cats_files = []
for cat in os.listdir(src):
    if os.path.isdir(src + cat):
        for annotation in os.listdir(src + cat + "/labels"):
            file_name = os.path.splitext(annotation)[0]
            all_cats_files.append((cat, file_name))

np.random.shuffle(all_cats_files)

indices = [int(len(all_cats_files) * e) for e in accumulate(split_ratio)]

splitted = np.split(ary=np.array(all_cats_files), indices_or_sections=indices)

print(f"The dataset is successfully splitted into {', '.join(folder_names)} folders.")

src_yaml = src + "data.yaml"
dst_yaml = dst + "data.yaml"
os.makedirs(os.path.dirname(dst_yaml), exist_ok=True)
shutil.copy(src_yaml, dst_yaml)

for folder, cats_files in zip(folder_names, splitted):
    print(f"\nCopying into {folder} folder.")
    for cat, file_name in tqdm(cats_files):

        src_image = src + f"{cat}/images/{file_name}.jpg"
        dst_image = dst + f"{folder}/images/{file_name}.jpg"
        os.makedirs(os.path.dirname(dst_image), exist_ok=True)
        shutil.copy(src_image, dst_image)

        src_label = src + f"{cat}/labels/{file_name}.txt"
        dst_label = dst + f"{folder}/labels/{file_name}.txt"
        os.makedirs(os.path.dirname(dst_label), exist_ok=True)
        shutil.copy(src_label, dst_label)
