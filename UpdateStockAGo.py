# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 15:31:50 2017

@author: reave
"""

import tushare_functions_v1 as ts_func
import log_manager as lm


def main():
    lm.write_log_with_timestamp(lm._LOG_DEFAULT_STARTUP)
    ts_func.ts_get_version()
    #ts_func.ts_get_stock_basics_df()
    ts_func.save_all_stock_basics_to_csv()
    #tu_io.save_all_stock_basic_data_a_to_csv()
    #tu_io.save_every_stock_data_per_day_to_csv()


if __name__ == '__main__':
    main()
