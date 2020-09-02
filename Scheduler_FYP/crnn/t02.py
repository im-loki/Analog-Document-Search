from eval import ocr_event_trigger
import string

class ApiArguments(dict):
    """ This class is used to store the arguments for API implementation """
    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value

def call_ocr(fname, **kwargs):
    """Function to call the OCR functions without creating a subprocess"""
    arg = {
        "model_path": "./Model/prediction_model.hdf5",
        "data_path": "./" +fname,
        "gpus": [0],
        "characters": "0123456789" + string.ascii_lowercase+ "-",
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

    result = ocr_event_trigger(cfg)

    return result

print(call_ocr("Images/j.png"))