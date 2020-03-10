import pytesseract
from pytesseract import Output
import cv2
# import preprocessing
import subprocess
import re

# preprocessing.rotate_angle(img)
# img = preprocessing.get_grayscale(img)
# img = preprocessing.thresholding(img)
# img = preprocessing.deskew(img)

## Non ApI Based Approach ##
def call_ocr_non_api_way(fname):
    command = "python3 -W ignore crnn/eval.py --model CRNN --model_path ./crnn/Model/prediction_model.hdf5 --data_path ./"+fname
    getVersion =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout
    version =  getVersion.read()
    result = str(version.decode())
    predicted_text = re.search("Detected result: (.*)", result ,re.IGNORECASE)

    # print("My version is", result)
    if predicted_text:
        print(predicted_text.group(1))
        return predicted_text.group(1)
    return " "

def segment_process(img_src):
	print("Image Source: ", img_src)
	img = cv2.imread(img_src)
	d = pytesseract.image_to_data(img, output_type=Output.DICT)
	# print(d)

	n_w = 0
	total_string = ""
	n_boxes = len(d['level'])
	for i in range(n_boxes):
	    print(i, d['left'][i], d['top'][i], d['width'][i], d['height'][i])
	    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
	    if(x, y != 0, 0):
	        if(d['par_num'][i] != 0):
	            if(d['line_num'][i] != 0):
	                if(d['word_num'][i] != 0):
	                    # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) #draws borders
	                    # You have to extract Windows here
	                    n_w += 1
	                    print(w, h)
	                    crop_img = img[y:y+h, x:x+w]
	                    h = "crnn/Images/Saved" + str(n_w) + ".png"
	                    cv2.imwrite(h, crop_img)
	                    total_string +=  " " +  call_ocr_non_api_way(h)
	                        # cv2.imshow("Line", crop_img)
	                        # cv2.waitKey(0)
	print("No. of Words: ", n_w)
	print("String Detected: ", total_string)
	# cv2.imshow('img', img)
	# cv2.waitKey(0)
	return total_string

# segment_process("Images/i.png")

