from email.policy import default
import os
import argparse
import random

from coco import COCO


def print(s):
    print("[txtcoco]>>> ", s)

def check_paths(args):

    # 检查txt_path 
    if not os.path.isfile(args.txt_path):
        raise Exception(f"reading {args.txt_path} error!")

    # 检查coco_path
    if args.coco_path == "" or args.coco_path == ".":
        args.coco_path = os.path.abspath(".")+"\\coco"

    if not os.path.exists(args.coco_path):
        os.makedirs(args.coco_path)
        print(f"coco_path doesn't exist, create {args.coco_path}")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--txt_path', '-t',  type=str, default="./data/swedish/new.txt", help="the path of txt file")
    parser.add_argument('--coco_path', '-c',  type=str, default="./coco", help="the path of coco's home")
    parser.add_argument('--img_path', '-i',  type=str, default=".", help="the dir of source images")
    parser.add_argument('--split', '-s',  type=str, default="1", help="split the dataset(float),format:train_size,val_size,test_size")
    parser.add_argument('--appending', '-a', action="store_true", help="appending mode")
    parser.add_argument('--old_ann_path', '-o',  type=str, default=".", help="the path of the last annotation which you wanna append to")
    parser.add_argument('--no_copy',  action="store_false", help="whether copy the source image to coco")
    parser.add_argument('--cat',  type=str, default="./data/swedish/category.txt", help="the file where preserves categories")
    
    args = parser.parse_args()

    check_paths(args)

    # 读取split
    sp = [float(i) for i in args.split.split(",")]
    s = 0
    for i in sp:
        s += i
    if s != 1:
        raise ValueError("the sum of the proportions of train,val and test should be equal to 1!")
            
    # 读取categories
    if os.path.isfile(args.cat):
        f = open(args.cat, 'r')
        category_dict = dict()
        for c in f.readlines():
            k, v = c.rstrip("\n").split(":")
            category_dict[k] = v
    else:
        print(f"fail reading {args.cat}!")

    coco = COCO(src_ann_path=args.txt_path,
                     root_path=args.coco_path,
                    is_append=args.appending,
                    old_ann_path=args.old_ann_path,
                    copy=args.no_copy,
                    src_img_path=args.img_path
            )

    # 读取txt文件,导入coco
    with open(args.txt_path, "r") as f:

        data = f.readlines()
        index = list(range(len(data)))
        random.shuffle(index)

        for i in index:

            line = data[i]

            items = line.strip("\n").split(",")
            
            img_id = coco.insertImage(items[0], items[1], items[2])

            for j in range(3, len(items), 5):
                bbox = [round(float(b), 3) for b in items[j+1:j+5]]
                coco.insertAnnotation(img_id, category_dict[items[3]], bbox=bbox)
    coco.save2json()


    split_para = "7:2:1"  # 7train 2val 1test
    if not split_para:
        pass 
    else:
        tmp = split_para.split(":")
        s = 0
        for i in tmp:
            s += int(i)
        if s != 10:
            raise ValueError("Wrong!")
        # parse situations

    # origin_image_path -> shuffle -> parse split information -> 1.jpg 2.jpg 
    # log.txt xxxxx.jpg -> 2.jpg  


