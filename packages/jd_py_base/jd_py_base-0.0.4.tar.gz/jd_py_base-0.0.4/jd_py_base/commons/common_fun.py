# -*- coding: UTF-8 -*-
import traceback
import datetime
import time
import os


def get_next_check_time():
    cur_time = datetime.datetime.now()
    cur_week_day = cur_time.weekday()
    if cur_week_day == 4 or cur_week_day == 5:
        next_check_time_str = (cur_time + datetime.timedelta(days=3)).strftime("%Y-%m-%d") + 'T08:30:00'
    else:
        next_check_time_str = (cur_time + datetime.timedelta(days=1)).strftime("%Y-%m-%d") + 'T08:30:00'
    return next_check_time_str
