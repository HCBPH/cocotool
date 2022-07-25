

import json

avd_url = r"data\adv\instances_train2017.json"

with open(avd_url, "r") as f:
    ann = json.load(f)
    images = ann['images']
    # annotations = ann['annotations']
    for i in range(5000):
        image = images[i]
        image_name = image['file_name']
        height = image['height']
        width = image['width']
        image_id = image['id']

        # 然后根据image_name去找对应的avd图片，然后对比hw
        for j in range(i, len(images)):
            img = images[j]
            if image_name in img['file_name']:
                if height != img['height'] or width != img['width']:
                    print(f"find image:{image_name}({image_id})")
