import cv2
import sys


# 生成category映射
# with open("./data/gtsdb/t.txt", "r") as f:
#     with open("./data/gtsdb/category.txt", "w") as fw:
#         lines = f.readlines()
#         for idx, line in enumerate(lines):
#             if "mandatory" in line:
#                 fw.write(f"{idx}:{0}\n")
#             if "prohibitory" in line:
#                 fw.write(f"{idx}:{1}\n")
#             if "danger" in line:
#                 fw.write(f"{idx}:{2}\n ")

img_dir = "E:/Data/dataset/GTSDB/"
fro = r"E:\Data\dataset\GTSDB\gt.txt"
to = "./data/gtsdb/convert.txt"


f = open("./data/gtsdb/category.txt", 'r')
category_dict = dict()
for c in f.readlines():
    k, v = c.rstrip("\n").split(":")
    category_dict[k] = v

with open(fro, "r") as f:
    with open(to, "w") as fw:
        lines = f.readlines()
        img_name = ""
        n = 0
        for line in lines:
            items = line.strip().split(";")
            if img_name != items[0]:
                img_name = items[0]
                n+=1
                img_url = img_dir+img_name
                img = cv2.imread(img_url)
                cv2.imwrite(img_url.split(".")[0]+".jpg", img)
                height, width = img.shape[0:2]
                fw.write("\n")
                fw.write(img_name.split(".")[0]+".jpg"+",")
                fw.write(f"{height},{width},")
            x1, y1, x2, y2 = [float(i) for i in items[1:5]]
            if category_dict.get(items[-1], 0) != 0:    
                fw.write(f"{items[-1]},{x1},{y1},{x2-x1},{y2-y1},")

            progress = (n*100) // 900
            print("\r", end="")
            print("progress:[{}{}] {}%".format(">"*progress, " "*(100-progress), progress), end="")
            sys.stdout.flush()
        print("\n>>> ", n)










"""
0 = speed limit 20 (prohibitory)
1 = speed limit 30 (prohibitory)
2 = speed limit 50 (prohibitory)
3 = speed limit 60 (prohibitory)
4 = speed limit 70 (prohibitory)
5 = speed limit 80 (prohibitory)
6 = restriction ends 80 (other)
7 = speed limit 100 (prohibitory)
8 = speed limit 120 (prohibitory)
9 = no overtaking (prohibitory)
10 = no overtaking (trucks) (prohibitory)
11 = priority at next intersection (danger)
12 = priority road (other)
13 = give way (other)
14 = stop (other)
15 = no traffic both ways (prohibitory)
16 = no trucks (prohibitory)
17 = no entry (other)
18 = danger (danger)
19 = bend left (danger)
20 = bend right (danger)
21 = bend (danger)
22 = uneven road (danger)
23 = slippery road (danger)
24 = road narrows (danger)
25 = construction (danger)
26 = traffic signal (danger)
27 = pedestrian crossing (danger)
28 = school crossing (danger)
29 = cycles crossing (danger)
30 = snow (danger)
31 = animals (danger)
32 = restriction ends (other)
33 = go right (mandatory)
34 = go left (mandatory)
35 = go straight (mandatory)
36 = go right or straight (mandatory)
37 = go left or straight (mandatory)
38 = keep right (mandatory)
39 = keep left (mandatory)
40 = roundabout (mandatory)
41 = restriction ends (overtaking) (other)
42 = restriction ends (overtaking (trucks)) (other)
"""


# img_url = r"E:\Data\dataset\GTSDB\00341.ppm"

# """
# 00088.ppm;412;440;436;464;8
# 00088.ppm;956;440;981;464;8

# 00341.ppm;923;465;997;533;13


# 00320.ppm;175;438;202;466;32
# 00320.ppm;921;403;951;434;32

# 00299.ppm;1245;247;1304;306;42
# """

# img = cv2.imread(img_url)
# x1, y1, x2, y2 = 923,465,997,533
# cv2.rectangle(img, [x1, y1], [x2, y2], color=[0, 0, 255], thickness=2)
# cv2.imshow("test", img)
# cv2.waitKey(0)

