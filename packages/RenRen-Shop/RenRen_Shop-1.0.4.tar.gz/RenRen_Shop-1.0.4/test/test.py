# -*- coding: utf-8 -*-
"""
@Time : 2022/4/6 15:07 
@Author : YarnBlue 
@description : 
@File : test.py 
"""
import json
import random
import time

from RenRen_Shop.factory import Factory


if __name__ == '__main__':
    with Factory() as client:
        data = {
            'status': 1,
        }
        goods_ids = client.goods.fetch_goodsIds_list(**data)
        print(len(goods_ids))
