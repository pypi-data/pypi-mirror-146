# -*- coding: utf-8 -*-
"""
@Time : 2022/4/6 15:53 
@Author : YarnBlue 
@description : 
@File : member_infos.py 
"""
from RenRen_Shop.api.RenRen_api import RenRenApi


class Memberinfos(RenRenApi):
    def memer_infos(self, id):
        rep = self.session.get(self.URL.member_infos(), params={'id': id}, **self.kwargs)
        return rep.json()
