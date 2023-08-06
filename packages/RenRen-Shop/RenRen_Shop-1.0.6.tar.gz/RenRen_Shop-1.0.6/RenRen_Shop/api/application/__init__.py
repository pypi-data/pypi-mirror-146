# -*- coding: utf-8 -*-
"""
@Time : 2022/4/7 9:56 
@Author : YarnBlue 
@description : 
@File : __init__.py.py 
"""
from .seckill import Add as SecKillAdd, Edit as SecKillEdit, Delete as SecKillDelete
from .seckill import Infos as SecKillinfos, List as FetchSecKillList
from .diypage import *
from .goods_helper import *

__all__ = ['SecKillAdd',
           'SecKillEdit',
           'SecKillDelete',
           'FetchSecKillList',
           'SecKillinfos',
           'PageEdit',
           'PageInfos',
           'PageContent',
           'GoodsHelper',
           'PageAdd'
           ]
