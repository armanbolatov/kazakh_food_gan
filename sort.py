import yaml
import os
import shutil


src_yaml = "dataset/data.yaml"
with open(src_yaml, "r") as stream:
    try:
        yaml_file = yaml.safe_load(stream)
        cat_id_to_name = yaml_file['names']
    except yaml.YAMLError as exc:
        print(exc)
shutil.copy(src_yaml, "dataset_sorted")


def walk_folder(folder_name):

    image_to_label = {}
    images_path = f"./dataset/{folder_name}/images/"
    labels_path = f"./dataset/{folder_name}/labels/"

    for annotation in os.listdir(labels_path):
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
        if not os.path.isdir(dir):
            os.makedirs(dir + "images/")
            os.makedirs(dir + "labels/")
        src_image = images_path + f"{file_name}.jpg"
        shutil.copy(src_image, dir + "images")
        src_label = labels_path + f"{file_name}.txt"
        shutil.copy(src_label, dir + "labels")


folders = ['train', 'test', 'valid']
for folder in folders:
    walk_folder(folder)
