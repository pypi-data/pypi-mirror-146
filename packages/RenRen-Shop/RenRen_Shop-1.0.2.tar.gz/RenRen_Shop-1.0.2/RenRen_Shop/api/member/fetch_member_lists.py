# -*- coding: utf-8 -*-
"""
@Time : 2022/4/6 14:54 
@Author : YarnBlue 
@description : 
@File : fetch_member_lists.py 
"""
import time

from RenRen_Shop.common.fetch import Fetch


class FetchMemberList(Fetch):
    def __init__(self, session, **kwargs):
        """

        :param cookie:
        :param session:
        :param session_id:
        :param shop_id:
        :param kwargs:
        """
        super().__init__(session, **kwargs)
        self.first = self.URL.member_list()
        self.Temp = {
            'page': 1,
            'pagesize': 100,
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
        """

        :param kwargs: 可接受参数如下：

        =========================

        keyword: 关键词搜索，接受昵称，姓名，手机号

        source: 用户来源; 21:小程序

        level_id: 用户等级

        group_id: 用户标签

        is_blake: 是否黑名单

        label_field: 营销标签，值为 is_hot, is_new, is_recommand

        start_time: 开始时间， 时间格式2022-04-01 00:00:00

        end_time: 结束时间， 时间格式2022-04-01 00:00:00

        page: 页数

        pagesize: 每页数量大小

        =========================

        :return:
        """
        if kwargs:
            for index, (key, value) in enumerate(kwargs.items()):
                self.Temp[key] = value
        self.fetch(self.first, **kwargs)

    def next(self, **kwargs):
        """

        :param kwargs: 可接受参数如下：

        =========================

        keyword: 关键词搜索，接受昵称，姓名，手机号

        source: 用户来源; 21:小程序, 20:微信公众号, 10:H5, 30:抖音

        level_id: 用户等级

        group_id: 用户标签

        is_blake: 是否黑名单

        label_field: 营销标签，值为 is_hot, is_new, is_recommand

        start_time: 开始时间， 时间格式2022-04-01 00:00:00

        end_time: 结束时间， 时间格式2022-04-01 00:00:00

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
