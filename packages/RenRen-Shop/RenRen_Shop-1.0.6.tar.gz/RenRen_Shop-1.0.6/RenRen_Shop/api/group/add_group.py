# -*- coding: utf-8 -*-
"""
@Time : 2022/4/1 20:04 
@Author : YarnBlue 
@description : 
@File : add_group.py 
"""
from RenRen_Shop.api.RenRen_api import RenRenApi


class AddGroup(RenRenApi):
    def add_group(self, name, status, *goods_ids):
        """

        :param name: 组名
        :param status: 状态；1:启动 2:关闭
        :param goods_ids:
        :return:
        """
        data = {
            'name': name,
            'status': status
        }
        for index, each in enumerate(goods_ids):
            data[f'goods_id[{index}]'] = each
        self.session.post(self.URL.add_group(), data=data)
