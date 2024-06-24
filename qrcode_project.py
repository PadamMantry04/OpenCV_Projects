import cv2
import numpy as np
from pyzbar.pyzbar import decode


def decodeQR(img):
    for barcode in decode(img):
        mydata = barcode.data.decode("utf-8")
        print(mydata)
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True,(255, 0, 255), 3)
        cv2.putText(img, mydata, (barcode.rect[0], barcode.rect[0]+2),cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_BRIGHTNESS, 35)

while True:
    success, img = cam.read()
    if not success:
        break

    decodeQR(img)
    cv2.imshow('Result', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

