# -*- coding: utf-8 -*-
"""
@Time : 2022/4/11 9:30 
@Author : YarnBlue 
@description : 一键复制商品
@File : goods_copy.py 
"""
import json
import os.path
import random
import time

from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.api.goods.add_goods import AddGoods
from RenRen_Shop.common import exchange_params, template, set_spec_id, set_child_spec_id


class GoodsCopy(RenRenApi):
    """
    一键复制指定商品，并按需修改指定属性
    """
    def good_info_copy(self, goods_id):
        params = dict(id=goods_id, flag='copy')
        goods_infos = self.session.get(self.URL.goods_info(), params=params, **self.kwargs).json()['data']
        return goods_infos

    def copy_goods(self, goods_id, **kwargs):
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
        form_status: 是否插入表单
        form_id: 表单ID
        subShopCategory: 子店铺商品分类
        group: 商品组id
        label: 商品标签，list,需与label_id一同修改
        label_id: 商品标签,需与label一同修改
        browse_level_perm_ids: 浏览权限会员等级id, list
        browse_tag_perm_ids: 浏览权限会员标签id, list
        buy_level_perm_ids: 购买权限会员等级id, list
        buy_tag_perm_ids: 购买权限会员标签id, list
        browse_level_perm: "0",是否开启会员等级浏览权限
        browse_tag_perm: "0",是否开启会员标签组浏览权限
        buy_level_perm: "0",是否开启会员等级购买权限
        buy_tag_perm: "0",是否开启会员标签组购买权限
        ====================

        :param goods_id:
        :param kwargs:
        :return:
        """
        goods_infos = self.good_info_copy(goods_id)
        perm_data = goods_infos.pop('perm_data')
        goods_infos['browse_tag_perm_ids'] = perm_data['browse']['member_tag'] if perm_data['browse'][
            'member_tag'] else ''
        goods_infos['browse_level_perm_ids'] = perm_data['browse']['member_level'] if perm_data['browse'][
            'member_level'] else ''
        goods_infos['buy_tag_perm_ids'] = perm_data['buy']['member_tag'] if perm_data['buy'][
            'member_tag'] else ''
        goods_infos['buy_level_perm_ids'] = perm_data['buy']['member_level'] if perm_data['buy'][
            'member_level'] else ''
        goods_infos.pop('id')
        goods_infos = exchange_params(goods_infos, **kwargs)
        if int(goods_infos['has_option']):
            spec = goods_infos.pop('spec')
            options = goods_infos.pop('options')
            ids = list()  # 用于存储规格属性id
            for each in spec:  # 对spec数据中的规格及规格项生成新的id,并进行替换
                title = each['title']
                id = each['id']
                res = set_spec_id(title, id)
                ids.append(res)
                each['id'] = res['id']
                for item in each['items']:
                    item_id = item['id']
                    item_title = item['title']
                    item_res = set_child_spec_id(item_title, item_id, id)
                    item['id'] = item_res['id']
                    item['spec_id'] = res['id']
                    ids.append(item_res)
                    time.sleep(0.01)
            for index, option in enumerate(options):
                option.pop('id')
                option.pop('shop_id')
                option.pop('sub_shop_id')
                option.pop('goods_id')
                option['tmpid'] = f'_tmpID_{index}'
                option['specs'] = option['specs'].split(',')
                for i, each_spec in enumerate(option['specs']):
                    for every in ids:
                        if every['type'] == 'childSpec':
                            if each_spec == every['raw_id']:
                                option['specs'][i] = every['id']
                                break
        else:
            spec = None
            options = None
        goods_commission = template('goods_commission', os.path.dirname(__file__))
        member_level_discount = dict() if 'member_level_discount' not in goods_infos.keys() \
            else goods_infos.pop('member_level_discount')
        adder = AddGoods(self.session, **self.kwargs)
        goods_infos['buy_button_settings'] = template('buy_button_settings', os.path.dirname(__file__))
        if adder.add_goods(goods=goods_infos,
                           spec=spec,
                           options=options,
                           goods_commission=goods_commission,
                           member_level_discount=member_level_discount):
            return True
        else:
            return False

