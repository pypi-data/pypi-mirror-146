# -*- coding: utf-8 -*-
"""
@Time : 2022/4/7 15:02 
@Author : YarnBlue 
@description : 
@File : common_fuc.py 
"""
import json
import os
import time
from RenRen_Shop.common.log import log
logger = log().log()


def str_2_time(dt):
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    return timestamp


def time_2_str(timestamp):
    # 转换为localtime
    time_local = time.localtime(timestamp)
    # 转换为新的时间格式
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt


def template(Type, filePath) -> json:
    with open(os.path.join(filePath, f'template/{Type}_template.json'), 'rb') as f:
        data = json.load(f)
    return data


def exchange_params(data, split='__', **kwargs):
    """
    对dict进行传入的key-value更新，支持多级嵌套修改，默认以__标识上下级关系，可使用__[num]__对下级为list的情况进行修改
    例如 ：“key1__2__key2 == value”
    表示：将原数据 key1 值中的第二个元素的key2 重新赋值为value

    :param data:
    :param split:
    :param kwargs:
    :return:
    """
    for index, (keys, value) in enumerate(kwargs.items()):
        if isinstance(value, int) or isinstance(value, float):
            value = str(value)
        key_split = keys.split(split)
        for i, each in enumerate(key_split):
            if each.isdigit():
                key_split[i] = int(each)
        level_count = len(key_split)
        if level_count == 1:
            data[key_split[0]] = value
        elif level_count == 2:
            data[key_split[0]][key_split[1]] = value
        elif level_count == 3:
            data[key_split[0]][key_split[1]][key_split[2]] = value
        else:
            logger.error('参数级数超过3')
    return data


def set_spec_id(title, raw_id=None):
    """
    生成规格属性id，如颜色;
    返回格式如下：
    =================
    {
        'type': 'spec',
        'title': title,
        'id': f'spec{int(time.time()*1000)}',
        'raw_id': raw_id
    }
    =================

    :param title: 规格名称，如颜色
    :param raw_id: 原spec_id
    :return:
    """
    return {
        'type': 'spec',
        'title': title,
        'id': f'spec{int(time.time()*1000)}',
        'raw_id': raw_id
    }


def set_child_spec_id(title, raw_id=None, raw_spec_id=None):
    """
    生成规格项id，如红色
    返回格式如下：
    ================
    {
        'type': 'childSpec',
        'title': title,
        'id': f'childSpec{int(time.time()*1000)}',
        'raw_id': raw_id,
        'raw_spec_id': raw_spec_id
    }
    ================

    :param title: 规格项名称，如红色
    :param raw_spec_id: 所属规格原spec_id
    :param raw_id: 原childSpec_id
    :return:
    """
    return {
        'type': 'childSpec',
        'title': title,
        'id': f'childSpec{int(time.time()*1000)}',
        'raw_id': raw_id,
        'raw_spec_id': raw_spec_id
    }
