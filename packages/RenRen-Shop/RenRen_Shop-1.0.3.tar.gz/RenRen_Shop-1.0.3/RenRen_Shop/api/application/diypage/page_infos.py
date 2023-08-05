# -*- coding: utf-8 -*-
"""
@Time : 2022/4/7 19:09 
@Author : YarnBlue 
@description : 
@File : page_infos.py 
"""
import json

from RenRen_Shop.api.RenRen_api import RenRenApi


class PageInfos(RenRenApi):
    def page_infos(self, id, type=10) -> json:
        rep = self.session.get(self.URL.page_edit(),
                               params={'id': id, 'type': type},
                               **self.kwargs)
        return rep.json()
