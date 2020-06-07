# import preprocessing
""" Module to call the neural network function after setting few parameters"""
import subprocess
from multiprocessing import Process, Queue
import os
import time
import re
import pytesseract
from pytesseract import Output
import cv2
import string
from sys import exit
from crnn.eval import ocr_event_trigger as oc1
from crnn.eval import evaluate_string as ev1
import gc

class ApiArguments(dict):
    """ This class is used to store the arguments for API implementation """
    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value

def call_ocr1(fname, **kwargs):
    """Function to call the OCR functions without creating a subprocess"""
    arg = {
        "model_path": "./crnn/Model/prediction_model.hdf5",
        # "data_path": "./"+fname,
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

    cfg = ApiArguments(arg)

    result = oc1(cfg)

    return result

def f0(name, q, d, l, u, img):
    time.sleep(1)
    total_string = ""
    string = list()
    n_w = 0
    model = call_ocr1("")
    for i in range(l, u):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if(x, y != 0, 0):
            if(d['par_num'][i] != 0):
                if(d['line_num'][i] != 0):
                    if(d['word_num'][i] != 0):
                        n_w += 1
                        crop_img = img[y:y+h, x:x+w]
                        h = "crnn/Images/Saved" + str(i) + ".png"
                        cv2.imwrite(h, crop_img)
                        string.append(ev1(model, h))
                        gc.collect()
    q.put(string)

def f1(name, q, d, l, u, img):
    time.sleep(1)
    total_string = ""
    string = list()
    n_w = 0
    model = call_ocr1("")
    for i in range(l, u):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if(x, y != 0, 0):
            if(d['par_num'][i] != 0):
                if(d['line_num'][i] != 0):
                    if(d['word_num'][i] != 0):
                        n_w += 1
                        crop_img = img[y:y+h, x:x+w]
                        h = "crnn/Images/Saved" + str(i) + ".png"
                        cv2.imwrite(h, crop_img)
                        string.append(ev1(model, h))
                        gc.collect()
    q.put(string)

def f2(name, q, d, l, u, img):
    time.sleep(1)
    total_string = ""
    string = list()
    n_w = 0
    model = call_ocr1("")
    for i in range(l, u):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if(x, y != 0, 0):
            if(d['par_num'][i] != 0):
                if(d['line_num'][i] != 0):
                    if(d['word_num'][i] != 0):
                        n_w += 1
                        crop_img = img[y:y+h, x:x+w]
                        h = "crnn/Images/Saved" + str(i) + ".png"
                        cv2.imwrite(h, crop_img)
                        string.append(ev1(model, h))
                        gc.collect()
    q.put(string)
def f3(name, q, d, l, u, img):
    time.sleep(1)
    total_string = ""
    string = list()
    n_w = 0
    model = call_ocr1("")
    for i in range(l, u):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if(x, y != 0, 0):
            if(d['par_num'][i] != 0):
                if(d['line_num'][i] != 0):
                    if(d['word_num'][i] != 0):
                        n_w += 1
                        crop_img = img[y:y+h, x:x+w]
                        h = "crnn/Images/Saved" + str(i) + ".png"
                        cv2.imwrite(h, crop_img)
                        string.append(ev1(model, h))
                        gc.collect()
                        
    q.put(string)

def segment_process(img_src):
    print("Image Source: ", img_src)
    # return pytesseract.image_to_string(img_src)
    img = cv2.imread(img_src)
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_w = 0
    total_string = ""
    n_boxes = len(d['level'])

    # Must be removed uses Tesseract #
    # print(d['text'])
    # for t_w in d['text']:
    #     if t_w != "":
    #         total_string += " " + re.sub('[();\/:\.+=\-?,]', " ", t_w.strip().lower())
    # return total_string
    # Must be removed uses Tesseract #

    l, u = list(), list()

    multi = 4

    for i in range(multi):
        l.append(int(i*(1/multi)*n_boxes))
        u.append(int((i+1)*(1/multi)*n_boxes))

    print(l, u)
    q0 = Queue()
    q1 = Queue()
    q2 = Queue()
    q3 = Queue()

    p0 = Process(target=f0, args=(str(0), q0, d, l[0], u[0], img,))
    p1 = Process(target=f1, args=(str(1), q1, d, l[1], u[1], img,))
    p2 = Process(target=f2, args=(str(2), q2, d, l[2], u[2], img,))
    p3 = Process(target=f3, args=(str(3), q3, d, l[3], u[3], img,))

    p0.start()
    p1.start()
    p2.start()
    p3.start()

    string_list = q0.get() + q1.get() + q2.get() + q3.get()
    return " ".join(string_list)
    # print(q0.get() + q1.get() + q2.get() + q3.get())