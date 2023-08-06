# -*- coding: utf-8 -*-
"""
@Time : 2022/4/1 15:00 
@Author : YarnBlue 
@description : 
@File : edit_goods.py 
"""
import json
import random
import time


from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.api.goods.add_goods import AddGoods
from RenRen_Shop.api.goods.goods_info import GoodsInfo
from RenRen_Shop.common.log import log
from RenRen_Shop.common.common_fuc import exchange_params
logger = log().logger


class EditGoods(RenRenApi):
    @staticmethod
    def form_data(infos: dict) -> dict:
        """
        获取到的商品数据，重组数据结构，用于编辑用

        :param infos:
        :return:
        """
        goods_commission = AddGoods.template('goods_commission')
        if int(infos['has_option']):
            try:
                options = infos.pop('options')
                for option in options:
                    option['specs'] = option['specs'].split(',')
                    option['tmpid'] = option['id']
            except Exception as e:
                logger.error(f'options错误，{e}')
                options = None
            try:
                spec = infos.pop('spec')
                for each in spec:
                    items = each['items']
                    for item in items:
                        item['specId'] = item['spec_id']
                        item['_sortId'] = f'{int(time.time()*1000)}_{random.random()}'
            except Exception as e:
                logger.error(f'spec错误，{e}')
                spec = None
        else:
            options = None
            spec = None
        data = {
            'options': options,
            'spec': spec,
            'member_level_discount': {} if 'member_level_discount' not in infos.keys() else infos.pop('member_level_discount'),
            'goods': infos,
            'goods_commission': goods_commission
        }
        return data

    def __edit_goods__(self,
                       goods: dict,  # 商品属性
                       spec: list,  # 多规格
                       options: list,  # 多规格定价
                       goods_commission: dict,  # 分销设置
                       member_level_discount: dict  # 会员折扣信息
                       ) -> bool:
        data = {
            'goods': json.dumps(goods),
            'spec': json.dumps(spec),
            'options': json.dumps(options),
            'goods_commission': json.dumps(goods_commission),
            'member_level_discount': json.dumps(member_level_discount)
        }
        rep = self.session.post(self.URL.edit_goods(), data=data)
        if rep.json()['error'] == 0:
            return True
        else:
            return False

    def edit_goods(self, id, **kwargs):
        """
        多级属性以__标明上下级关系
        常见修改的属性如下：
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

        :param id:
        :param kwargs:
        :return:
        """
        get_goods_info = GoodsInfo(self.session,
                                   **self.kwargs)
        goods_infos = get_goods_info.goods_info(id)['data']
        # for index, (key, value) in enumerate(kwargs.items()):
        #     goods_infos[key] = value
        goods_infos = exchange_params(goods_infos, **kwargs)
        data = self.form_data(goods_infos)
        rep = self.__edit_goods__(data['goods'],
                                  data['spec'],
                                  data['options'],
                                  data['goods_commission'],
                                  data['member_level_discount'])
        if rep:
            return True
        else:
            return False

    def edit_goods_quick(self, goods_id, field, value):
        """
        商城自带简单快捷商品属性修改
        ====================
        id: goods_id
        field: 修改部分，可选值：title, is_recommand, is_hot, is_new
        value: 修改的内容
        ====================

        :return:
        """
        data = {
            'id': goods_id,
            'field': field,
            'value': value
        }
        rep = self.session.post(self.URL.edit_goods_quick(), data=data, **self.kwargs)
        return True if rep.json()['error'] == 0 else False

    def edit_goods_sku(self, **kwargs):
        """
        商城自带商品sku价格库存修改
        参数如下：
        ===============================
        goods_id: 商品id
        options[0][id]: 第一个sku的id
        options[0][price]: 第一个sku的价格
        options[0][stock]: 第一个sku的库存
        options[1][id]: 第二个sku的id
        options[1][price]: 第二个sku的价格
        options[1][stock]: 第二个sku的库存
        ......
        (其余依次类推，需全部囊括)
        ===============================

        :return:
        """
        rep = self.session.post(self.URL.edit_goods_sku(), data=kwargs, **self.kwargs)
        return True if rep.json()['error'] == 0 else False


