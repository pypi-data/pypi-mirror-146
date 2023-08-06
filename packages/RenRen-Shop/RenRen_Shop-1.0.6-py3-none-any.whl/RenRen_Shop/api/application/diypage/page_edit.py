# -*- coding: utf-8 -*-
"""
@Time : 2022/4/7 13:45 
@Author : YarnBlue 
@description : 
@File : page_edit.py 
"""
import json

from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.common import logger


class PageEdit(RenRenApi):
    def page_edit(self, **kwargs):
        """
        参数如下：
        ==================================
        type: 页面类型， 10：首页  0：自定义页, 编辑前后保持一致，否则会失败
        id: 页面id
        name: 页面名称
        thumb: 封面图，图片base64值
        common: 页面通用设置
        content: 页面内容
        status: 页面状态
        ==================================

        :param kwargs:
        :return:
        """
        data = {
            'type': kwargs['type'],
            'id': kwargs['id'],
            'name': kwargs['name'],
            'thumb': kwargs['thumb'],
            'common': json.dumps(kwargs['common']) if isinstance(kwargs['common'], dict) else kwargs['common'],
            'content': json.dumps(kwargs['content']) if isinstance(kwargs['content'], list) else kwargs['content'],
            'status': kwargs['status']
        }
        rep = self.session.post(self.URL.page_edit(), data=data, **self.kwargs)
        if rep.json()['error'] == 0:
            return True
        else:
            logger.error(rep.text)
            return False
