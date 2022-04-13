import urllib.request
import cv2
import numpy as np
import imutils

url = "http://10.127.32.234:8080/shot.jpg"

while True:
    imgPath = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgPath.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    #img = imutils.resize(img, 400, 200)
    img = cv2.resize(img, (268, 201))
    cv2.imshow("a", img)
    if ord('q') == cv2.waitKey(1):
        exit(0)

# import cv2

# cap = cv2.VideoCapture('http://192.168.0.3:8080/video')

# while(True):
#     ret, frame = cap.read()
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         cv2.destroyAllWindows()
#         break