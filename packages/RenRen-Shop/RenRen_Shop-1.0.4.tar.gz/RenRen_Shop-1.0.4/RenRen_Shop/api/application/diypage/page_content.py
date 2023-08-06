# -*- coding: utf-8 -*-
"""
@Time : 2022/4/7 14:14 
@Author : YarnBlue 
@description : 
@File : page_content.py 
"""
import json
import os.path

from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.common.common_fuc import template, exchange_params
from RenRen_Shop.common.log import log
logger = log().log()


class PageContent(RenRenApi):
    @staticmethod
    def secKill_edit(raw_content, **kwargs):
        """
        秒杀组件内容组成部分
        参数说明如下：（以__标注从属关系）
        ============================
        id: 固定值, seckill
        type: 固定值, seckill
        name: 固定值, 秒杀
        params: 组件元素，可选取固定值，可修改部分内容
        params__titlename: 秒杀标题文字内容
        params__activityGoodsType: 组件样式，0：滑动，1：列表
        params__bgstyle:标题背景
        params__showmore: 是否显示更多
        params__showtag: 是否显示价格标签
        params__tagtext: 价格标签文字
        params__activityData: 秒杀活动数据，调用秒杀活动接口获取信息，部分信息例如展示商品选择
        params__activityData__goods_ids: 展示的活动商品，list
        params__activityData__goods_count: 展示商品计数
        params__activityData__level:1, 未知，采用固定值1
        params__activityData__check: true, 未知，采用固定值
        params__goodsnum: 固定值，可展示的商品数量
        style: 组件样式风格，采用固定值即可
        data: 组件中展示商品数据，list，调用商品信息接口api.goods.goods_info获取信息,
        _comIndex_: 固定格式 "seckill_<时间戳前两位>_<linux时间戳（毫秒）>"
        例如："seckill_16_1649294757986"，若是现有则读取，若是新增则生成
        svg: "seckill", 固定值
        groupName: "营销组件", 固定值
        yIndex: 4, 固定值
        groupType: "4" ,固定值
        color: "#2d8cf0", 固定值
        typeid: "seckill", 固定值

        ============================

        :param raw_content: 源数据
        :param kwargs:
        :return:
        """

        data = exchange_params(raw_content, **kwargs)
        return data

    @staticmethod
    def fetch_seckill_content(page_content):
        """
        从页面内容中，返回秒杀的组件列表及index信息

        :return:
        """
        data = []
        for index, each_content in enumerate(page_content):
            if each_content['id'] == 'seckill':
                data.append([index, each_content])
        return data
