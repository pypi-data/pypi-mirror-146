# -*- coding: utf-8 -*-
"""
@Time : 2022/4/7 13:45 
@Author : YarnBlue 
@description : 
@File : page_edit.py 
"""
from RenRen_Shop.api.RenRen_api import RenRenApi


class PageEdit(RenRenApi):
    def page_edit(self, **kwargs):
        """
        参数如下：
        ==================================
        type: ? 采用固定值10
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
            'type': 10,
            'id': kwargs['id'],
            'name': kwargs['name'],
            'thumb': kwargs['thumb'],
            'common': kwargs['common'],
            'content': kwargs['content'],
            'status': kwargs['status']
        }
        rep = self.session.post(self.URL.page_edit(), data=data, **self.kwargs)
        if rep.json()['error'] == 0:
            return True
        else:
            return False
