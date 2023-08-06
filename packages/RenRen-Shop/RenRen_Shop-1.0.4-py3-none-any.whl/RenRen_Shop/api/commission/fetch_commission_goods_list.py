# -*- coding: utf-8 -*-
"""
@Time : 2022/4/8 17:37 
@Author : YarnBlue 
@description : 
@File : fetch_commission_goods_list.py 
"""
from .fetch_agent_list import FetchAgentsList


class FetchCommissionGoodsList(FetchAgentsList):
    def __init__(self, session, **kwargs):
        """

        :param cookie:
        :param session:
        :param session_id:
        :param shop_id:
        :param kwargs:
        """
        super().__init__(session, **kwargs)
        self.first = self.URL.commission_goods_list()
        self.Temp = {
            'page': 1,
            'pagesize': 10,
        }
        self.is_end = False
        self.next_page = 1
