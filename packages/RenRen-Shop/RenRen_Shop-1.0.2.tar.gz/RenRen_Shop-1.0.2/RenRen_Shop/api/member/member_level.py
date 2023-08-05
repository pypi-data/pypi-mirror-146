# -*- coding: utf-8 -*-
"""
@Time : 2022/4/6 15:35 
@Author : YarnBlue 
@description : 
@File : member_level.py 
"""
from RenRen_Shop.api.RenRen_api import RenRenApi


class MemberLevel(RenRenApi):
    def member_levels_list(self, **kwargs):
        """
        可选参数：
        ===============
        status: 等级是否启用
        keyword: 关键词查询
        ===============

        :param kwargs:
        :return:
        """
        params = {
            'pagesize': 100,
            'page': 1
        }
        for index, (key, value) in enumerate(kwargs.items()):
            params[key] = value
        rep = self.session.get(self.URL.member_level(), params=params, **self.kwargs)
        return rep.json()['list']
