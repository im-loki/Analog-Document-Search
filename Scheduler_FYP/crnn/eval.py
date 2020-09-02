""" Module to call the neural network function after taking care of the conditions that were specified earlier"""
import os
import argparse
import string
from tqdm import tqdm
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.python.keras import backend as K
from tensorflow.keras.models import model_from_json, load_model
from crnn.utils import pad_image, resize_image, create_result_subdir
from crnn.STN.spatial_transformer import SpatialTransformer
from crnn.models import CRNN, CRNN_STN
import gc

def set_gpus():
    os.environ["CUDA_VISIBLE_DEVICES"] = str(cfg.gpus)[1:-1]

def collect_data():
    if os.path.isfile(cfg.data_path):
        return [cfg.data_path]
    else:
        files = [os.path.join(cfg.data_path, f) for f in os.listdir(cfg.data_path) if f[-4:] in ['.jpg', '.JPG', '.png', '.PNG']]
        return files

def load_image(img_path):
    if cfg.nb_channels == 1:
        return cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    else:
        return cv2.imread(img_path)    

def preprocess_image(img):
    if img.shape[1] / img.shape[0] < 6.4:
        img = pad_image(img, (cfg.width, cfg.height), cfg.nb_channels)
    else:
        img = resize_image(img, (cfg.width, cfg.height))
    if cfg.nb_channels == 1:
        img = img.transpose([1, 0])
    else:
        img = img.transpose([1, 0, 2])
    img = np.flip(img, 1)
    img = img / 255.0
    if cfg.nb_channels == 1:
        img = img[:, :, np.newaxis]
    return img

def predict_text(model, img):
    y_pred = model.predict(img[np.newaxis, :, :, :])
    shape = y_pred[:, 2:, :].shape
    ctc_decode = K.ctc_decode(y_pred[:, 2:, :], input_length=np.ones(shape[0])*shape[1])[0][0]
    ctc_out = K.get_value(ctc_decode)[:, :cfg.label_len]
    result_str = ''.join([cfg.characters[c] for c in ctc_out[0]])
    result_str = result_str.replace('-', '')
    return result_str

def evaluate(model, data):
    if len(data) == 1:
        result = evaluate_one(model, data)
        return result

def evaluate_one(model, data):
    img = load_image(data[0])
    img = preprocess_image(img)
    result = predict_text(model, img)
    print('Detected result: {}'.format(result))
    return result

def ocr_event_trigger(arg):
    """Function to setup and apply the neural network"""
    global cfg
    cfg = arg
    set_gpus()

    _, model = CRNN_STN(cfg)
    model.load_weights(cfg.model_path)

    return model
    
def evaluate_string(model, file_path):
    data = [file_path] # return file list
    result = evaluate(model, data)
    return result