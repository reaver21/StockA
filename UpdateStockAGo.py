# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 15:31:50 2017

@author: reave
"""

import tushare_io_functions as tu_io
import log_manager as lm


def main():
    lm.write_log_with_timestamp(lm.LOG_DEFAULT_STARTUP)
    tu_io.save_all_stock_basic_data_a_to_csv()
    tu_io.save_every_stock_data_per_day_to_csv()


if __name__ == '__main__':
    main()
