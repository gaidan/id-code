import cv2
import numpy as np
from sys import argv
from PIL import Image, ImageDraw
from math import *
from time import *

st = time()

img = cv2.imread(argv[1])
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_green = np.array((40, 40, 40))
upper_green = np.array((70, 255, 255))
lower_yellow = np.array((20, 100, 100))
upper_yellow = np.array((30, 255, 255))
lower_lower_red = np.array((0, 120, 70))
lower_upper_red = np.array((10, 255, 255))
upper_lower_red = np.array((170, 120, 70))
upper_upper_red = np.array((180, 255, 255))
lower_purple = np.array((129, 50, 70))
upper_purple = np.array((158, 255, 255))
g_mask = cv2.inRange(hsv, lower_green, upper_green)
y_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
l_r_mask = cv2.inRange(hsv, lower_lower_red, lower_upper_red)
u_r_mask = cv2.inRange(hsv, upper_lower_red, upper_upper_red)
p_mask = cv2.inRange(hsv, lower_purple, upper_purple)
r_mask = l_r_mask + u_r_mask

img = cv2.bitwise_and(img, img, mask=g_mask)

coords = []
for i in range(0, g_mask.shape[0]):
    for j in range(0, g_mask.shape[1]):
        if g_mask[i][j] != 0:
            coords.append((j, i))
lr = coords[round(len(coords)/2)+25]

coords = []
for i in range(0, y_mask.shape[0]):
    for j in range(0, y_mask.shape[1]):
        if y_mask[i][j] != 0:
            coords.append((j, i))
ur = coords[round(len(coords)/2)+25]

coords = []
for i in range(0, r_mask.shape[0]):
    for j in range(0, r_mask.shape[1]):
        if r_mask[i][j] != 0:
            coords.append((j, i))
ul = coords[round(len(coords)/2)]

coords = []
for i in range(0, r_mask.shape[0]):
    for j in range(0, r_mask.shape[1]):
        if p_mask[i][j] != 0:
            coords.append((j, i))
ll = coords[round(len(coords)/2)+25]

print(ul)
print(ur)
print(ll)
print(lr)

im = Image.open(argv[1])
polygon = [ul, ur, lr, ll]
mask = Image.new("L", im.size, 0)
draw = ImageDraw.Draw(mask)
draw.polygon(polygon, fill=255, outline=None)
black = Image.new("RGB", im.size, (0, 0, 255))
result = Image.composite(im, black, mask)
angle = atan2(ur[1]-ul[1], ur[0]-ul[0])*(180/3.14)
result = result.rotate(angle, fillcolor=(0, 0, 255))
result.save("output.jpg")

result = cv2.imread("output.jpg")
hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
g_mask = cv2.inRange(hsv, lower_green, upper_green)
y_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
l_r_mask = cv2.inRange(hsv, lower_lower_red, lower_upper_red)
u_r_mask = cv2.inRange(hsv, upper_lower_red, upper_upper_red)
p_mask = cv2.inRange(hsv, lower_purple, upper_purple)
r_mask = l_r_mask + u_r_mask

coords = []
for i in range(0, g_mask.shape[0]):
    for j in range(0, g_mask.shape[1]):
        if g_mask[i][j] != 0:
            coords.append((j, i))
lr = coords[round(len(coords)/2)+25]

coords = []
for i in range(0, y_mask.shape[0]):
    for j in range(0, y_mask.shape[1]):
        if y_mask[i][j] != 0:
            coords.append((j, i))
ur = coords[round(len(coords)/2)+25]

coords = []
for i in range(0, r_mask.shape[0]):
    for j in range(0, r_mask.shape[1]):
        if r_mask[i][j] != 0:
            coords.append((j, i))
ul = coords[round(len(coords)/2)]

coords = []
for i in range(0, r_mask.shape[0]):
    for j in range(0, r_mask.shape[1]):
        if p_mask[i][j] != 0:
            coords.append((j, i))
ll = coords[round(len(coords)/2)+25]

print("=====")
print(ul)
print(ur)
print(ll)
print(lr)

dis0 = sqrt((ul[0]-ll[0])**2 + (ul[1]-ll[1])**2)
dis1 = sqrt((ur[0]-lr[0])**2 + (ur[1]-lr[1])**2)
square_size0 = dis0/8
square_size1 = dis1/8
avg_size = (square_size0+square_size1)/2

ang0 = atan2(ll[1]-ul[1], ll[0]-ul[0])
ang1 = atan2(lr[1]-ur[1], lr[0]-ur[0])

im = Image.open("output.jpg")

image_code = []

print("=====")
for i in range(0, 8):
    nxl = ul[0]+((square_size0*i)*cos(ang0))
    nyl = ul[1]+((square_size0*i)*sin(ang0))
    nxr = ur[0]+((square_size1*i)*cos(ang1))
    nyr = ur[1]+((square_size1*i)*sin(ang1))
    ang2 = atan2(nyr-nyl, nxr-nxl)
    dis2 = sqrt((nxl-nxr)**2+(nyl-nyr)**2)
    step = dis2/8
    binary = []
    for j in range(0, 8):
        tx = nxl+((step*j)*cos(ang2))
        ty = nyl+((step*j)*sin(ang2))
        cim = im.crop((tx, ty, tx+avg_size, ty+avg_size))
        cim = cim.resize((1, 1), resample=0)
        d_c = cim.getpixel((0, 0))
        d_c = (d_c[0]/255, d_c[1]/255, d_c[2]/255)
        b = 0
        v = 0
        for t in d_c:
            if t > b:
                b = t
        if (b*100) > 60:
            v = 0
        else:
            v = 1
        binary.append(v)
    image_code.append(int("".join([str(n) for n in binary]), 2))

image_code = [chr(n) for n in image_code]
image_code = "".join(image_code)
print(image_code)
