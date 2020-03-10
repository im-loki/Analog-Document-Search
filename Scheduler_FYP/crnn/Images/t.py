import pytesseract
from pytesseract import Output
import cv2
img = cv2.imread('f.png')

prev_x, prev_y = 0, 0

d = pytesseract.image_to_data(img, output_type=Output.DICT)
n_boxes = len(d['level'])
for i in range(n_boxes):
    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print(x, y, x+w, y+h)
    # You have to extract Windows here
    if i==4:
    	print(x, y, x+w, y+h)
    	crop_img = img[y:y+h, x:x+w]
    	cv2.imwrite("saved.jpg", crop_img)
    	cv2.imshow("cropped", crop_img)
    	cv2.waitKey(0)

cv2.imshow('img', img)
cv2.waitKey(0)