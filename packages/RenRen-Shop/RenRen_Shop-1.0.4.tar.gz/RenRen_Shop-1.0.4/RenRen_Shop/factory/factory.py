#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/3 21:10
# @Author  : YarnBlue
# @Site    : api常用功能集合
# @File    : factory.py
# @Software: PyCharm
import getpass
import time
from typing import TypeVar

import requests

from RenRen_Shop.api.category import *
from RenRen_Shop.api.url.url import URL
from RenRen_Shop.api.goods import *
from RenRen_Shop.api.group import *
from RenRen_Shop.api.log import *
from RenRen_Shop.api.photo_album import *
from RenRen_Shop.api.app import *
from RenRen_Shop.api.uploader import *
from RenRen_Shop.common import *
from RenRen_Shop.api.member import *
from RenRen_Shop.api.commission import *
from RenRen_Shop.api.application import *


Myshop = TypeVar('Myshop', int, str)


class Factory:
    logger = log().logger

    def __init__(self, username=None, password=None, host=None, **kwargs):
        if not username:
            username = input('请输入你的用户名：\n')
        if not password:
            password = input('请输入您的密码：\n')
        self.username = username
        self.password = password
        self.kwargs = kwargs
        self.session = requests.Session()
        self.URL = URL()
        if host:
            self.URL.host = host
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/100.0.4896.60 Safari/537.36',
            'client-type': '50'
        }
        self.session_id = None
        self.cookie = None
        self.shop_id = None
        self.session.headers = self.headers
        self.request_session_id()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__logout():
            self.logger.info('账号登出成功')
        else:
            self.logger.error('账号登出失败')

    def __enter__(self):
        self.logger.info('账户初始化')
        if self.__login():
            self.logger.info('账户登录成功')
        else:
            self.logger.error('账户登录失败，请检查账号密码')
        self.__get_shop_id()
        self.logger.info('获取该账户管理的店铺')
        self.__shop_init(self.shop_ids[0])
        self.logger.info('店铺初始化，默认获取第一个店铺的管理权，若有多个店铺，可通过self.switch_shop()进行管理权切换')
        return self

    def request_session_id(self):
        rep = self.session.get(self.URL.get_session_id(), **self.kwargs)
        self.session_id = rep.json()['session_id']
        self.headers['session-id'] = self.session_id
        self.session.headers = self.headers

    def __login(self):
        data = {
            'username': self.username,
            'password': self.password
        }
        rep = self.session.post(self.URL.login(), data=data, **self.kwargs)
        if rep.json()['error'] == 0:
            return True
        else:
            self.logger.error(rep.text)
            return False

    def __get_shop_id(self):
        t = int(time.time())
        rep = self.session.get(self.URL.shop_index(), params={'t': t})
        shop_list = rep.json()['list']
        self.shop = {}
        self.shop_ids = []
        self.shop_names = []
        for shop in shop_list:
            self.shop_ids.append(int(shop['shop_id']))
            self.shop_names.append(shop['name'])
            self.shop[shop['shop_id']] = shop['name']

    def __logout(self):
        rep = requests.post(self.URL.logout(), headers=self.headers, **self.kwargs)
        if rep.json()['error'] == 0:
            return True
        else:
            self.logger.error(rep.text)
            return False

    def switch_shop(self, myshop: Myshop):
        """
        切换需要管理的店铺，支持店铺ID或店铺名切换

        :param myshop:
        :return:
        """
        self.__shop_init(myshop)

    def __shop_init(self, myshop: Myshop):
        """
        店铺初始化，默认管理第一个店铺

        :param myshop:
        :return:
        """
        if isinstance(myshop, int):
            self.shop_id = myshop
            self.shop_name = self.shop[str(myshop)]
        if isinstance(myshop, str):
            self.shop_name = myshop
            self.shop_id = self.shop_ids[self.shop_names.index(myshop)]
        self.headers['shop-id'] = str(self.shop_id)
        self.common = self.__Common()
        self.category = self.__Category(self.session, **self.kwargs)
        self.goods = self.__Goods(self.session, **self.kwargs)
        self.group = self.__Groups(self.session, self.shop_id, **self.kwargs)
        self.log = self.__Log(self.session, **self.kwargs)
        self.app = self.__App(self.session, **self.kwargs)
        self.upload = self.__Upload(self.session, **self.kwargs)
        self.photo_album = self.__PhotoAlbum(self.session, **self.kwargs)
        self.member = self.__Member(self.session, **self.kwargs)
        self.commission = self.__Commission(self.session, **self.kwargs)
        self.seckill = self.__Seckill(self.session, **self.kwargs)

    class __Common:
        def __init__(self):
            self.Time2Str = time_2_str
            self.Str2Time = str_2_time

    class __Category:
        def __init__(self, session, **kwargs):
            """
            商品分类功能模块

            :param session:
            :param kwargs:
            """
            self.session = session
            self.kwargs = kwargs
            self.CategoryList = CategoryList(self.session, **self.kwargs)
            self.category_list = self.CategoryList.category_list
            self.SetCategory = SetCategory(self.session, **self.kwargs)
            self.set_category = self.SetCategory.set_category

    class __Goods:
        def __init__(self, session, **kwargs):
            """
            商品功能模块

            :param session:
            """
            self.session = session
            self.kwargs = kwargs
            self.AddGoods = AddGoods(self.session, **self.kwargs)
            self.add_goods = self.AddGoods.add_goods
            self.EditGoods = EditGoods(self.session, **self.kwargs)
            self.edit_goods = self.EditGoods.edit_goods
            self.edit_goods_quick = self.EditGoods.edit_goods_quick
            self.edit_goods_sku = self.EditGoods.edit_goods_sku
            self.FetchGoods = FetchGoodsList(self.session, **self.kwargs)
            self.GoodsInfo = GoodsInfo(self.session, **self.kwargs)
            self.goods_info = self.GoodsInfo.goods_info
            self.FetchGoodsIdsList = FetchGoodsIdList(self.session, **self.kwargs)
            self.fetch_goodsIds_list = self.FetchGoodsIdsList.fetch_goodsId_list
            self.FilterGoods = FilterGoods(self.session, **self.kwargs)
            self.filter_goods = self.FilterGoods.filter_goods
            self.GoodsKeyValue = GoodsKeyValue(self.session, **self.kwargs)
            self.goods_key_value = self.GoodsKeyValue.goods_key_value
            self.GoodsCopy = GoodsCopy(self.session, **self.kwargs)
            self.goods_copy = self.GoodsCopy.copy_goods

    class __Groups:
        def __init__(self, session, shop_id, **kwargs):
            """
            商品分组功能模块

            :param session:
            """
            self.session = session
            self.shop_id = shop_id
            self.kwargs = kwargs
            self.AddGroup = AddGroup(self.session, **self.kwargs)
            self.add_group = self.AddGroup.add_group
            self.FetchGroupsList = FetchGroupsList(self.session, **self.kwargs)
            self.GroupsInfo = GroupsInfo(self.session, **self.kwargs)
            self.groups_info = self.GroupsInfo.groups_info
            self.UpdateGroups = UpdateGroups(self.session, self.shop_id, **kwargs)
            self.update_groups = self.UpdateGroups.update_groups
            self.add_goods_to_groups = self.UpdateGroups.add_goods_to_groups

    class __Log:
        def __init__(self, session, **kwargs):
            """
            店铺操作日志功能版块

            :param session:
            :param kwargs:
            """
            self.session = session
            self.kwargs = kwargs
            self.FetchLogList = FetchLogList(self.session, **self.kwargs)
            self.LogInfo = LogInfo(self.session, **self.kwargs)

    class __PhotoAlbum:
        def __init__(self, session, **kwargs):
            """
            相册功能模块

            """
            self.session = session
            self.kwargs = kwargs
            self.AddAlbum = AddAlbum(self.session, **self.kwargs)

    class __Upload:
        def __init__(self, session, **kwargs):
            """
            文件上传功能模块

            :param session:
            :param kwargs:
            """
            self.session = session
            self.kwargs = kwargs
            self.ImgUploader = ImgUploader(self.session, **self.kwargs)

    class __App:
        def __init__(self, session, **kwargs):
            """
            常用应用功能模块

            :param session:
            :param kwargs:
            """
            self.session = session
            self.kwargs = kwargs
            self.MassUpdateGoods = MassUpdateGoods(self.session, **self.kwargs)
            self.MySecKill = MySecKill(self.session, **self.kwargs)

    class __Member:
        def __init__(self, session, **kwargs):
            """
            会员功能模块

            :param session:
            :param keyword:
            """
            self.session = session
            self.kwargs = kwargs
            self.FetchMemberList = FetchMemberList(self.session, **self.kwargs)
            self.MemberLevel = MemberLevel(self.session, **self.kwargs)
            self.member_level = self.MemberLevel.member_levels_list
            self.MemberInofs = Memberinfos(self.session, **self.kwargs)
            self.member_infos = self.MemberInofs.memer_infos

    class __Commission:
        def __init__(self, session, **kwargs):
            """
            分销功能模块

            :param session:
            :param kwargs:
            """
            self.session = session
            self.kwargs = kwargs
            self.FetchAgentsList = FetchAgentsList(self.session, **self.kwargs)
            self.ChangeAgent = ChangeAgent(self.session, **self.kwargs)
            self.change_agent = self.ChangeAgent.change_agent
            self.GoodsCommission = GoodsCommission(self.session, **self.kwargs)
            self.cancel_goods_commission = self.GoodsCommission.cancel_commission
            self.add_goods_commission = self.GoodsCommission.add_commission

    class __Seckill:
        def __init__(self, session, **kwargs):
            """
            秒杀功能模块

            :param session:
            :param kwargs:
            """
            self.session = session
            self.kwargs = kwargs
            self.SeckillAdd = SecKillAdd(self.session, **self.kwargs)
            self.seckill_add = self.SeckillAdd.add
            self.SeckillEdit = SecKillEdit(self.session, **self.kwargs)
            self.seckill_edit = self.SeckillEdit.edit
            self.SeckillDelete = SecKillDelete(self.session, **self.kwargs)
            self.seckill_delete = self.SeckillDelete.seckill_delete
            self.SecKillInfos = SecKillinfos(self.session, **self.kwargs)
            self.seckill_infos = self.SecKillInfos.infos
            self.FetchSecKillList = FetchSecKillList(self.session, **self.kwargs)
