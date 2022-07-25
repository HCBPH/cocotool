import os
import json
import cv2
import copy


def transferAnn(image_id, annotations, new_ann):
    for annotation in annotations:
        if annotation['image_id'] == image_id:
            new_ann.append(annotation)



adv_img_dir = "E:/Download/aliyunpan/advdata/"
clean_ann_path = r"E:\Data\dataset\TrafficSign\annotations\instances_train2017.json"
adv_ann_path = "./data/adv/instances_train2017.json"

if not os.path.isdir(os.path.dirname(adv_ann_path)):
    os.mkdir(os.path.dirname(adv_ann_path))

with open(clean_ann_path, "r") as f:
    ann = json.load(f)
    images = ann['images']
    annotations = ann['annotations']
    image_id = images[-1]['id']
    annotation_id = annotations[-1]['id']
    img_count = image_id
    ann_count = annotation_id

    file_list = os.listdir(adv_img_dir)
    print(f"准备插入{len(file_list)}张图片")
    for file_name in file_list:
        print(">>> processing "+file_name)
        id_, file_type = file_name[:8], file_name[-4:]
        tofind = "".join([id_, file_type])
        
        for i in range(len(images)):
            if tofind == images[i]["file_name"]:
                image_id += 1
                t_image = copy.copy(images[i])
                t_image['id'] = image_id
                t_image['file_name'] = file_name
                images.append(t_image)

                for ann_idx in range(len(annotations)):
                    if(annotations[ann_idx]['image_id'] == images[i]['id']):
                        t_annotation = copy.copy(annotations[ann_idx])
                        annotation_id += 1
                        t_annotation['id'] = annotation_id
                        t_annotation['image_id'] = image_id
                        annotations.append(t_annotation)
    print(f">>> 总共插入{image_id-img_count}张图片，{annotation_id-ann_count}个标签。")
        
    with open(adv_ann_path, "w") as fw:
        json.dump(ann, fw)


        


