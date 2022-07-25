import os
import time
from shapely.geometry import Polygon
import json
import shutil
import numpy as np


class COCO:

    def __init__(self, src_img_path="E:/Output/carla/train2017/",
                    src_ann_path="E:/Output/carla/annotations/instances_train2017.json",
                    src_type = "",
                    root_path="E:/Data/dataset/TrafficSign/",
                    coco_type=2017,
                    copy=True,
                    is_append=True,
                    old_ann_path="",
                    cat = None
                    ) -> None:
        """
        # params:
        #   src_img_path: 源数据的图片文件夹
        #   src_ann_path: 源数据的标签文件
        #   src_type: 源文件标注的类型
        #   root_path: 生成coco数据的根目录
        #   coco_type: coco格式，现在只有2017格式
        #   copy: 是否将源数据的图片复制到 root_path/train2017
        #   is_append: 是否为插入模式，True的时候，会读取old_ann_path下的annotations.json(coco格式),在之前的内容后面追加。
        #   old_ann_path: 之前coco的标签，如果没有，就is_append修改为False
        #
        """

        # to
        self.root_path = root_path
        if not("".endswith("/") or self.root_path.endswith("\\")):
            self.root_path += "/"
        self.annotation_path = self.root_path + "annotations/instances_train"+str(coco_type)+".json"
        self.train_path = root_path + "train" + str(coco_type) + "/"
        self.val_path = root_path + "val" + str(coco_type) + "/"
        self.test_path = root_path + "test" + str(coco_type) + "/"

        # from
        self.src_img_path = src_img_path
        self.src_ann_path = src_ann_path
        self.src_type = src_type

        # coco object property
        self.coco = dict()
        self.info = None  # dict
        self.license = []   
        self.categories = []
        self.images = []
        self.annotations = []

        self.image_id = 0   # 对images标签中的id做一个全局记录
        self.annotation_id = 0   # 对annotation标签中的id做一个全局记录
        # self.categories_id = 0

        if copy:
            if not os.path.isdir(src_img_path):
                raise FileNotFoundError(f"{src_img_path} is not a valid dir")
            else:
                self.copy = True

                if not os.path.exists(self.train_path):
                    os.mkdir(self.train_path)
                    print(f"train image dir doesn't exist, create {self.train_path}")

                if not os.path.exists(self.val_path):
                    os.mkdir(self.val_path)
                    print(f"val image dir doesn't exist, create {self.val_path}")

                if not os.path.exists(self.test_path):
                    os.mkdir(self.test_path)
                    print(f"test image dir doesn't exist, create {self.test_path}")
        else:
            self.copy = False
        

        if is_append:  # 检查annotation文件是否存在，存在则读取，否则创建新文件
            self.check_annotation(old_ann_path=old_ann_path)
        else:
            self.is_append=False
        
        if not self.is_append:
            self.initInfo()
            self.initLicense()
            self.initCategories(cat)




    def check_annotation(self, old_ann_path):
        if not os.path.exists(old_ann_path):
            print(f"annotations.json({old_ann_path}) doesn't exist, init a new coco!")
            self.is_append = False
        else:
            self.is_append = True
            with open(old_ann_path, "r") as f:
                old_ann = json.load(f)
            self.info = old_ann['info']
            self.license = old_ann['license']
            self.categories = old_ann['categories']
            self.images = old_ann['images']
            self.annotations = old_ann['annotations']
            self.image_id = len(self.images)
            self.annotation_id = len(self.annotations)
            print(f"successfully reading {old_ann_path}! load {self.image_id} images and {self.annotation_id} annotations")




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
        print("coco info has inited!")




    def initLicense(self, id=0, name="", url=""):
        self.license.append({"id": id, "name": name, "url": url})
        print("coco license has inited!")




    def initCategories(self, label_names=None):
        if label_names is None:
            label_names = ['mandatory', 'prohibitory', 'warning']
        for i, name in enumerate(label_names):
            self.categories.append({
                "id":i,
                "name":name
            })
        print("coco categories have inited:\n", self.categories)
        return self.categories




    def insertImage(self, file_name, to=None, height=1080, width=1920):

        if to is None:
            raise ValueError("to can't be None")

        self.images.append({
            "height": height, 
            "width": width, 
            "id": self.image_id,
            "file_name": to
        })
        
        self.image_id += 1
        # print(f"coco images insert one:{file_name}")

        if self.copy:
            fro = self.src_img_path + file_name
            to = self.train_path + to
            shutil.copyfile(fro, to)
        return self.image_id - 1




    def insertAnnotation(self, image_id, category_id, bbox:list, iscrowd=0):
        segmentation = [bbox[0], bbox[1], round(bbox[0]+bbox[2], 3), bbox[1],
                        round(bbox[0]+bbox[2]), round(bbox[1]+bbox[3], 3), bbox[0], round(bbox[1]+bbox[3], 3)]
        self.annotations.append({
            "id": self.annotation_id,
            "image_id": image_id,
            "category_id": category_id,
            "segmentation": [segmentation],
            "bbox": bbox,
            "iscrowd": iscrowd,
            "area": round(Polygon(np.array(segmentation).reshape(-1, 2)).area, 3)
        })
        self.annotation_id += 1
        return self.annotation_id - 1




    def getCatDict(self):
        dic = dict()
        for d in self.categories:
            dic[d['name']] = d['id']
        return dic




    def save2json(self):
        self.coco = {'info': self.info, 'license': self.license, 'categories': self.categories, 'images': self.images, 'annotations': self.annotations}
        d = os.path.dirname(self.annotation_path)
        if not os.path.exists(d):
            os.makedirs(d)
        with open(self.annotation_path, "w") as f:
            json.dump(self.coco, f)
            print("coco has been saved to:"+self.annotation_path)

    


    """
    # TODO:
    #
    """
    def info(self):
        return self.info




    def license(self):
        return self.license


    
    def categories(self):
        return self.categories

    


    def images(self):
        return self.images



    
    def annotation(self):
        return self.annotations




if __name__ == '__main__':
    coco = COCO()





