# -*- coding: utf-8 -*-
"""
@Time : 2022/4/9 16:55 
@Author : YarnBlue 
@description : 批量设置分类
@File : set_category.py 
"""
from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.common import logger


class SetCategory(RenRenApi):
    def set_category(self, method, category_ids: list, *goods_ids):
        """


        :param method: 0：不替换原有分类， 1：替换原有分类
        :param category_ids: 商品分类ids, list
        :param goods_ids: 商品ids
        :return:
        """
        data = dict()
        data['method'] = method
        for index, category_id in enumerate(category_ids):
            data[f'category_id[{index}]'] = category_id

        for index, goods_id in enumerate(goods_ids):
            data[f'goods_id[{index}]'] = goods_id

        rep = self.session.post(self.URL.set_category(), data=data, **self.kwargs)
        if rep.json()['error'] == 0:
            return True
        else:
            logger.error(rep.text)
            return False
