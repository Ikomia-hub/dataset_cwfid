import os
import yaml
import numpy as np


def load_cwfid_dataset(folder_path):
    data = {"images": [], "metadata": {}}
    data["metadata"]["category_colors"] = [(0, 0, 0), (0, 255, 0), (255, 0, 0)]
    data["metadata"]["category_names"] = {0: "background", 1: "crop", 2: "weed"}

    annotations = []
    labels = []
    images = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith("image.png"):
                images.append(os.path.join(root, file))

    for img in images:
        label = img.replace("images"+os.sep, "annotations"+os.sep)
        label = label.replace("image.png", "annotation.png")
        annot = label.replace(".png", ".yaml")
        labels.append(label)
        annotations.append(annot)

    id = 0
    for img, mask, annotation in zip(images, labels, annotations):
        id += 1
        record = {
            "image_id": id,
            "filename": img,
            "semantic_seg_masks_file": mask,
            "annotations": [],
            "height": 966,
            "width": 1296
        }

        with open(annotation) as file:
            annotation_data = yaml.load(file, Loader=yaml.FullLoader)
            for e in annotation_data["annotation"]:
                polygon_annot = {
                    "category_id": list(data["metadata"]["category_names"].values()).index(e["type"])
                }
                x = e["points"]["x"]
                y = e["points"]["y"]

                if type(x) == list:
                    points = np.zeros(2*len(x))
                    points[0::2] = x
                    points[1::2] = y
                    polygon_annot["segmentation_poly"] = [points]
                    record["annotations"].append(polygon_annot)

        data["images"].append(record)
    return data


