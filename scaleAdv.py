import json


def remake_bbox(ori_bbox, ori_shape, adv_shape=(800, 1332)):
    rate_w, rate_h = adv_shape[0] / ori_shape[0], adv_shape[1] / ori_shape[1]
    [x1, x2, x3, x4] = ori_bbox
    return [x1*rate_h, x2*rate_w, x3*rate_h, x4*rate_w]


avd_url = r"data\adv\instances_train2017.json"
adv_shape=(800, 1332)
new_url = r"data\adv\instances_train2017_new.json"
ann = None
flag = False
with open(avd_url, "r") as f:
    ann = json.load(f)
    images = ann['images']
    annotations = ann['annotations']
    # for i in len(images):
    #     # image = images[i]
    #     # image_name = image['file_name']
    #     # image_id = image['id']
    #     images[i]['height'] = adv_shape[0]
    #     images[i]['width'] = adv_shape[1]
        

    # 然后遍历annotations，获取bbox，方法如remake_bbox函数，根据新值替换原来的
    for j in range(len(annotations)):
        annotation = annotations[j]
        image_id = annotation['image_id']

        if annotation['id'] == 5111:
            flag = True

        if flag:
            for i in range(len(images)):
                image = images[i]
                # image_name = image['file_name']
                if image_id == image['id']:
                    height = image['height']
                    width = image['width']
                    image['height'] = adv_shape[0]
                    image['width'] = adv_shape[1]
                    bbox = remake_bbox(annotation['bbox'], (height, width))
                    annotation['bbox'] = bbox
                    break

with open(new_url, "w") as f:
    json.dump(ann, f)
        
        


