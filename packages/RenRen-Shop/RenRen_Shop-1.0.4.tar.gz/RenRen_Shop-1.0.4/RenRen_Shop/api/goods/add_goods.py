# -*- coding: utf-8 -*-
"""
@Time : 2022/3/30 14:57 
@Author : YarnBlue 
@description : 
@File : add_goods.py 
"""
import json
import os
import time

import numpy as np

from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.common import logger


class AddGoods(RenRenApi):
    @staticmethod
    def template(type):
        filepath = os.path.dirname(__file__)
        with open(os.path.join(filepath, f'template/{type}_template.json'), 'rb') as f:
            data = json.load(f)
        return data

    @staticmethod
    def spec_id(title):
        """
        生成规格属性id，如颜色

        :return:
        """
        return {
            'type': 'spec',
            'title': title,
            'id': f'spec{int(time.time()*1000)}'
        }

    @staticmethod
    def child_spec_id(title):
        """
        生成规格项id，如红色

        :return:
        """
        return {
            'type': 'childSpec',
            'title': title,
            'id': f'childSpec{int(time.time()*1000)}'
        }

    @staticmethod
    def spec_data(raw):
        """
        返回数据格式：
        ====================
        [
         {
              "id": "spec1648622802529",
              "title": "颜色",
              "items": [
                   {
                        "id": "childSpec1648622802529",
                        "title": "红色",
                        "_sortId": "1648622949216_0.15230839649661587",
                        "specId": "spec1648622802529"
                   },
                   {
                        "id": "childSpec1648622972887",
                        "title": "黄色",
                        "display_order": 1,
                        "specId": "spec1648622802529",
                        "_sortId": "1648622972899_0.9147591621231812"
                   }
              ],
              "image_checked": "1"
         },
         {...},
        ]
        ====================
        :param raw: 源规格数据，格式为:{title1:items1, title2:items2,...}其中title为规格名称，items为该规格下的属性名称列表；
        如{'颜色':['红','黑'], '尺寸':['大','小']}
        :return:
        """
        # 获取原格式中的规格名称和规格项名称
        title_data = dict()
        for index, each in enumerate(raw):
            key = each['title']
            values = list()
            items = each['items']
            for item in items:
                values.append(item['title'])
            title_data[key] = values

        # 生成数据

    def add_goods(self,
                  goods: dict,  # 商品属性
                  spec: list,  # 多规格
                  options: list,  # 多规格定价
                  goods_commission: dict,  # 分销设置
                  member_level_discount: dict  # 会员折扣信息
                  ) -> bool:
        data = {
            'goods': json.dumps(goods),
            'spec': json.dumps(spec) if spec else None,
            'options': json.dumps(options) if options else None,
            'goods_commission': json.dumps(goods_commission),
            'member_level_discount': json.dumps(member_level_discount)
        }
        rep = self.session.post(self.URL.add_goods(), data=data)
        if rep.json()['error'] == 0:
            return True
        else:
            logger.error(rep.text)
            return False

    def add_goods_data_for_post(self, **kwargs):
        goods_data: dict = self.template('goods')

        # 更新商品详情信息
        goods_data['title'] = kwargs['title']  # 标题
        goods_data['type'] = int(kwargs['type'])  # 商品类型
        goods_data['sub_title'] = kwargs['sub_title']  # 副标题
        goods_data['short_title'] = kwargs['short_title']  # 短标题
        goods_data['thumb'] = kwargs['thumb']  # 首图
        goods_data['thumb_all'] = kwargs['thumb_all']  # 轮播图
        goods_data['category_id'] = kwargs['category_id']  # 分类
        goods_data['content'] = kwargs['content']  # 详情图
        goods_data['params'] = kwargs['params']  # 参数

        return goods_data

    def add_goods_from_csv(self, file):
        pass

    def add_goods_from_sql(self):
        pass


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)



