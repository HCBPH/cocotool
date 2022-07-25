import os
import cv2


img_path = "./data/swedish/set2-part0/"

ann_path = "E:\\Data\\dataset\\swedish\\annotations2.txt"

out_path = "./data/swedish/convert2.txt"

ann_count = 0
img_count = 0

with open(ann_path, "r") as f:
    with open(out_path, "w") as fw:


        while True:
            line = f.readline()
            if(line == ""):
                print("finish reading Swedish annotation")
                break

            t = []

            img, labels = line.split(":")
            t.append(img)

            # i = cv2.imread(img_path+img)
            # t.append(str(i.shape[0]))
            # t.append(str(i.shape[1]))
            t.append("960")
            t.append("1280")

            if ";" not in labels:
                print(f"{img} doesn't contain traffic sign!")
                fw.write(",".join(t)+"\n")
                continue
            
            labels = labels.split(";")
            for label in labels:
                if(label == "\n" or label == "MISC_SIGNS" or label == " \n"):
                    continue
                try:
                    is_visible, x2, y2, x1, y1, category = label.split(", ")[:6]
                except:
                    print(">>>>>", img, label)
                height = str(float(y2) - float(y1))
                width = str(float(x2) - float(x1))
                if category == "OTHER" or category == "INFORMATION" or category == "UNREADABLE":
                    continue
                t.append(category)
                t.append(x1)
                t.append(y1)
                t.append(height)
                t.append(width)
            fw.write(",".join(t)+"\n")