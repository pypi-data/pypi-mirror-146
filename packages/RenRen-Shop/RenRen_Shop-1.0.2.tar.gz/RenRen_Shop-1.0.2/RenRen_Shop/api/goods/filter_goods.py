# -*- coding: utf-8 -*-
"""
@Time : 2022/4/8 23:01 
@Author : YarnBlue 
@description : 根据给定的限定条件，筛选符合要求的商品
@File : filter_goods.py 
"""
import time

from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.api.goods.fetch_goods_list import FetchGoodsList
from RenRen_Shop.common.log import log
from RenRen_Shop.api.goods.goods_info import GoodsInfo
from RenRen_Shop.configs.configs import DELAY

logger = log().log()


class FilterGoods(RenRenApi):
    @staticmethod
    def __filter_params__(data, key, value, judge, split='__'):
        """
        支持多级嵌套筛选，默认以__标识上下级关系，__0__中0表示当前为list
        例如 ：“key1__2__key2”
        表示：原数据为dict下嵌套list,list内为dict,用于goods_options筛选

        :param judge: 对比方法，取值可为 '=', '<', '>', '><'
        :param value: 对比的内容
        :param key: 要判断的key
        :param data: 要判断的原数据
        :param split:
        :param kwargs:
        :return:
        """
        if not isinstance(value, list) and not isinstance(value, dict):
            value = str(value)
        key_split = key.split(split)
        if key_split[0] not in data.keys():
            return False
        level_count = len(key_split)  # 字典键值对级数
        if level_count == 1:
            if judge == '=':
                return True if data[key_split[0]] == value else False
            elif judge == '!=':
                return True if data[key_split[0]] != value else False
            elif judge == '<':
                return True if float(data[key_split[0]]) < float(value) else False
            elif judge == '>':
                return True if float(data[key_split[0]]) > float(value) else False
            elif judge == '><':
                return True if float(value[0]) < float(data[key_split[0]]) < float(value[1]) else False
            else:
                logger.error('请输入有效的判定方式')
                raise Exception('JudgeTypeError')
        elif level_count == 2:
            if judge == '=':
                return True if data[key_split[0]][key_split[1]] == value else False
            elif judge == '!=':
                return True if data[key_split[0]][key_split[1]] != value else False
            elif judge == '<':
                return True if float(data[key_split[0]][key_split[1]]) < float(value) else False
            elif judge == '>':
                return True if float(data[key_split[0]][key_split[1]]) > float(value) else False
            elif judge == '><':
                return True if float(value[0]) < float(data[key_split[0]][key_split[1]]) < float(value[1]) else False
            else:
                logger.error('请输入有效的判定方式')
                raise Exception('JudgeTypeError')
        elif level_count == 3:
            if key_split[1].isdigit():
                for index, each in enumerate(data[key_split[0]]):
                    if judge == '=':
                        if each[key_split[2]] == value:
                            return True
                        else:
                            continue
                    elif judge == '!=':
                        if each[key_split[2]] != value:
                            return True
                        else:
                            continue
                    elif judge == '<':
                        if float(each[key_split[2]]) < float(value):
                            return True
                        else:
                            continue
                    elif judge == '>':
                        if float(each[key_split[2]]) > float(value):
                            return True
                        else:
                            continue
                    elif judge == '><':
                        if float(value[0]) < float(each[key_split[2]]) < float(value[1]):
                            return True
                        else:
                            continue
                    else:
                        logger.error('请输入有效的判定方式')
                        raise Exception('JudgeTypeError')
                return False
        else:
            logger.error('参数级数超过3')
            raise Exception('ParamsLevelError')

    def filter_goods(self, key, value, judge, split='__', return_type=0):
        """
        支持多级嵌套筛选，默认以__标识上下级关系，__0__中0表示当前为list
        例如 ：“key1__2__key2”
        表示：原数据为dict下嵌套list,list内为dict,用于goods_options筛选

        支持的key如下：
        ====================
        status: 上下架  0:下架; 1:上架;
        title: 标题
        sub_title: 副标题
        short_title: 短标题
        sub_shop_id: 子门店
        type: 商品类型 0：实体 1：虚拟
        thumb: 首图
        thumb_all: 轮播图 list
        stock: 库存
        sales: 虚拟销量
        real_sales: 真实销量
        price: 价格
        has_option: 是否多规格
        options: 规格，list[dict[str, any]]
        options__[num]__title: sku名称
        options__[num]__thumb: sku缩略图
        options__[num]__price: sku售价
        options__[num]__cost_price: sku成本
        options__[num]__original_price: sku划线价
        options__[num]__stock: sku库存
        options__[num]__stock_warning: sku库存预警
        options__[num]__sales: sku销量
        options__[num]__weight: sku重量
        content: 详情图
        dispatch_express: 是否开启快递配送
        dispatch_type: 物流方式 0：包邮 1：默认模板 2：统一运费
        dispatch_id: 快递模板ID
        dispatch_price: 邮费， 统一运费时有效
        dispatch_verify: 是否开启核销,开启后需指定核销点
        is_all_verify: 是否选择所有核销点
        dispatch_verify_point_id: 核销点ID,列表
        dispatch_verify_point_list: 核销点信息，与上一条成对存在，列表
        weight: 重量
        ext_field__invoice: 发票
        ext_field__show_sales: 是否展示销量
        ext_field__show_stock: 是否展示库存
        ext_field__exchange: 换货
        ext_field__return: 退货
        ext_field__refund: 退货退款
        ext_field__is_delivery_pay: 货到付款
        ext_field__auto_putaway: 自动上架
        ext_field__putaway_time: 上架时间，格式："0NaN-NaN-NaN NaN:NaN:NaN",
        ext_field__offaway_time: 下架时间，格式："0NaN-NaN-NaN NaN:NaN:NaN",
        ext_field__option_type: 规格样式，0：纯文本；1：缩略小图；2：缩略大图
        ext_field__single_max_buy: 单次最大购买
        ext_field__single_max_buy: 单次最少购买
        ext_field__max_buy: 总共最大购买
        ext_field__buy_limit:是否开启购买权限
        ext_field__note: 商品备注
        is_recommand: 是否推荐 0或1
        is_hot: 是否热卖
        is_new: 是否新品
        params: 参数，list,格式如：[{'key': '产地', 'value': '大陆'},{},...]
        category__category_id: 分类ID, 需与category_id一同修改
        category_id: 分类ID, 需与category__category_id一同修改
        category__sub_shop_id: 所属子店铺ID
        give_credit_status: 是否赠送积分
        give_credit_num: 赠送积分数量
        is_commission: 是否分销
        browse_level_perm: 会员查看权限
        browse_tag_perm: 标签组查看权限
        buy_level_perm: 会员购买权限
        buy_tag_perm: 标签组购买权限
        form_status: 是否插入表单
        form_id: 表单ID
        subShopCategory: 子店铺商品分类
        group: 商品组id
        label: 商品标签，list,需与label_id一同修改
        label_id: 商品标签,需与label一同修改
        perm_data__browse__member_level: 浏览权限会员等级id, list
        perm_data__browse__member_tag: 浏览权限会员标签id, list
        perm_data__buy__member_level: 购买权限会员等级id, list
        perm_data__buy__member_tag: 购买权限会员标签id, list
        browse_level_perm: "0",是否开启会员等级浏览权限
        browse_tag_perm: "0",是否开启会员标签组浏览权限
        buy_level_perm: "0",是否开启会员等级购买权限
        buy_tag_perm: "0",是否开启会员标签组购买权限
        ====================

        :param return_type: 返回的数据形式，0:goods_ids, 1:goods_infos
        :param judge: 对比方法，取值可为 '=', '<', '>', '><', '!='
        :param value: 对比的内容
        :param key: 要判断的key
        :param split:
        :return:
        """
        goods_ids = list()
        goods_infos = list()
        fetcher = FetchGoodsList(self.session, **self.kwargs)
        get_info = GoodsInfo(self.session, **self.kwargs)
        while fetcher.next():
            for result in fetcher.result():
                if key.split(split)[0] not in result:
                    goods_info = get_info.goods_info(result['id'])['data']
                    if self.__filter_params__(goods_info, key, value, judge, split):
                        goods_ids.append(result['id'])
                        goods_infos.append(goods_info)
                    time.sleep(DELAY)  # 防止ip封禁
                else:
                    if self.__filter_params__(result, key, value, judge, split):
                        goods_ids.append(result['id'])
                        goods_infos.append(result)
        if return_type:
            return goods_infos
        else:
            return goods_ids
        