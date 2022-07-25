import os
import argparse
import random
import sys

from coco import COCO


def printf(s):
    print("[txt2coco]>>> ", s)


def printProgress(cur, all):
    n = (cur*100)//all
    print("\r", end="")
    print("progress:[{}{}] {}%".format(">"*n, " "*(100-n), n), end="")
    sys.stdout.flush()


def check_paths(args):

    # 检查txt_path 
    if not os.path.isfile(args.txt_path):
        raise Exception(f"reading {args.txt_path} error!")

    # 检查coco_path
    if args.coco_path == "" or args.coco_path == ".":
        args.coco_path = os.path.abspath(".")+"\\coco"

    if not os.path.exists(args.coco_path):
        os.makedirs(args.coco_path)
        printf(f"coco_path doesn't exist, create {args.coco_path}")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--txt_path', '-t',  type=str, default="./data/swedish/new.txt", help="the path of txt file")
    parser.add_argument('--coco_path', '-c',  type=str, default="./coco", help="the path of coco's home")
    parser.add_argument('--img_path', '-i',  type=str, default=".", help="the dir of source images")
    parser.add_argument('--split', '-s',  type=str, default="1", help="split the dataset(float),format:train_size,val_size,test_size")
    parser.add_argument('--appending', '-a', action="store_true", help="appending mode")
    parser.add_argument('--old_ann_path', type=str, default=".", help="the path of the last annotation which you wanna append to")
    parser.add_argument('--logging',  action="store_true", help="whether log the source image to coco")
    parser.add_argument('--cat',  type=str, default="./data/swedish/category.txt", help="the file where preserves categories")
    
    args = parser.parse_args()

    check_paths(args)

    # 读取split
    sp = [0, 0, 0]
    t = [i.strip() for i in args.split.split(",")]
    if len(t) == 3:
        if t[0] != "":
            sp[0] = float(t[0])
        if t[1] != "":
            sp[1] = float(t[1])
        if t[2] != "":
            sp[2] = float(t[2])
    elif len(t) == 1:
        sp[0] = float(t[0])
    else:
        raise ValueError("split accept 1 or 3 params!")

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
        f.close()
    else:
        printf(f"fail reading {args.cat}!")

    coco = COCO(
        coco_path=args.coco_path,
        src_imgs=args.img_path,
        old_ann_path=args.old_ann_path,
        categories=category_dict,
        appending=args.appending,
        logging=args.logging,
    )

    # 读取txt文件,导入coco
    with open(args.txt_path, "r") as f:

        progress = 0

        data = f.readlines()
        index = list(range(len(data)))
        random.shuffle(index)

        sp = [round(i*len(index)) for i in sp]
        trainset = index[0:sp[0]]
        valset = index[sp[0]:sp[0]+sp[1]]
        testset = index[sp[0]+sp[1]:]

        for i in trainset:
            line = data[i]
            items = line.strip().rstrip(",").split(",")

            # if len(items)<5:
            #     print("aaaaaa")

            img_id = coco.insertTrainImage(file_name=items[0], height=items[1], width=items[2])
            if(img_id == -1):
                printf("something error occured when insert an image into train!")

            for j in range(3, len(items), 5):
                bbox = [round(float(b), 3) for b in items[j+1:j+5]]
                coco.insertTrainAnnotation(image_id=img_id, category_id=category_dict[items[j]], bbox=bbox)
            progress += 1
            printProgress(progress, len(index))

        
        for i in valset:
            line = data[i]
            items = line.strip().rstrip(",").split(",")
            img_id = coco.insertValImage(file_name=items[0], height=items[1], width=items[2])
            if(img_id == -1):
                printf("something error occured when insert an image into val!")
            for j in range(3, len(items), 5):
                bbox = [round(float(b), 3) for b in items[j+1:j+5]]
                coco.insertValAnnotation(image_id=img_id, category_id=category_dict[items[j]], bbox=bbox)
            progress += 1
            printProgress(progress, len(index))


        for i in testset:
            line = data[i]
            items = line.strip().rstrip(",").split(",")
            img_id = coco.insertTestImage(file_name=items[0], height=items[1], width=items[2])
            if(img_id == -1):
                printf("something error occured when insert an image into test!")
            for j in range(3, len(items), 5):
                bbox = [round(float(b), 3) for b in items[j+1:j+5]]
                coco.insertTestAnnotation(image_id=img_id, category_id=category_dict[items[j]], bbox=bbox)
            progress += 1
            printProgress(progress, len(index))
        print()

    coco.saveAnnotation()


    # split_para = "7:2:1"  # 7train 2val 1test
    # if not split_para:
    #     pass 
    # else:
    #     tmp = split_para.split(":")
    #     s = 0
    #     for i in tmp:
    #         s += int(i)
    #     if s != 10:
    #         raise ValueError("Wrong!")
    #     # parse situations

    # # origin_image_path -> shuffle -> parse split information -> 1.jpg 2.jpg 
    # # log.txt xxxxx.jpg -> 2.jpg  


