# -*- coding: utf-8 -*-
'''
Since tushare 1.0.1, there are some new Interfaces.
Now we need get a connection first, then use bar() to get data.
'''
import sys
import os
import datetime as dt
import tushare as ts
import pandas as pd
import log_manager as lm


"""
These default Path are just for Windows users.
"""
_STOCK_DATA_DIR = r'D:\Workspace\QuantOne\StockDataA'
_STOCK_DATA_PER_DAY_DIR = r'D:\Workspace\QuantOne\StockDataA\Days'
_ALL_STOCK_BASICS_FILE_NAME = r'AllStockBasciInfo.csv'

"""
default Parameters
"""
_FILE_ENCODING = 'utf-8'
_DATE_TIME_FORMAT_YMD = '%Y-%m-%d'


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
        _df = ts.get_stock_basics()
        _log = 'Get Stock Basics OK.'
    except EnvironmentError:
        _log = 'Get Stock Basics FAILED.'
        sys.exit(1)
    lm.write_log_with_timestamp(_log)
    return _df


def save_all_stock_basics_to_csv(filedir=_STOCK_DATA_DIR, filename=_ALL_STOCK_BASICS_FILE_NAME,
    csv_mode='w', csv_header=True, csv_encoding=_FILE_ENCODING):
    """
    Save all stock basics Dataframe to csv file.
    """
    try:
        _df = ts_get_stock_basics_df()
        if not os.path.exists(filedir):
            os.mkdir(filedir)
        file_full_path = filedir + '\\' + filename
        _df.to_csv(file_full_path, mode=csv_mode, header=csv_header, encoding=csv_encoding)
        _log = 'SAVE all stock basics csv OK. File saved to {0}'.format(file_full_path)
    except EnvironmentError:
        _log = 'SAVE all stock basics csv FAILED.'
    lm.write_log_with_timestamp(_log)


def read_all_stock_basics_from_csv(filedir=_STOCK_DATA_DIR, filename=_ALL_STOCK_BASICS_FILE_NAME,
    csv_encoding=_FILE_ENCODING, csv_dtype='str'):
    try:
        file_full_path = filedir + '\\' + filename
        _df = pd.read_csv(file_full_path, encoding=csv_encoding, dtype=csv_dtype)
        _log = 'Load all stock basics from csv OK. Load from file {0}'.format(file_full_path)
    except EnvironmentError:
        _log = 'Load all stock basics from csv FAILED.'
    lm.write_log_with_timestamp(_log)
    return _df


def save_every_stock_data_to_csv(stock_freq='D', stock_adj='qfq', stock_factors=['vr', 'tor'], csv_dtype='str', csv_encoding=_FILE_ENCODING):
    '''
    Use tushare 1.0.2 Interface.
    Parameters:
        freq: 1min/5min/15min/30min/60min/D/W/M/Q/Y
        adj: qfq/hfq/None
        factors: ['vr','tor'] 'vr' means LiangBi, 'tor' means HuanShouLv
        ma:[5,10,20,60] Avg line. Because ma is calculated by the data you ask for. If the amount is less than\
        5, the ma will be nan. So we don't use this param.
    '''
    _df = read_all_stock_basics_from_csv()
    totalcount = _df['code'].shape[0]
    progress = 0
    for stock_code in _df['code']:
        try:
            if not os.path.exists(_STOCK_DATA_PER_DAY_DIR):
                os.mkdir(_STOCK_DATA_PER_DAY_DIR)
            file_full_path = _STOCK_DATA_PER_DAY_DIR + '\\' + stock_code + '.csv'
            # Use new function since tushare 1.0.2
            curr_conn = ts_get_connection()
            if os.path.exists(file_full_path):
                # if a stock data file already exists, get the lastest date from csv and then get new data.
                # Use bar() function instead of get_k_data()
                tmp_df = pd.read_csv(file_full_path, encoding=csv_encoding, dtype=csv_dtype)
                # Must descend 'datetime' series!
                _date_time_series_desc = tmp_df['datetime'].sort_values(ascending=False)
                # print(_date_time_series_desc)
                last_date = _date_time_series_desc.values[0]
                # print(last_date)
                # Then get today's datetime str %Y-%m-%d. And then add 1 day and convert to str.
                _start_date = dt.datetime.strftime(dt.datetime.strptime(last_date, _DATE_TIME_FORMAT_YMD)+dt.timedelta(days=1), _DATE_TIME_FORMAT_YMD)
                _df_bar_data = ts.bar(code=stock_code, conn=curr_conn, start_date=_start_date, freq=stock_freq, adj=stock_adj, factors=stock_factors)
                _df_bar_data = _df_bar_data.sort_index(ascending =True)
                _df_bar_data.to_csv(file_full_path, mode='a', header=False, encoding=csv_encoding)
            else:
                # The data we got is sorted by datetime Descending. And we will save all datetime Ascending.
                _df_bar_data = ts.bar(code=stock_code, conn=curr_conn, freq=stock_freq, adj=stock_adj, factors=stock_factors)
                _df_bar_data = _df_bar_data.sort_index(ascending =True)
                _df_bar_data.to_csv(file_full_path, mode='w', header=True, encoding=csv_encoding)
            _log = "Progress {0} of {1} is Done. Stock {2} data per day saved to {3}".format(
                progress, totalcount, stock_code, file_full_path)
            progress += 1
        except EnvironmentError:
            progress += 1
            _log = "Progress {0} of {1} is Failed. Stock {2} data per day saved to {3}".format(
                progress, totalcount, stock_code, file_full_path)
        lm.write_log_with_timestamp(_log)
