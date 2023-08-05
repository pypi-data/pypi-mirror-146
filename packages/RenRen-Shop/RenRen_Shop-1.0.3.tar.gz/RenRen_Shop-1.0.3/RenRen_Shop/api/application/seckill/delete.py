# -*- coding: utf-8 -*-
"""
@Time : 2022/4/10 9:06
@Author : YarnBlue
@description :
@File : delete.py
"""
from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.common.common_fuc import logger


class Delete(RenRenApi):
    def seckill_delete(self, id):
        rep = self.session.get(self.URL.seckill_delete(), params={'id': id}, **self.kwargs)
        if rep.json()['error'] == 0:
            return True
        else:
            logger.error(rep.text)
            return False
