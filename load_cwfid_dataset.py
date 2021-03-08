import os
import yaml
import numpy as np


def load_cwfid_dataset(folder_path):
    data = {"images": [], "metadata": {}}
    data["metadata"]["category_colors"]=[(0,0,0),(255,0,0),(0,0,255)]
    data["metadata"]["category_names"]={0:"soil",1:"weed",2:"crop"}

    annotations=[]
    annotation_masks=[]
    images=[]
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith("annotation.png"):
                annotation_masks.append(os.path.join(root, file))
            if file.endswith("annotation.yaml"):
                annotations.append(os.path.join(root, file))
            if file.endswith("image.png"):
                images.append(os.path.join(root, file))
    id=0
    for img,mask, annotation in zip(images,annotation_masks,annotations):
        id+=1
        record={}
        record["id"]=id
        record["filename"]=img
        record["semantic_seg_masks_file"]=mask
        record["annotations"]=[]
        record["height"]= 1296
        record["width"]=966
        with open(annotation) as file:
            annotation_data= yaml.load(file, Loader=yaml.FullLoader)

            for e in annotation_data["annotation"]:
                polygon_annot = {}
                polygon_annot["category_id"] = list(data["metadata"]["category_names"].values()).index(e["type"])
                x = e["points"]["x"]
                y = e["points"]["y"]
                points = np.stack([x,y]).T
                polygon_annot["segmentation_poly"]=[points]
                record["annotations"].append(polygon_annot)

        data["images"].append(record)
    return data


