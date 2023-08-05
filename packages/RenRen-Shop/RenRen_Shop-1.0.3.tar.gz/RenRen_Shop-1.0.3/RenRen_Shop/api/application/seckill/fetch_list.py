# -*- coding: utf-8 -*-
"""
@Time : 2022/4/10 13:44 
@Author : YarnBlue 
@description : 
@File : fetch_list.py
"""
from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.api.goods.fetch_goods_list import FetchGoodsList


class List(FetchGoodsList):
    def __init__(self, session, **kwargs):
        super().__init__(session, **kwargs)
        self.first = self.URL.seckill_list()
        self.Temp = {
            'page': 1,
            'pagesize': 100,
        }

    def next(self, **kwargs):
        """

        :param kwargs: 可接受参数如下：

        =========================
        status: 活动状态；0: 未开始，1:进行中，-1: 停止，-2:手动停止

        keyword: 关键词搜索

        start_time:开始时间，2022-04-10 00:00

        end_time:结束时间

        goods_title:活动商品

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
