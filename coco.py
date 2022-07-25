from logging import root
import os
import time
from tkinter import E
from shapely.geometry import Polygon
import json
import shutil
import numpy as np


class COCO:
    def __init__(self,
            coco_path, src_imgs, 
            old_ann_path,
            categories,
            appending=False, logging=True,
            coco_type=2017, src_type = None
        ) -> None:

        coco_path = checkPath(coco_path)
        src_imgs = checkPath(src_imgs)

        if not os.path.exists(coco_path):
            os.makedirs(coco_path)
        self.coco_path = coco_path

        if os.path.exists(src_imgs):
            self.src_imgs = src_imgs
        else:
            raise FileNotFoundError(src_imgs)
        
        self.appending = appending
        self.logging = logging
        self.coco_type = str(coco_type)

        dic = dict()
        if self.appending:
            if not os.path.isdir(old_ann_path):
                raise Exception("old_ann_path must already exist!")
            ann_dir = os.listdir(old_ann_path)
            if len(ann_dir) >3 or len(ann_dir) == 0:
                raise Exception("error parsing old_ann_path!")
            for f in ann_dir:
                if ".json" in f:
                    if "train" in f:
                        dic['train'] = f
                    elif "val" in f:
                        dic['val'] = f
                    elif "test" in f:
                        dic['test'] = f
                    else:
                        self.print("detect invalid annotation file!")

        ann_train_url = self.coco_path + "annotations/instances_train"+str(coco_type)+".json"
        ann_val_url = self.coco_path + "annotations/instances_val"+str(coco_type)+".json"
        ann_test_url = self.coco_path + "annotations/instances_test"+str(coco_type)+".json"
        self.annotation_train = Annotation(name="train"+self.coco_type, ann_url=ann_train_url, old_ann_url=checkPath(old_ann_path)+dic.get("train", "."), categories=categories, appending=appending)
        self.annotation_val = Annotation(name = "val"+self.coco_type, ann_url=ann_val_url, old_ann_url=checkPath(old_ann_path)+dic.get("val", "."), categories=categories, appending=appending)
        self.annotation_test = Annotation(name="test"+self.coco_type, ann_url=ann_test_url, old_ann_url=checkPath(old_ann_path)+dic.get("test", "."), categories=categories, appending=appending)

        train_path = self.coco_path + "images/train" + str(coco_type) + "/"
        val_path = self.coco_path + "images/val" + str(coco_type) + "/"
        test_path = self.coco_path + "images/test" + str(coco_type) + "/"
        self.train = ImageSource("train"+self.coco_type, train_path, self.logging)
        self.val = ImageSource("val"+self.coco_type, val_path, self.logging)
        self.test = ImageSource("test"+self.coco_type, test_path, self.logging)
        self.print("COCO has been initialized!")


    # train2017
    def insertTrainImage(self, file_name, height=1080, width=1920):
        if not os.path.isabs(file_name):
            file_name = self.src_imgs + file_name
        img_id, img_name = self.train.insertImage(file_name)
        if img_id != -1:
            self.annotation_train.insertImage(img_id=img_id, file_name=img_name, height=height, width=width)
        return img_id
    

    def insertTrainAnnotation(self, image_id, category_id, bbox:list, iscrowd=0):
        self.annotation_train.insertAnnotation(image_id=image_id, category_id=category_id, bbox=bbox, iscrowd=iscrowd)
    

    # val2017
    def insertValImage(self, file_name, height=1080, width=1920):
        if not os.path.isabs(file_name):
            file_name = self.src_imgs + file_name
        img_id, img_name = self.val.insertImage(file_name)
        if img_id != -1:
            self.annotation_val.insertImage(img_id=img_id, file_name=img_name, height=height, width=width)
        return img_id
    

    def insertValAnnotation(self, image_id, category_id, bbox:list, iscrowd=0):
        self.annotation_val.insertAnnotation(image_id=image_id, category_id=category_id, bbox=bbox, iscrowd=iscrowd)


    # test2017
    def insertTestImage(self, file_name, height=1080, width=1920):
        if not os.path.isabs(file_name):
            file_name = self.src_imgs + file_name
        img_id, img_name = self.test.insertImage(file_name)
        if img_id != -1:
            self.annotation_test.insertImage(img_id=img_id, file_name=img_name, height=height, width=width)
        return img_id
    

    def insertTestAnnotation(self, image_id, category_id, bbox:list, iscrowd=0):
        self.annotation_test.insertAnnotation(image_id=image_id, category_id=category_id, bbox=bbox, iscrowd=iscrowd)


    def saveAnnotation(self):
        self.annotation_train.save2json()
        self.annotation_val.save2json()
        self.annotation_test.save2json()

    
    def print(self, s):
        print(f"[{self.__class__.__name__}]>>> {s}")





