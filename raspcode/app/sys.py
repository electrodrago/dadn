import cv2
import numpy as np

image = cv2.imread("data/image_5.jpg")
#image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
#image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)s
image = cv2.resize(image, (1080, 720))


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray = cv2.bilateralFilter(gray, 11, 17, 17)
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(gray,kernel,iterations = 2)
kernel = np.ones((4,4),np.uint8)
dilation = cv2.dilate(erosion,kernel,iterations = 2)
edged = cv2.Canny(dilation, 30, 200)
contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
rects = [cv2.boundingRect(cnt) for cnt in contours]
rects = sorted(rects,key=lambda  x:x[1],reverse=True)


filename = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
i = 0
prev_boxes = []
for c in contours:
    (x, y, w, h) = cv2.boundingRect(c)    
    if w * h > 12500 and w * h < 40000:
        out = gray[y+10:y+h-10,x+10:x+w-10]
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        prev_boxes.append([y + 2, y + h - 2, x + 2, x + w - 2])
        i = i + 1

prev_boxes = sorted(prev_boxes)
unique = []
for i in prev_boxes:
    if i not in unique:
        unique.append(i)

t = 20
del_list = []

for i in range(len(unique) - 1):
    if (abs(unique[i][0] - unique[i + 1][0]) < t) and (abs(unique[i][1] - unique[i + 1][1]) < t) and (abs(unique[i][2] - unique[i + 1][2]) < t) and (abs(unique[i][3] - unique[i + 1][3]) < t):
        del_list.append(i)

for i in reversed(del_list):
    del unique[i]

j = 0

for i in unique:
    kernel = np.ones((2, 2),np.uint8)


    
    out = gray[i[0]:i[1], i[2]:i[3]]
    out = cv2.erode(out, kernel, iterations = 1)
    cv2.imwrite('cropped\\' + str(filename[j]) + '.jpg', out)
    j += 1
    if j == 13:
        break