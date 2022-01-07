#!/usr/bin/env python3
import cv2 
import numpy as np 
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
import math

image = cv2.imread('/home/grp-vert/catkin-ws/src/groupe-vert/vision_test/scripts/moin.jpg') 
  
# passage en niveau de gris
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
  
###### extration des régions avec la lib skimage

# Binarisation de l'image 
ret, thresh = cv2.threshold(gray, 127, 255, 1)
cv2.imshow("image seuillée",thresh)
cv2.waitKey(0)

# extraction des régions et des propriétés des régions
label_img = label(thresh)
regions = regionprops(label_img)
print(regions)
cv2.waitKey(0)

# affichage des régions et des boites englobantes
fig, ax = plt.subplots()
ax.imshow(thresh, cmap=plt.cm.gray)

for props in regions:
    y0, x0 = props.centroid
    orientation = props.orientation
    x1 = x0 + math.cos(orientation) * 0.5 * props.minor_axis_length
    y1 = y0 - math.sin(orientation) * 0.5 * props.minor_axis_length
    x2 = x0 - math.sin(orientation) * 0.5 * props.major_axis_length
    y2 = y0 - math.cos(orientation) * 0.5 * props.major_axis_length

    ax.plot((x0, x1), (y0, y1), '-r', linewidth=2.5)
    ax.plot((x0, x2), (y0, y2), '-r', linewidth=2.5)
    ax.plot(x0, y0, '.g', markersize=15)

    minr, minc, maxr, maxc = props.bbox
    bx = (minc, maxc, maxc, minc, minc)
    by = (minr, minr, maxr, maxr, minr)
    ax.plot(bx, by, '-b', linewidth=2.5)

ax.axis((0, 600, 600, 0))
plt.show()

cv2.waitKey(0)