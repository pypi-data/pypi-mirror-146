# -*- coding: utf-8 -*-
"""
@Time : 2022/4/1 14:49 
@Author : YarnBlue 
@description : 
@File : goods_info.py 
"""

from RenRen_Shop.api.RenRen_api import RenRenApi


class GoodsInfo(RenRenApi):
    def goods_info(self, goods_id):
        rep = self.session.get(self.URL.goods_info(), params={'id': goods_id}, **self.kwargs)
        return rep.json()


