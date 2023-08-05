# -*- coding: utf-8 -*-
"""
@Time : 2022/4/7 21:54 
@Author : YarnBlue 
@description : 
@File : infos.py 
"""
from RenRen_Shop.api.RenRen_api import RenRenApi


class Infos(RenRenApi):
    def infos(self):
        self.session.get(self.URL.seckill_edit())