from .constants import Constants
import pandas as pd
import json
import os


def read_file(file_path):
    """
    Read data from the file.
    If the file does not exist, return None.
    """
    try:
        with open(file_path, 'r') as file:
            data = file.read()
    except FileNotFoundError:
        data = None

    return data


def read_csv_file(file_path):
    """
    Read data from the csv file.
    If the file does not exist, return None.
    """
    try:
        data = pd.read_csv(file_path)
        data = data.to_dict(orient="index")
    except FileNotFoundError:
        data = None

    return data


def write_csv_file(file_path, data):
    """
    Write data to the csv file.
    """
    data = pd.DataFrame(data)
    data.to_csv(file_path, index=False)


def read_json_file(file_path):
    """
    Read data from the json file.
    If the file does not exist, return None.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = None

    return data


def write_json_file(file_path, data):
    """
    Write data to the json file.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file)


def get_raw_file_path(filename):
    return os.path.join(Constants.Data.RAW_DATA_PATH, filename)


def get_processed_file_path(filename):
    return os.path.join(Constants.Data.PROCESSED_DATA_PATH, filename)
