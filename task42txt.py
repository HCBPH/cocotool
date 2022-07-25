import os
from re import I
from turtle import color
from unicodedata import category
from cv2 import line
import numpy as np
import cv2
import json


class Task4:
    def __init__(self, task_root, txt_path="./data/task4/convert.txt") -> None:
        self.root = task_root
        self.images_root = os.path.join(task_root, "images")
        self.labels_root = os.path.join(task_root, "labels")
        self.map = {
            "prohibitory":1,
            "warning":2,
            "mandatory":3
            }
        self.label_files = self.load_labels()
        self.txt_path = txt_path

    
    def toTxt(self):
        if len(self.label_files) == 0:
            raise Exception("there is no label files in "+self.labels_root)

        with open(self.txt_path, "w") as fw:
            print("\n")
            for i, label_file in enumerate(self.label_files):

                progress = (i+1)*100 // len(self.label_files)
                print("\rprogress:[{}{}]{}%".format(">"*progress, " "*(100 - progress), progress), end="")

                label_path = os.path.join(self.labels_root, label_file)
                line = []
                with open(label_path, "r") as f:
                    label = json.load(f)
                    
                    image_name = label["info"]["image_name"]
                    line.append(image_name)

                    size = cv2.imread(os.path.join(self.images_root, image_name)).shape[0:2]
                    line.extend(size)

                    annotations = label['annotation']
                    for ann in annotations:
                        category = ann['category']
                        cx, cy, w, h = [float(i) for i in ann['bbox']]
                        x, y = (cx - w/2, cy - h/2)
                        line.append(category)
                        line.extend([x, y, h, w])
                    
                    line = [str(i) for i in line]
                    line = ",".join(line)
                    line += "\n"
                    fw.write(line)

    
    def show(self, name):
        name = name.split(".")[0]
        label_name = name + ".json"
        image_name = name + ".jpg"
        with open(os.path.join(self.labels_root, label_name), "r") as f:
            label = json.load(f)

        annotations = label["annotation"]
        img = cv2.imread(os.path.join(self.images_root, image_name))
        # print(">>>", os.path.join(self.images_root, image_name))
        for ann in annotations:
            category = ann['category']
            cx, cy, w, h = [float(i) for i in ann['bbox']]
            x1,y1,x2,y2 = cx-w/2,cy-h/2,cx+w/2,cy+h/2
            cv2.rectangle(img, [int(x1),int(y1)], [int(x2),int(y2)], color=[0,0,255], thickness=2)
            cv2.putText(img, category, [int(x1)-10,int(y1)-5], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA, False)
        cv2.imshow(image_name, img)
        cv2.waitKey(0)



    def load_labels(self):
        label_files = os.listdir(self.labels_root)
        return label_files




if __name__ == '__main__':

    task4_root = r"E:\Data\dataset\task4"

    task4 = Task4(task4_root)

    task4.toTxt()
    # task4.show("4a0a1df8-ae55-11ec-8d5c-3800258c3060.jpg")

