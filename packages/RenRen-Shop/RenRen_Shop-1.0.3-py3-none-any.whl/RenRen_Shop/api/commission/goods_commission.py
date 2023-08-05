# -*- coding: utf-8 -*-
"""
@Time : 2022/4/8 17:44 
@Author : YarnBlue 
@description : 商品分销功能模块
@File : goods_commission.py
"""
from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.api.goods.edit_goods import EditGoods


class GoodsCommission(RenRenApi):
    def cancel_commission(self, goods_id):
        rep = self.session.post(self.URL.commission_cancel(), data={'id': goods_id}, **self.kwargs)
        return True if rep.json()['error'] == 0 else False

    def add_commission(self, goods_id):
        client = EditGoods(self.session, **self.kwargs)
        return client.edit_goods(goods_id, is_commission=1)

