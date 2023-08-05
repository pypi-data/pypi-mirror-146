# -*- coding: utf-8 -*-
"""
@Time : 2022/4/8 11:04 
@Author : YarnBlue 
@description : 
@File : goods_helper.py 
"""
from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.common.log import log
logger = log().log()


class GoodsHelper(RenRenApi):
    def goods_helper(self, **kwargs):
        """
        参数如下：
        ======================================
        url：需要抓取的商品链接
        type：商品类型，如：taobao
        category_id：商品分类
        goods_type：商品类型，0：实物，1：虚拟
        ======================================

        :param kwargs:
        :return:
        """
        rep = self.session.post(self.URL.goods_helper(), data=kwargs, **self.kwargs)
        if rep.json()['error'] == 1:
            return True
        else:
            logger.error(rep.text)
            return False
