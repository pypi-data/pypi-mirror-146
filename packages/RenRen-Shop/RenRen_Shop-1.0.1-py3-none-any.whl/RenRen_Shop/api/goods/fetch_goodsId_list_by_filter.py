# -*- coding: utf-8 -*-
"""
@Time : 2022/4/7 10:50 
@Author : YarnBlue 
@description : 
@File : fetch_goodsId_list_by_filter.py 
"""
from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.api.goods.fetch_goods_list import FetchGoodsList


class FetchGoodsIdList(RenRenApi):
    def fetch_goodsId_list(self, **kwargs):
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
        fetcher = FetchGoodsList(self.session, **self.kwargs)
        goods_ids = []
        while fetcher.next(**kwargs):
            for result in fetcher.result():
                id = result['id']
                goods_ids.append(id)
        return goods_ids
