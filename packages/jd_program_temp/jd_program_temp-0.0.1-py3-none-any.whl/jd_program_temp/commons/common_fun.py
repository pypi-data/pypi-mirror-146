# -*- coding: UTF-8 -*-
import traceback
import datetime
import time
import os
import zipfile


def get_next_check_time():
    """获取下一次交易日期"""
    cur_time = datetime.datetime.now()
    cur_week_day = cur_time.weekday()
    if cur_week_day == 4 or cur_week_day == 5:
        next_check_time_str = (cur_time + datetime.timedelta(days=3)).strftime("%Y-%m-%d") + 'T08:30:00'
    else:
        next_check_time_str = (cur_time + datetime.timedelta(days=1)).strftime("%Y-%m-%d") + 'T08:30:00'
    return next_check_time_str


def check_path(path, check_file_size=False, min_size=3 * 1024):
    """检查文件是否存在"""
    if not check_file_size:
        return True if os.path.exists(path) else False
    else:
        return True if os.path.exists(path) and os.path.getsize(path) >= min_size else False


def un_zip(file_name, out_path):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    zip_file.extractall(out_path)
    zip_file.close()


def get_file_size(dir_path, date_str):
    count = 0
    for file in os.listdir(dir_path):
        if date_str in file:
            count += 1
    return count


def get_path_size(str_path):
    if not check_path(str_path):
        return 0

    if os.path.isfile(str_path):
        return os.path.getsize(str_path)

    n_total_size = 0
    for strRoot, lsDir, lsFiles in os.walk(str_path):
        # get child directory size
        for strDir in lsDir:
            n_total_size = n_total_size + get_path_size(os.path.join(strRoot, strDir))
        for strFile in lsFiles:
            n_total_size = n_total_size + os.path.getsize(os.path.join(strRoot, strFile))
    return n_total_size


def tuple_to_file(tuple_data, file_path):
    write_data_str = ','.join([str(x).strip() for x in tuple_data])
    with open(file_path, 'a') as file_object:
        file_object.write(write_data_str + '\n')
        file_object.close()


def get_current_date(date_format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(date_format)


def get_now_timedate():
    return (datetime.datetime.today()).strftime('%Y%m%d%H')


def try_get(obj, path):
    try:
        for p in path:
            if obj is None:
                return ''
            if isinstance(obj, list):
                obj = obj[p]
            else:
                obj = obj.get(p)
        return '' if obj is None else obj
    except Exception as e:
        return ''