class Annotation:

    def __init__(self, name, ann_url, old_ann_url="", categories=None, appending=False) -> None:

        # categories只有在创建一个全新的annotaion时会被引用，来初始化categories属性。
        # 如果是appending模式，则会读取原先old_ann_url中的categories
        # 在插入annotation时，关注的时category_id，所以要确保来自其他文件的标签映射关系和coco中标签映射关系一致
        # 例如：外部文件是从'MANDATORY'映射到0，而coco中的是从'mandatory'映射到0，id0都标示mandartory
        self.name = name
        self.content = None
        self.ann_url = ann_url
        self.info = {}
        self.licenses = []
        self.categories = []
        self.images = []
        self.annotations = []
        self.ann_id = 0

        if appending:
            self.check_annotation(old_ann_url=old_ann_url)
        else:
            self.is_append=False

        if not self.is_append:
            self.initInfo()
            self.initLicenses()
            if categories is None:
                raise ValueError("categories can't be None when initializing a new Annotation")
            self.initCategories(categories)

        
    def initInfo(self, description="coco dataset",
                url="",
                version="1.0",
                year=2017,
                contributor="",
                date_create=None):
        self.info = {
            "description": description,
            "url": url,
            "version": version,
            "year": year,
            "contributor": contributor,
            "date_created": date_create if date_create is not None else time.strftime("%Y-%m-%d", time.localtime())
        }
        self.print("info has been initialized!")


    def initLicenses(self, id=0, name="", url=""):
        self.licenses.append({"id": id, "name": name, "url": url})
        self.print("licenses has been initialized!")


    def initCategories(self, label_names=None):
        if label_names is None:
            label_names = ['mandatory', 'prohibitory', 'warning']
        for k, v in label_names.items():
            self.categories.append({
                "id":v,
                "name":k
            })
        self.print("categories have been initialized!")
        return self.categories

    
    def check_annotation(self, old_ann_url):
        if not os.path.isfile(old_ann_url):
            self.print(f"old annations file:{old_ann_url} doesn't exist, init a new coco!")
            self.is_append = False
            raise ValueError(f"error reading old_ann_url{old_ann_url}")
        else:
            self.is_append = True
            with open(old_ann_url, "r") as f:
                old_ann = json.load(f)
            self.info = old_ann['info']
            self.licenses = old_ann['licenses']
            self.categories = old_ann['categories']
            self.images = old_ann['images']
            self.annotations = old_ann['annotations']
            self.image_id = len(self.images)
            self.ann_id = len(self.annotations)
            self.print(f"successfully reading {old_ann_url}! load {self.image_id} images and {self.ann_id} annotations")
    

    def insertImage(self, img_id, file_name, height=1080, width=1920):

        self.images.append({
            "height": int(height), 
            "width": int(width), 
            "id": img_id,
            "file_name": file_name
        })


    def insertAnnotation(self, image_id, category_id, bbox:list, iscrowd=0):
        segmentation = [bbox[0], bbox[1], round(bbox[0]+bbox[2], 3), bbox[1],
                        round(bbox[0]+bbox[2]), round(bbox[1]+bbox[3], 3), bbox[0], round(bbox[1]+bbox[3], 3)]
        self.annotations.append({
            "id": self.ann_id,
            "image_id": image_id,
            "category_id": int(category_id),
            "segmentation": [segmentation],
            "bbox": bbox,
            "iscrowd": iscrowd,
            "area": round(Polygon(np.array(segmentation).reshape(-1, 2)).area, 3)
        })
        self.ann_id += 1
        return self.ann_id - 1


    def getCategoriesDict(self):
        dic = dict()
        for d in self.categories:
            dic[d['name']] = d['id']
        return dic


    def save2json(self):
        self.content = {'info': self.info, 'licenses': self.licenses, 'categories': self.categories, 'images': self.images, 'annotations': self.annotations}
        d = os.path.dirname(self.ann_url)
        if not os.path.exists(d):
            os.makedirs(d)
        with open(self.ann_url, "w") as f:
            json.dump(self.content, f)
            self.print("annotation has been saved to:"+self.ann_url)


    def getImageIdFromAnnotations(self):
        return self.image_id


    def print(self, s):
        print(f"[{self.__class__.__name__}:{self.name}]>>> {s}")




class ImageSource():

    def __init__(self, name="default", root_path=None, logging=True) -> None:
        self.name = name

        if root_path is None:
            raise ValueError("root_path can't be None")
        else:
            root_path = checkPath(root_path)
        self.path = root_path  # make sure it ends with '/' or '\\'.

        if not os.path.exists(root_path):
            os.makedirs(root_path)
            self.img_id = 0
        else:
            exist_imgs = os.listdir(root_path)
            if len(exist_imgs) == 0:
                self.img_id = 0
            else:
                last_img = exist_imgs[-1]
                n = last_img.split(".")[0]
                if not n.isdigit():
                    raise Exception(f"the name of the image in {name} is illegal!")
                self.img_id = int(n) + 1

        self.img_list = [] # only in few time, we need it.
        self.logging = logging
        self.log_url = f"./log/img-src-{self.name}.log"
        
        if self.logging:
            with open(self.log_url, "a+") as f:
                if not os.path.isdir(os.path.dirname(self.log_url)):
                    os.makedirs(os.path.dirname(self.log_url))
                head = ">"*100 + f"\n{time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())}\n"
                f.write(head)
        self.print(f"initialized!")
                
    

    # insert an image
    def insertImage(self, fro, img_type=None):

        # fro: it is best to be a absolute url, or we can't make sure it work.
        # to: 'jpg','png'..... if none, follow the original image.

        if img_type is None:
            img_type = fro.split(".")[-1]

        img_name = "{:0>8}".format(self.img_id) + "." + img_type
        to = self.path + img_name

        try:
            shutil.copyfile(fro, to)
            self.img_id += 1
            self.img_list.append(to)
            if self.logging:
                with open(self.log_url, "a+") as f:
                    f.write(f"{fro}-->{to}\n")
            else:
                self.print("insert one image, from {fro} to {to}.")
            
            return self.img_id-1, img_name
        except:
            self.print(f"there is some unexpected happend when copying {fro} to {to}!")
            return -1, -1
            

            
        

    def print(self, s):
        print(f"[{self.__class__.__name__}:{self.name}]>>> {s}")




def checkPath(p:str):
    if not (p.endswith("/") or p.endswith("\\")):
        return p+"/"
    else:
        return p
