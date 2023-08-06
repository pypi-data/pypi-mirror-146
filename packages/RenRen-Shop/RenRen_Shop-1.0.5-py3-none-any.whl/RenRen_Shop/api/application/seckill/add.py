# -*- coding: utf-8 -*-
"""
@Time : 2022/4/7 9:57 
@Author : YarnBlue 
@description : 
@File : add.py 
"""
import json
import time

from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.api.goods.goods_info import GoodsInfo
from RenRen_Shop.common import time_2_str, str_2_time
from RenRen_Shop.common.log import log
from RenRen_Shop.configs.configs import DELAY

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

    def add_quick(self, *goods_ids, **kwargs):
        """
        必须参数：*goods_ids,  start_time, duration/end_time， title

        支持的属性如下：
        =============
        start_time: 开始时间, 2022-04-07 08:00:00
        duration:单位秒
        preheat:单位秒
        end_time: 结束时间
        preheat_time: 预热时间
        title: 秒杀标题
        is_commission: 开启分销
        limit_type: 限购类型
        limit_num
        =============

        快速增加秒杀活动
        :param kwargs: 秒杀的一些属性设置
        :param goods_ids: 需要参加秒杀的商品
        :return:
        """
        if kwargs.get('duration'):
            end_time = time_2_str(str_2_time(kwargs['start_time']) + int(kwargs['duration']))
        else:
            end_time = kwargs['end_time']
        if kwargs.get('preheat'):
            preheat_time = time_2_str(str_2_time(kwargs['start_time']) - int(kwargs['preheat']))
        else:
            preheat_time = kwargs['preheat_time'] if 'preheat_time' in kwargs.keys() else None
        data = {
            'rules[is_commission]': kwargs['is_commission'] if 'is_commission' in kwargs.keys() else 1,
            'rules[limit_type]': kwargs['limit_type'] if 'limit_type' in kwargs.keys() else 1,
            'rules[limit_num]': kwargs['limit_num'] if 'limit_num' in kwargs.keys() else 1,
            'is_preheat': 1 if 'preheat_time' in kwargs.keys() else 0,
            'client_type': kwargs['client_type'] if 'client_type' in kwargs.keys() else '21',
            'start_time': kwargs['start_time'],
            'end_time': end_time,
            'preheat_time': preheat_time,
            'title': kwargs['title']
        }
        goodsIds = ','.join(goods_ids)
        fetcher = GoodsInfo(self.session, **self.kwargs)
        goods_info = list()
        options = list()
        for goods_id in goods_ids:
            infos = fetcher.goods_info(goods_id)['data']
            time.sleep(DELAY)
            rules = list()
            if int(infos['has_option']):
                for option in infos['options']:
                    options.append(option['id'])
                    rules.append({'option_id': option['id'],
                                  'is_join': 1,
                                  'activity_price': float(option['price']) * 0.9,
                                  'activity_stock': int(option['stock'])
                                  })
                goods_info.append({'goods_id': infos['id'],
                                   'has_option': 1,
                                   'rules': rules
                                   })
            else:
                goods_info.append({'goods_id': infos['id'],
                                   'has_option': 0,
                                   'option_id': 0,
                                   'activity_stock': int(infos['stock']),
                                   'activity_price': 0.9 * float(infos['price']),
                                   })
        data['goods_info'] = json.dumps(goods_info)
        data['goods_ids'] = goodsIds
        data['option_ids'] = ','.join(options) if options else None

        rep = self.session.post(self.URL.seckill_add(), data=data, **self.kwargs)
        if rep.json()['error'] == 0:
            return True
        else:
            logger.error(rep.text)
            return False




