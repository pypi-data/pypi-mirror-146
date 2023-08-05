# -*- coding: utf-8 -*-
"""
@Time : 2022/4/7 9:57 
@Author : YarnBlue 
@description : 
@File : add.py 
"""

from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.common.log import log
logger = log().log()


class Add(RenRenApi):
    def add(self, is_commission=1, limit_type=1, limit_num=1, **kwargs):
        """
        参数解释如下:
        ======================================
        start_time: 2022-04-07 08:00:00
        end_time: 2022-04-07 10:00:00
        title: 秒杀活动标题
        is_preheat: 是否预热, 默认为1
        rules[is_commission]: 是否开启秒杀，默认1
        rules[limit_type]: 限购类型，0不限制，1每人限购，2每人每天限购.默认1
        rules[limit_num]: 限购数量。默认1
        goods_info: 参加商品的信息，参见template中的格式。json字符串
        client_type: 平台类型，21：小程序, 默认21
        preheat_time: 预热时间，2022-04-07 05:00:00
        goods_ids: 参与商品的id,多商品用,分割
        option_ids: 所有商品参与秒杀的sku_id
        ======================================

        :param limit_num:
        :param limit_type:
        :param is_commission:
        :param kwargs:
        :return:
        """
        data = {
            'rules[is_commission]': is_commission,
            'rules[limit_type]': limit_type,
            'rules[limit_num]': limit_num,
            'is_preheat': 1,
            'client_type': '21',

        }
        for index, (key, value) in enumerate(kwargs.items()):
            data[key] = value
        rep = self.session.post(self.URL.seckill_add(), data=data, **self.kwargs)
        if rep.json()['error'] == 0:
            return True
        else:
            logger.error(rep.text)
            return False

