import os
import cv2

img_dir = r"E:\Data\dataset\CCTSDB\Images"
ann_url = r"E:\Data\dataset\CCTSDB\GroundTruth\GroundTruth.txt"
txt_url = "./data/cctsdb/convert.txt"

if not os.path.isdir(os.path.dirname(txt_url)):
    os.makedirs(os.path.dirname(txt_url))

with open(ann_url, "r") as f:
    with open(txt_url, "w") as fw:
        lines = f.readlines()

        img_name = ""

        # line 00000.png;527;377;555;404;warning
        for line in lines:
            items = line.strip().split(";")

            if img_name != items[0]:
                img_name = items[0]
                height, width = cv2.imread(os.path.join(img_dir, img_name)).shape[0:2]
                fw.write("\n")
                fw.write(f"{items[0]},{height},{width},")
            x1, y1, x2, y2 = [float(i) for i in items[1:5]]  
            # fw.write(f"{items[-1]},{x1},{y1},{x2-x1},{y2-y1},")
            fw.write(f"{items[-1]},{x1},{y1},{y2-y1},{x2-x1},")








# 检查标签和图片
# import cv2
# with open(ann_url, "r") as f:
#     lines = f.readlines()
#     for line in lines:
#         items = line.strip().split(';')
#         img_name = items[0]
#         x1, y1, x2, y2 = [int(i) for i in items[1:5]]
#         img = cv2.imread(os.path.join(img_dir, img_name))
#         cv2.rectangle(img, [x1, y1], [x2, y2], color=[0,0,255], thickness=2)
#         cv2.imshow("test", img)
#         cv2.waitKey(0)


