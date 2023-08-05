# -*- coding: utf-8 -*-
"""
@Time : 2022/4/7 10:42 
@Author : YarnBlue 
@description : 我的秒杀活动
特性：
1 按需选择需要参与秒杀的商品
2 整点秒杀，全年循环
3 每场秒杀持续两小时
4 提前4个小时预热
5 固定比例库存参与活动
6 固定比例价格参与活动（取整）
@File : MySecKill.py 
"""
import json
import random
import time

from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.api.goods import FetchGoodsIdList
from RenRen_Shop.api.goods import GoodsInfo
from RenRen_Shop.api.application import SecKillAdd
from RenRen_Shop.common.log import log
from RenRen_Shop.common.common_fuc import *
from RenRen_Shop.api.goods.fetch_goodsId_list_by_filter import FetchGoodsIdList
logger = log().log()


class MySecKill(RenRenApi):
    @staticmethod
    def str_2_time(dt):
        timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        return timestamp

    @staticmethod
    def time_2_str(timestamp):
        # 转换为localtime
        time_local = time.localtime(timestamp)
        # 转换为新的时间格式
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt

    def get_goods_by_filter(self, **kwargs):
        """

        :param kwargs: 可接受参数如下：

        =========================
        status: 上下架商品，值为0或1

        keywords: 关键词搜索，接受名称，编码，条码

        label_field: 营销标签，值为 is_hot, is_new, is_recommand

        create_time[]: 时间范围，按列表传入 时间格式[2022-03-28+00:00,2022-03-28+00:00],因key包含[],以**kwargs传入

        category_id[]: 分类搜索，多个分类按表格传入，单个分类可以使用参数category_id,因key包含[],以**kwargs传入

        type: 类型，值为 all, 0, 1, 2, 3, 4, 5

        audit_status: 审核状态

        sub_shop_name: 子店铺名

        page: 页数

        pagesize: 每页数量大小

        =========================

        :return:
        """
        goods_ids = FetchGoodsIdList(self.session, **self.kwargs).fetch_goodsId_list(**kwargs)
        return goods_ids

    def build_goods_datas(self, stock_radio=1, price_radio=0.9, *goods_ids):
        """
        指定商品加入秒杀活动的数据生成方法，返回格式为：
        {
            'goods_info': json.dumps(goods_infos),
            'goods_ids': ','.join(ids),
            'option_ids': ','.join(option_ids)
        }

        :param stock_radio:
        :param price_radio:
        :param goods_ids:
        :return:
        """
        goods_infos = []
        ids = []
        option_ids = []
        for goods_id in goods_ids:
            goods_info = GoodsInfo(self.session, **self.kwargs).goods_info(goods_id)
            has_option = goods_info['data']['has_option']
            rules = []
            if int(has_option):
                options = goods_info['data']['options']
                for option in options:
                    try:
                        option_id = option['id']
                        stock = int(option['stock'])
                        if not stock:
                            continue
                        price = float(option['price'])
                        rule = {
                            'option_id': option_id,
                            'activity_stock': str(int(stock * float(stock_radio))),
                            'activity_price': str(round(price * float(price_radio), 1)),
                            'is_join': 1
                        }
                        rules.append(rule)
                        option_ids.append(option_id)
                    finally:
                        continue
                if rules:
                    ids.append(goods_id)
            data = {
                'goods_id': goods_id,
                'has_option': has_option,
                'rules': rules
            }
            goods_infos.append(data)
        return {
            'goods_info': json.dumps(goods_infos),
            'goods_ids': ','.join(ids),
            'option_ids': ','.join(option_ids)
        }

    def add_my_seckill(self,
                       start_time,
                       title,
                       stock_radio=1,
                       price_radio=0.9,
                       preheat=4.0,
                       duration=2.0,
                       *goods_ids):
        """
        对指定商品，生成秒杀活动

        :param start_time:
        :param title:
        :param stock_radio:
        :param price_radio:
        :param preheat:
        :param duration:
        :param goods_ids:
        :return:
        """
        start_timestamp = self.str_2_time(start_time)
        end_timestamp = start_timestamp + int(duration * 3600)
        preheat_timestamp = start_timestamp - int(preheat * 3600)
        end_time = self.time_2_str(end_timestamp)
        preheat_time = self.time_2_str(preheat_timestamp)

        goods_data = self.build_goods_datas(stock_radio, price_radio, *goods_ids)
        goods_info = goods_data['goods_info']
        goods_ids = goods_data['goods_ids']
        option_ids = goods_data['option_ids']

        data = {
            'start_time': start_time,
            'end_time': end_time,
            'title': title,
            'goods_info': goods_info,
            'preheat_time': preheat_time,
            'goods_ids': goods_ids,
            'option_ids': option_ids
        }
        if SecKillAdd(self.session, **self.kwargs).add(**data):
            logger.info('Done')
            return True
        else:
            return False

    def add_my_seckill_with_filter(self,
                       start_time,
                       title,
                       stock_radio=1,
                       price_radio=0.9,
                       preheat=4.0,
                       duration=2.0,
                       is_random=False,
                       random_radio=1.0,
                       **kwargs):
        """
        根据筛选条件，自动将商品生成秒杀活动

        :param random_radio: 随机加入的比例
        :param is_random: 是否开启随机
        :param duration: 活动持续时间，单位小时
        :param preheat: 预热时间，单位小时
        :param price_radio: 价格比例
        :param stock_radio: 库存比例
        :param start_time: 活动开始时间
        :param title: 活动标题
        :param kwargs: 商品筛选
        :return:
        """
        start_timestamp = self.str_2_time(start_time)
        end_timestamp = start_timestamp + int(duration * 3600)
        preheat_timestamp = start_timestamp - int(preheat * 3600)
        end_time = self.time_2_str(end_timestamp)
        preheat_time = self.time_2_str(preheat_timestamp)

        goods_ids_filter = self.get_goods_by_filter(**kwargs)
        if is_random:
            goods_ids_filter = random.sample(goods_ids_filter, int(len(goods_ids_filter) * random_radio))
        goods_data = self.build_goods_datas(stock_radio, price_radio, *goods_ids_filter)
        goods_info = goods_data['goods_info']
        goods_ids = goods_data['goods_ids']
        option_ids = goods_data['option_ids']

        data = {
            'start_time': start_time,
            'end_time': end_time,
            'title': title,
            'goods_info': goods_info,
            'preheat_time': preheat_time,
            'goods_ids': goods_ids,
            'option_ids': option_ids
        }
        if SecKillAdd(self.session, **self.kwargs).add(**data):
            logger.info('Done')
            return True
        else:
            return False

    def add_mySecKill_with_filter_and_time(self, start_dt, **kwargs):
        """
        对指定的商品，随机组成5个秒杀活动，每个活动持续2小时，提前4小时预热，从上午8点开始
        :param start_dt: 格式：2022-04-07 08:00:00
        :param kwargs:
        :return:
        """
        start_timdstamp = str_2_time(start_dt)
        goods_ids = FetchGoodsIdList(self.session, **self.kwargs).fetch_goodsId_list(**kwargs)
        count = len(goods_ids)
        random.shuffle(goods_ids)
        for i in range(5):
            goods = []
            if i != 4:
                for j in range(int(count * 0.2)):
                    goods.append(goods_ids.pop())
            else:
                goods = goods_ids

            start_time = time_2_str(start_timdstamp + 3600 * i * 3)
            self.add_my_seckill(start_time, f'{8 + i * 3}点整点秒杀', 1, 0.9, 24, 2, *goods)
