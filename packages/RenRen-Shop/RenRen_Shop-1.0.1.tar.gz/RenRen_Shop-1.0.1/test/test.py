# -*- coding: utf-8 -*-
"""
@Time : 2022/4/6 15:07 
@Author : YarnBlue 
@description : 
@File : test.py 
"""
import json
import random

from RenRen_Shop.factory import Factory


if __name__ == '__main__':
    with Factory() as client:
        goods_ids = client.goods.filter_goods('real_sales', 2, '>')
        client.logger.info(f'筛选出的数量总数为：{len(goods_ids)}')
        print(goods_ids)
