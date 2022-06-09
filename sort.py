import yaml
import os
import shutil
from tqdm import tqdm


def walk_folder(folder_name, cat_id_to_name):

    image_to_label = {}
    images_path = f"./dataset/{folder_name}/images/"
    labels_path = f"./dataset/{folder_name}/labels/"
    print(f"Started sorting folder {folder_name}:")

    for annotation in tqdm(os.listdir(labels_path)):
        with open(labels_path + annotation, 'r') as f:
            file_name = os.path.splitext(annotation)[0]
            image_to_label[file_name] = []
            for label in f:
                cat_id, *bbox = map(float, label.split())
                label = cat_id_to_name[int(cat_id)]
                image_to_label[file_name].append((label, bbox))
        image_cats = [label[0] for label in image_to_label[file_name]]
        num_cats = len(set(image_cats))
        if num_cats == 0:
            dir = f"dataset_sorted/empty/"
        elif num_cats == 1:
            dir = f"dataset_sorted/{image_cats[0]}/"
        else:
            dir = f"dataset_sorted/mixed/"
 
        src_image = images_path + f"{file_name}.jpg"
        dst_image = dir + "images"
        os.makedirs(os.path.dirname(dst_image), exist_ok=True)
        shutil.copy(src_image, dst_image)

        src_label = labels_path + f"{file_name}.txt"
        dst_label = dir + "labels"
        os.makedirs(os.path.dirname(dst_label), exist_ok=True)
        shutil.copy(src_label, dst_label)


def main():
    
    dir = "dataset_sorted/"
    if not os.path.exists(dir):
        os.makedirs(dir)

    src_yaml = "dataset/data.yaml"
    with open(src_yaml, "r") as stream:
        try:
            yaml_file = yaml.safe_load(stream)
            cat_id_to_name = yaml_file['names']
        except yaml.YAMLError as exc:
            print(exc)
    shutil.copy(src_yaml, dir + "data.yaml")

    folders = ("train", "test", "valid")
    for folder in folders:
        walk_folder(folder, cat_id_to_name)
    
    print("\nCategory statistics:\n")
    total = 0
    for cat in os.listdir(dir):
        if os.path.isdir(dir + cat):
            _, _, files = next(os.walk(dir + cat + "/images"))
            total += len(files)
            print(f"{len(files)}\tfiles of category\t{cat}")
    print(f"\nTotal {total} files.")


if __name__ == "__main__":
    main()