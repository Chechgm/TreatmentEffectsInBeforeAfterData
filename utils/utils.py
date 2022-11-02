""" General data and model utils
"""
import pickle
from typing import Dict


def load_model(model_dir: str):
    """ Loads a stan model
    """
    with open(model_dir, 'r') as f:
        model_definition = f.read()
    
    return model_definition


def data_saving(data_dictionary: Dict, data_dir: str):
    """ Saves a dictionary using pickle
    """
    with open(data_dir, "wb") as f:
        pickle.dump(data_dictionary, f)


def pkl_loading(data_dir: str):
    """ Loads a pickle dictionary
    """
    with open(data_dir, "rb") as f:
        data_dictionary = pickle.load(f)

    return data_dictionary


def txt_loading(data_dir: str):
    """ Loads a pickle dictionary
    """
    with open(data_dir, "rb") as f:
        data = f.read()

    return data
