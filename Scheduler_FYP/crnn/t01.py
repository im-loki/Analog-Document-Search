# import preprocessing
""" Module to call the neural network function after setting few parameters"""
import subprocess
import re
import string
import pytesseract
import cv2
from pytesseract import Output
from crnn.eval import ocr_event_trigger

# preprocessing.rotate_angle(img)
# img = preprocessing.get_grayscale(img)
# img = preprocessing.thresholding(img)
# img = preprocessing.deskew(img)

class ApiArguments(dict):
    """ This class is used to store the arguments for API implementation """
    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value

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

def call_ocr(fname, **kwargs):
    """Function to call the OCR functions without creating a subprocess"""
    arg = {
        "model_path": "./crnn/Model/prediction/prediction_model.hdf5",
        "data_path": "./"+fname,
        "gpus": [0],
        "characters": "0123456789" + string.ascii_lowercase+"-",
        "label_len": 16,
        "nb_channels": 1,
        "width": 200,
        "height": 31,
        "model": "CRNN",
        "conv_filter_size": [64, 128, 256, 256, 512, 512, 512],
        "lstm_nb_units": [128, 128],
        "timesteps": 50,
        "dropout_rate": 0.25
    }

    """
    if not len(kwargs) == 0:
        for key, value in kwargs.items():
            if key in arg:
                arg[key] = value
            else:
                print(
                    "Invalid argument is API call. Invalid key was {}".format(
                        key
                    )
                )
    """

    cfg = ApiArguments(arg)

    result = ocr_event_trigger(cfg)

    return result

def segment_process(img_src):
    print("Image Source: ", img_src)
    img = cv2.imread(img_src)
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
	# print(d)

    n_w = 0
    total_string = ""
    n_boxes = len(d['level'])
        # Loop to iterate over all the bounding boxes
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
                        total_string +=  " " +  call_ocr(h)
                        #total_string +=  " " +  call_ocr_non_api_way(h)
	                    # cv2.imshow("Line", crop_img)
	                    # cv2.waitKey(0)
    print("No. of Words: ", n_w)
    print("String Detected: ", total_string)
	# cv2.imshow('img', img)
	# cv2.waitKey(0)
    return total_string

# segment_process("Images/i.png")

