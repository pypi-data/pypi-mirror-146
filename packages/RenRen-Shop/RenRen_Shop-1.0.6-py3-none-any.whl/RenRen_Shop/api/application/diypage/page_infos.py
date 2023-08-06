# -*- coding: utf-8 -*-
"""
@Time : 2022/4/7 19:09 
@Author : YarnBlue 
@description : 
@File : page_infos.py 
"""
import json

from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.common import logger


class PageInfos(RenRenApi):
    def page_infos(self, id, type) -> json:
        """
        返回格式为：
        ========================
        {
            'common': json.dumps(dict),
            'content': json.dumps(list),
            'creat_time':str,
            'id': str,
            'shop_id': str,
            'status': str,
            'template_id': str,
            'thumb': str,
            'type': str,
            'update_time': str
        }
        ========================
        :param id:
        :param type:
        :return:
        """
        rep = self.session.get(self.URL.page_edit(),
                               params={'id': id, 'type': type},
                               **self.kwargs)
        if rep.json()['error'] == 0:
            return rep.json()['data']
        else:
            logger.error(rep.text)
            return False
