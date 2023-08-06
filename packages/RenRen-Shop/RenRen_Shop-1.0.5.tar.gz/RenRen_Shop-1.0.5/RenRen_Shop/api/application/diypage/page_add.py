# -*- coding: utf-8 -*-
"""
@Time : 2022/4/12 19:13 
@Author : YarnBlue 
@description : 
@File : page_add.py 
"""
from RenRen_Shop.api.RenRen_api import RenRenApi


class PageAdd(RenRenApi):
    def page_add(self, **kwargs):
        """
        参数如下：
        ==================================
        type: 页面类型， 10：首页  0：自定义页
        name: 页面名称
        thumb: 封面图，图片base64值
        common: 页面通用设置
        content: 页面内容
        template_id: 页面状态
        ==================================

        返回格式为：{'error':0, 'id':1628}
        :param kwargs:
        :return:
        """
        data = {
            'type': kwargs['type'],
            'name': kwargs['name'],
            'thumb': kwargs['thumb'],
            'common': kwargs['common'],
            'content': kwargs['content'],
            'template_id': kwargs['template_id']
        }
        rep = self.session.post(self.URL.page_add(), data=data, **self.kwargs)
        if rep.json()['error'] == 0:
            return True
        else:
            return False
