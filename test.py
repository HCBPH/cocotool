import cv2
import os

img_url = "E:/Data/dataset/GTSDB/00000.ppm"
to = os.path.os.path.basename(img_url).split(".")[0] + ".jpg"
img = cv2.imread(img_url)
cv2.imwrite("./data/gtsdb/"+to, img)