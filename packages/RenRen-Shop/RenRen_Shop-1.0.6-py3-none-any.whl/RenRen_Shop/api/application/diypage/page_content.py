# -*- coding: utf-8 -*-
"""
@Time : 2022/4/7 14:14 
@Author : YarnBlue 
@description : 
@File : page_content.py 
"""
import copy
import json
import time

from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.common.common_fuc import template, exchange_params
from RenRen_Shop.common.log import log
from RenRen_Shop.api.application.seckill.infos import Infos as SecKillInfos
from RenRen_Shop.api.goods.goods_info import GoodsInfo
from RenRen_Shop.configs.configs import DELAY

logger = log().log()


class PageContent(RenRenApi):
    @staticmethod
    def edit_page_content_part(pageinfo: dict, index: int, content: dict):
        """

        :param pageinfo: 页面信息
        :param index: 组件序号
        :param content: 组件修改后的内容
        :return:
        """
        pagecontent_str = pageinfo['content']
        pagecontent = json.loads(pagecontent_str)
        pagecontent[index] = content
        pagecontent_str = json.dumps(pagecontent)
        pageinfo['content'] = pagecontent_str
        return pageinfo

    @staticmethod
    def fetch_content(page_content: list[dict], type_id):
        """
        从页面内容中，返回指定类型组件列表及index信息
        :param page_content:
        :param type_id: 组建类型，可取值如下：
        ========================
        fixedsearch: 固定搜索框
        blank: 辅助空白
        banner: 图片轮播
        menu: 菜单栏
        title: 标题栏
        goods: 商品组
        seckill: 秒杀
        picture: 单图组
        diymenu: 自定义菜单
        ========================
        :return:
        """
        data = []
        for index, each_content in enumerate(page_content):
            if each_content['id'] == type_id:
                data.append([index, each_content])
        return data

    def secKill_edit(self, raw_content: dict, **kwargs):
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
        params__activityData: 秒杀活动数据，调用秒杀活动接口获取信息，部分信息例如展示商品选择，根据params__activityData__id自动生成
        params__activityData__id: 秒杀活动id，指定后自动生成默认params__activityData,然后再根据传入参数值修改
        params__activityData__goods_ids: 展示的活动商品，list
        params__activityData__goods_count: 展示商品计数
        params__activityData__level:1, 未知，采用固定值1
        params__activityData__check: true, 未知，采用固定值
        params__goodsnum: 固定值，可展示的商品数量
        style: 组件样式风格，采用固定值即可
        data: 组件中展示商品数据，list
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
        if 'params__activityData__id' in kwargs.keys():
            info_getter = SecKillInfos(self.session, **self.kwargs)
            # 获取秒杀活动信息
            infos = info_getter.infos(kwargs['params__activityData__id'])
            goods_info = infos['goods_info']
            goods_ids = list()
            for each in goods_info:
                goods_ids.append(each['id'])
            goods_ids_select = goods_ids[0:min(len(goods_ids), 20)] \
                if 'params__activityData__goods_ids' not in kwargs.keys() \
                else kwargs['params__activityData__goods_ids']
            activityData = {
                'id': infos['id'],
                'title': infos['title'],
                'inner_type': infos['inner_type'],
                'start_time': infos['start_time'],
                'end_time': infos['end_time'],
                'stop_time': infos['stop_time'],
                'status': infos['status'],
                'goods_ids': goods_ids,
                'level': '1',
                'goods_count': len(goods_ids),
                'checked': True
            }
            kwargs['params__activityData'] = activityData
            data_res = []
            for goodsId in goods_ids_select:
                seckilldata = copy.deepcopy(infos)
                goods_info_raw = copy.deepcopy(infos['goods_info'])
                seckilldata['goods_info'] = list()
                goodsInfo = GoodsInfo(self.session, **self.kwargs).goods_info(goodsId)['data']
                time.sleep(DELAY)
                # option_id = goodsInfo['options'][0]['id'] if int(goodsInfo['has_option']) else None
                # original_stock = goodsInfo['options'][0]['stock'] \
                #     if int(goodsInfo['has_option']) \
                #     else goodsInfo['stock']
                option_id = None
                activity_stock = '0'
                original_stock = '0'
                activity_price = '0'
                activity_sales = '0'
                price = '0'
                productprice = '0'
                is_join = '1'
                for each_raw in goods_info_raw:
                    if int(each_raw['id']) == int(goodsId):
                        if int(goodsInfo['has_option']):
                            option_id = each_raw['rules'][0]['id']
                            activity_stock = each_raw['rules'][0]['activity_stock']
                            activity_price = each_raw['rules'][0]['activity_price']
                            is_join = each_raw['rules'][0]['is_join']
                            break
                        else:
                            option_id = None
                            activity_stock = each_raw['stock']
                            activity_price = each_raw['price']
                            activity_sales = each_raw['sales'] if 'sales' in each_raw.keys() else '0'
                if option_id:
                    for option in goodsInfo['options']:
                        if option_id == option['id']:
                            original_stock = option['stock']
                            price = option['price']
                            productprice = option['original_price']
                            break
                else:
                    original_stock = goodsInfo['stock']
                seckilldata['goods_info'] = [(dict(id=goodsInfo['id'],
                                                   shop_id=infos['shop_id'],
                                                   activity_id=infos['id'],
                                                   goods_id=goodsId,
                                                   option_id=option_id,
                                                   original_stock=original_stock,
                                                   activity_stock=activity_stock,
                                                   activity_price=activity_price,
                                                   activity_sales=activity_sales,
                                                   is_join=is_join,
                                                   sub_shop_id=infos['sub_shop_id']
                                                   )
                                              )]
                seckilldata['price_range'] = dict(min_price=activity_price, max_price=activity_price)
                seckilldata['activity_stock'] = activity_stock
                seckilldata_ = copy.deepcopy(seckilldata)
                item = dict(thumb=goodsInfo['thumb'],
                            price=price,
                            productprice=productprice,
                            sales=goodsInfo['sales'],
                            sub_title=goodsInfo['sub_title'],
                            title=goodsInfo['title'],
                            id=goodsId,
                            gid=goodsId,
                            bargain=0,
                            credit=0,
                            ctype=0,
                            has_option=goodsInfo['has_option'],
                            type=goodsInfo['type'],
                            presellData='',
                            seckillData=seckilldata_,
                            groupsData='',
                            groupsRebateData='',
                            groupsFissionData='',
                            preloading=False,
                            countTime=['2', '59', '59', '59']
                            )
                data_res.append(copy.deepcopy(item))
            kwargs['data'] = data_res
        datas = exchange_params(raw=raw_content, **kwargs)
        return datas

    def goods_edit(self, raw_content: dict, *goods_ids, **kwargs):
        """
        （注意：data参数，只需指定gid和id即可，其它属性可不传入）

        商品组组建内容编辑，属性修改如下：
        *goods_ids, 输入指定商品
        kwargs参数说明如下：（以__标注从属关系）

        ==============================
        params: 组建元素
        params__goodstype: 商品类型 0：商城商品 1：积分商品
        params__showprice: 是否显示商品售价
        params__showtag: ？
        params__goodsdata: 添加商品 1:手动选择, 2:选择分类, 3:选择分组, 4:营销属性
        params__cateid: 商品分类id
        params__catename: 分类名称
        params__groupid: 商品分组id
        params__groupname: 商品分组名称
        params__goodssort: 1:综合排序 2:按销量 3:价格排序 4:价格升序
        params__goodsnum: 商品显示数量，最多50
        params__showicon: 商品角标
        params__iconposition: 角标位置。如：'left top'
        params__productprice: 划线价
        params__productpricetext: 划线价文字
        params__showsales: 显示销量
        params__salestext: 销量文字
        params__productpriceline: ?
        params__pagetype: 页面类型 ?
        params__seecommission: ？
        params__cansee: ？
        params__seetitle: ？
        params__goodsscroll: 商品滚动
        params__goodsiconsrc: 角标图片链接
        params__icontype: 角标样式
        params__customicontext: 角标文字
        params__componentbg: 组建背景
        params__bgimg: 背景图
        params__commisionstype:佣金样式
        params__commisiontext: 佣金文字
        params__commisionStyle：？
        style: 组建风格，一般不修改，使用默认
        data: 组件内商品数据，使用接口调用商品数据，可酌情修改
        data__[num]__thumb:商品缩略图
        data__[num]__price: 价格，
        data__[num]__productprice: 划线价
        data__[num]__title: 商品标题
        data__[num]__sales: 售价
        data__[num]__gid: 商品id
        data__[num]__bargain: 开启讨价还价
        data__[num]__credit: 信用
        data__[num]__ctype: ?
        data__[num]__stock: 销量
        data__[num]__subtitle: 副标题
        data__[num]__commission: '' ？
        data__[num]__has_option: 是否多规格
        data__[num]__goodstype: ？
        data__[num]__type: 商品类型
        data__[num]__id: 商品id
        data__[num]__preloading: 预加载
        ==============================

        :param raw_content:
        :param kwargs:
        :return:
        """
        Infos = GoodsInfo(self.session, **self.kwargs)
        data = list()
        for goods_id in goods_ids:
            goods_infos = Infos.goods_info(goods_id)['data']
            item = dict(
                thumb=goods_infos['thumb'],
                price=goods_infos['price'],
                productprice=goods_infos['original_price'],
                title=goods_infos['title'],
                sales=goods_infos['sales'],
                gid=goods_id,
                bargin=0,
                credit=0,
                ctype=1,
                stock=goods_infos['stock'],
                subtitle=goods_infos['sub_title'],
                commission='',
                has_option=goods_infos['has_option'],
                goodstype=goods_infos['type'],
                type=goods_infos['type'],
                id=goods_infos['id'],
                preloading=False
            )
            data.append(copy.deepcopy(item))
            kwargs['data'] = data
        datas = exchange_params(raw_content, **kwargs)
        return datas

    def title_edit(self, raw_content: dict, **kwargs):
        """
        标题组件内容修改
        属性如下：
        ===============================
        params: 组件属性
        params__title: 标题
        params__icon: 图标
        params__subTitle: 查看更多
        params__linkurl: 跳转链接
        params__linkurl_name: 跳转链接名称
        params__secondTitle: 副标题
        params__righticon: 更多图标
        params__wxappid: 小程序appid
        params__titleweight: 文字大小
        params__showmore: 是否显示更多
        params__showTitle: 是否显示副标题
        style: 组件样式

        ===============================

        :param raw_content:
        :param kwargs:
        :return:
        """
        datas = exchange_params(raw_content, **kwargs)
        return datas

