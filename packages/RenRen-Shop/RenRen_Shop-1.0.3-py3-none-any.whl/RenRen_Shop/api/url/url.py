# -*- coding: utf-8 -*-
"""
@Time : 2022/3/30 11:11 
@Author : YarnBlue 
@description : 
@File : url.py 
"""


class URL:
    def __init__(self):
        self.host = 'https://rr.hanchenshop.com'

    def get_session_id(self):
        return self.host + '/account/index/get-session-id'

    def login(self):
        return self.host + '/account/login/submit'

    def logout(self):
        return self.host + '/account/logout'

    def upload_img(self):
        return self.host + f'/shop/api/utility/attachment/list/upload'

    def add_album(self):
        return self.host + f'/shop/api/utility/attachment/group/add'

    def add_goods(self):
        return self.host + f'/shop/api/goods/index/add'

    def edit_goods(self):
        return self.host + f'/shop/api/goods/index/edit'

    def edit_goods_quick(self):
        return self.host + '/shop/api/goods/index/property'

    def edit_goods_sku(self):
        return self.host + '/shop/api/goods/operation/set-price-and-stock'

    def category_list(self):
        return self.host + f'/shop/api/goods/category/get-list'

    def set_category(self):
        return self.host + '/shop/api/goods/operation/set-category'

    def goods_info(self):
        return self.host + '/shop/api/goods/index/get'

    def goods_list(self):
        return self.host + '/shop/api/goods/index/list'

    def add_group(self):
        return self.host + '/shop/api/goods/group/create'

    def group_list(self):
        return self.host + '/shop/api/goods/group/get-list'

    def groups_info(self):
        return self.host + '/shop/api/goods/group/get-one'

    def update_groups(self):
        return self.host + '/shop/api/goods/group/update'

    def log_list(self):
        return self.host + '/shop/api/sysset/log/list'

    def log_info(self):
        return self.host + '/shop/api/sysset/log/detail'

    def shop_index(self):
        return self.host + '/account/shop/list/index'

    def member_list(self):
        return self.host + '/shop/api/member/list'

    def member_level(self):
        return self.host + '/shop/api/member/level'

    def member_infos(self):
        return self.host + '/shop/api/member/detail'

    def agent_list(self):
        return self.host + '/shop/api/apps/commission/agent'

    def commission_goods_list(self):
        return self.host + '/shop/api/apps/commission/goods/list'

    def commission_cancel(self):
        return self.host + '/shop/api/apps/commission/goods/cancel'

    def change_agent(self):
        return self.host + '/shop/api/apps/commission/agent/change-agent'

    def seckill_add(self):
        return self.host + '/shop/api/apps/seckill/index/add'

    def seckill_edit(self):
        return self.host + '/shop/api/apps/seckill/index/edit'

    def seckill_infos(self):
        return self.host + '/shop/api/apps/seckill/index/detail'

    def seckill_delete(self):
        return self.host + '/shop/api/apps/seckill/index/delete'

    def seckill_list(self):
        return self.host + '/shop/api/apps/seckill/index/list'

    def page_edit(self):
        return self.host + '/shop/api/apps/diypage/page/list/edit'

    def goods_helper(self):
        return self.host + '/shop/api/apps/goodsHelper'


