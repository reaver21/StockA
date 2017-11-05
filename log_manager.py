# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 17:09:59 2017

@author: reave
"""

import os
import time

'''
Set default log_file_path
'''
_DEFAULT_LOG_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + r"\log.txt"
_LOG_DEFAULT_STARTUP = r'Automatic stock data update program start!'
LOG = ''


def write_log_with_timestamp(log_content=''):
    try:
        # open file
        log_file = os.open(_DEFAULT_LOG_FILE_PATH, os.O_CREAT | os.O_APPEND | os.O_RDWR)
        # format log content
        timestamp = '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] '
        LOG = log_content + '\n'
        # write log
        os.write(log_file, bytes(timestamp, 'GBK'))
        os.write(log_file, bytes(LOG, 'GBK'))
        os.close(log_file)
    except IOError:
        LOG = '[IO Error] log.txt process failed.'
    print(LOG)


def write_log_only(log_content=''):
    try:
        # open file
        log_file = os.open(_DEFAULT_LOG_FILE_PATH, os.O_CREAT | os.O_APPEND | os.O_RDWR)
        # format log content
        LOG = log_content + '\n'
        # write log
        os.write(log_file, bytes(LOG, 'GBK'))
        os.close(log_file)
    except IOError:
        LOG = '[IO Error] log.txt process failed.'
    print(LOG)


'''
basic
'''
