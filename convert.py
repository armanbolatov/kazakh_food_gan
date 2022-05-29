import json
import os
import shutil


def walk_folder(folder_name):

    file_id_to_file_name = {}
    file_id_to_cat_names = {}
    cat_id_to_cat_name = {}

    with open(f"./dataset/{folder_name}/_annotations.coco.json", 'r') as f:
        json_file = json.load(f)

        for image in json_file['images']:
            file_id_to_file_name[image['id']] = image['file_name']

        for cat in json_file['categories']:
            cat_id_to_cat_name[cat['id']] = cat['name']

        for file_id in file_id_to_file_name.keys():
            file_id_to_cat_names[file_id] = list()

        for annotation in json_file['annotations']:
            file_id = annotation['image_id']
            cat_name = cat_id_to_cat_name[annotation['category_id']]
            file_id_to_cat_names[file_id].append(cat_name)

    for file_id, cat_names in file_id_to_cat_names.items():
        num_of_cats = len(set(cat_names))
        if num_of_cats == 0:
            dir = f"dataset_sorted/empty"
        elif num_of_cats == 1:
            dir = f"dataset_sorted/{cat_names[0]}"
        else:
            dir = f"dataset_sorted/mixed"
        if not os.path.isdir(dir):
            os.makedirs(dir)
        file_name = file_id_to_file_name[file_id]
        src = f"./dataset/{folder_name}/{file_name}"
        shutil.copy(src, dir)


def main():
    folders = ['train', 'test', 'valid']
    for folder in folders:
        walk_folder(folder)


if __name__ == "__main__":
    main()
