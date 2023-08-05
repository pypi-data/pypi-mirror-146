# -*- coding: utf-8 -*-
"""
@Time : 2022/4/6 16:07 
@Author : YarnBlue 
@description : 
@File : change_agent.py
"""
from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.common.log import log


class ChangeAgent(RenRenApi):
    def change_agent(self, agent_id, member_id) -> bool:
        """
        修改上级分销商

        :param agent_id:
        :param member_id:
        :return:
        """
        params = {
            'agent_id': agent_id,
            'member_id': member_id
        }
        rep = self.session.post(self.URL.change_agent(), data=params, **self.kwargs)
        if rep.json()['error'] == 0:
            return True
        else:
            log().logger.info(rep.text)
            return False
