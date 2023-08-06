# -*- coding: utf-8 -*-
"""
@Time : 2022/4/6 16:03 
@Author : YarnBlue 
@description : 
@File : fetch_agent_list.py 
"""
import time

from RenRen_Shop.common.fetch import Fetch


class FetchAgentsList(Fetch):
    def __init__(self, session, **kwargs):
        """
        start() 启动时可以输入属性值，
        type:商品类型，可以为all, 0, 1, 2, 3, 4


        :param cookie:
        :param session:
        :param session_id:
        :param shop_id:
        :param kwargs:
        """
        super().__init__(session, **kwargs)
        self.first = self.URL.agent_list()
        self.Temp = {
            'page': 1,
            'pagesize': 10,
        }
        self.is_end = False
        self.next_page = 1

    def fetch(self, url, **kwargs):
        for index, (key, value) in enumerate(kwargs.items()):
            self.Temp[key] = value
        rep = self.session.get(url, params=self.Temp).json()
        self.data = rep['list']
        self.next_page = rep['page'] + 1
        self.previous_page = rep['page'] - 1
        if rep['total'] < rep['page_size'] or len(self.data) == 0:
            self.is_end = True
        else:
            self.is_end = False
        if rep['page'] == 1:
            self.is_start = True
        else:
            self.is_start = False

    def start(self, **kwargs):
        if kwargs:
            for index, (key, value) in enumerate(kwargs.items()):
                self.Temp[key] = value
        self.fetch(self.first, **kwargs)

    def next(self, **kwargs):
        """

        :param kwargs: 可接受参数如下：

        =========================

        keywords: 关键词搜索

        page: 页数

        pagesize: 每页数量大小

        =========================

        :return:
        """
        if self.is_end:
            return False
        else:
            if kwargs:
                for index, (key, value) in enumerate(kwargs.items()):
                    self.Temp[key] = value
            self.Temp['page'] = self.next_page
            self.fetch(self.first, **self.Temp)
            return True

    def previous(self) -> bool:

        if self.is_start:
            return False
        else:
            self.Temp['page'] = self.previous_page
            self.fetch(self.first, **self.Temp)
            return True

    def result(self):
        return self.data
