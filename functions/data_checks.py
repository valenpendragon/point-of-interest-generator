import os.path
import pandas as pd
import numpy as np

def check_workbook(input_fp, ws_list):
    """
    Pulls all worksheets in the input_fp and compares the names with the
    ws_list to see if any are missing or misnamed.
    :param input_fp: filepath to an Excel workbook
    :param ws_list: list of str, names of worksheets to look for
    :return: dict: maps missing_names (list) to 'missing' key, unused worksheets
        found in sheet_names to 'extras', and bad worksheets to 'corrupt'.
    """
    f = pd.ExcelFile(input_fp)
    actual_worksheets = f.sheet_names
    missing_names = []
    data = {}
    corrupt_worksheets = []
    for name in ws_list:
        try:
            idx = actual_worksheets.index(name)
        except ValueError:
            missing_names.append(name)
        else:
            actual_worksheets.pop(idx)
            try:
                df = pd.read_excel(input_fp, sheet_name=name,
                                   index_col=None, na_values=False)
            except ValueError:
                corrupt_worksheets.append(name)
            else:
                # This was simply a test. We can get rid of the DataFrame.
                df = None

    if len(actual_worksheets) == 0:
        data['extras'] = None
    else:
        data['extras'] = actual_worksheets
        for name in actual_worksheets:
            try:
                df = pd.read_excel(input_fp, sheet_name=name,
                                   index_col=None, na_values=False)
            except ValueError:
                corrupt_worksheets.append(name)
            else:
                df = None

    if len(missing_names) == 0:
        data['missing'] = None
    else:
        data['missing'] = missing_names

    if len(corrupt_worksheets) == 0:
        data['corrupt'] = None
    else:
        data['corrupt'] = corrupt_worksheets

    f.close()
    return data
