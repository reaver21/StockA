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
default_log_file_path = os.path.dirname(os.path.realpath(__file__)) + r"\log.txt"
LOG_DEFAULT_STARTUP = r'Automatic stock data update program start!'
LOG = ''


def write_log_with_timestamp(default_log_content=''):
    try:
        # open file
        log_file = os.open(default_log_file_path, os.O_CREAT | os.O_APPEND | os.O_RDWR)
        # format log content
        timestamp = '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] '
        LOG = default_log_content + '\n'
        # write log
        os.write(log_file, bytes(timestamp, 'GBK'))
        os.write(log_file, bytes(LOG, 'GBK'))
        os.close(log_file)
    except IOError:
        LOG = '[IO Error] log.txt process failed.'
    print(LOG)


def write_log_only(default_log_content=''):
    try:
        # open file
        log_file = os.open(default_log_file_path, os.O_CREAT | os.O_APPEND | os.O_RDWR)
        # format log content
        LOG = default_log_content + '\n'
        # write log
        os.write(log_file, bytes(LOG, 'GBK'))
        os.close(log_file)
    except IOError:
        LOG = '[IO Error] log.txt process failed.'
    print(LOG)


'''
basic
'''
