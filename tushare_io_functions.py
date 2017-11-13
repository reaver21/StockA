# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 20:47:22 2017

@author: reave
"""

import tushare as ts
import pandas as pd
import log_manager as lm
import sys
import os

stock_data_dir = "D:\Workspace\QuantOne\StockDataA"
stock_data_per_day_dir = "D:\Workspace\QuantOne\StockDataA\Days"
csv_filepath_stock_data_a = stock_data_dir + r"\AllStockBasciInfo.csv"
file_encoding = 'utf-8'
LOG = ''

'''
Get all stock basic information and save to CSV
'''


def save_all_stock_basic_data_a_to_csv():
    try:
        df = tu_get_stock_basics_dataframe()
        if os.path.exists(csv_filepath_stock_data_a):
            df.to_csv(csv_filepath_stock_data_a, mode='w', header=False, encoding=file_encoding)
        else:
            df.to_csv(csv_filepath_stock_data_a, encoding=file_encoding)
        LOG = 'SAVE all stock basics csv OK. File saved to {0}'.format(csv_filepath_stock_data_a)
    except EnvironmentError:
        LOG = 'SAVE all stock basics csv FAILED.'
    lm.write_log_with_timestamp(LOG)


def read_all_stock_basic_data_a_from_csv(filepath=csv_filepath_stock_data_a):
    try:
        df = pd.read_csv(csv_filepath_stock_data_a, encoding=file_encoding, dtype=str)
        LOG = 'Load all stock basics from csv OK. Load from file {0}'.format(csv_filepath_stock_data_a)
    except EnvironmentError:
        LOG = 'Load all stock basics from csv FAILED.'
    lm.write_log_with_timestamp(LOG)
    return df


def save_every_stock_data_per_day_to_csv():
    df = read_all_stock_basic_data_a_from_csv()
    totalcount = df['code'].shape[0]
    progress = 1
    for code in df['code']:
        try:
            if not os.path.exists(stock_data_per_day_dir):
                os.mkdir(stock_data_per_day_dir)
            filename = stock_data_per_day_dir + '\\' + code + '.csv'
            df_k = ts.get_k_data(code)
            if os.path.exists(filename):
                df_k.to_csv(filename, mode='a', header=False, encoding=file_encoding)
            else:
                df_k.to_csv(filename, encoding=file_encoding)
            LOG = "Progress {0} of {1} is Done. Stock {2} data per day saved to {3}".format(
                progress, totalcount, code, filename)
            progress += 1
        except EnvironmentError:
            progress += 1
            LOG = "Progress {0} of {1} is Failed. Stock {2} data per day saved to {3}".format(
                progress, totalcount, code, filename)
        lm.write_log_with_timestamp(LOG)


'''
Tushare function:
Get all stock basic information, if failed, stop the program.
'''


def tu_get_stock_basics_dataframe():
    try:
        df = ts.get_stock_basics()
        LOG = 'Get Stock Basics OK.'
    except EnvironmentError:
        LOG = 'Get Stock Basics FAILED.'
        sys.exit(1)
    lm.write_log_with_timestamp(LOG)
    return df
