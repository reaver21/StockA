# -*- coding: utf-8 -*-
'''
Since tushare 1.0.1, there are some new Interfaces.
Now we need get a connection first, then use bar() to get data.
'''
import tushare as ts
import pandas as pd
import log_manager as lm
import sys
import os

"""
These default Path are just for Windows users.
"""
_STOCK_DATA_DIR = "D:\Workspace\QuantOne\StockDataA"
_STOCK_DATA_PER_DAY_DIR = "D:\Workspace\QuantOne\StockDataA\Days"
_ALL_STOCK_BASICS_FILE_NAME = 'AllStockBasciInfo.csv'
_FILE_ENCODING = 'gbk'


def ts_get_connection():
    """
    Get connection to tushare.
    """
    try:
        conn = ts.get_apis()
    except IOError:
        lm.write_log_with_timestamp('[Timeout] Connection Timeout.')
        sys.exit(1)
    return conn


def ts_get_version():
    """
    Get tushare version and write to log.
    """
    ts_version = ts.__version__
    lm.write_log_with_timestamp('tushare version: ' + ts_version)
    return ts_version


def ts_get_stock_basics_df():
    """
    Get all stock basics as Dataframe.
    """
    try:
        df = ts.get_stock_basics()
        LOG = 'Get Stock Basics OK.'
    except EnvironmentError:
        LOG = 'Get Stock Basics FAILED.'
        sys.exit(1)
    lm.write_log_with_timestamp(LOG)
    return df


def save_all_stock_basics_to_csv(filedir=_STOCK_DATA_DIR, filename=_ALL_STOCK_BASICS_FILE_NAME,
    csv_mode='w', csv_header=True, csv_encoding=_FILE_ENCODING):
    """
    Save all stock basics Dataframe to csv file.
    """
    try:
        df = ts_get_stock_basics_df()
        if not os.path.exists(filedir):
            os.mkdir(filedir)
        file_full_path = filedir + '\\' + filename
        df.to_csv(file_full_path, mode=csv_mode, header=csv_header, encoding=csv_encoding)
        LOG = 'SAVE all stock basics csv OK. File saved to {0}'.format(file_full_path)
    except EnvironmentError:
        LOG = 'SAVE all stock basics csv FAILED.'
    lm.write_log_with_timestamp(LOG)


def read_all_stock_basics_from_csv(filedir=_STOCK_DATA_DIR, filename=_ALL_STOCK_BASICS_FILE_NAME,
    csv_encoding=_FILE_ENCODING, csv_dtype = str):
    try:
        file_full_path = filedir + '\\' + filename
        df = pd.read_csv(file_full_path, encoding=csv_encoding, dtype=csv_dtype)
        LOG = 'Load all stock basics from csv OK. Load from file {0}'.format(file_full_path)
    except EnvironmentError:
        LOG = 'Load all stock basics from csv FAILED.'
    lm.write_log_with_timestamp(LOG)
    return df
