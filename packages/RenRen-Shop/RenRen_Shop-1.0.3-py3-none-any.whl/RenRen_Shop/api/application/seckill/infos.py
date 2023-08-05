# -*- coding: utf-8 -*-
"""
@Time : 2022/4/7 21:54 
@Author : YarnBlue 
@description : 
@File : infos.py 
"""
from RenRen_Shop.api.RenRen_api import RenRenApi


class Infos(RenRenApi):
    def infos(self, id):
        rep = self.session.get(self.URL.seckill_infos(), params={'id': id}, **self.kwargs)
        if rep.json()['error'] == 0:
            return rep.json()['data']