# -*- coding: utf-8 -*-
"""
@Time : 2022/4/6 15:07 
@Author : YarnBlue 
@description : 
@File : test.py 
"""
import json
import random
import time

from RenRen_Shop.factory import Factory

def main(client):
    Fetcher = client.seckill.FetchSecKillList
    Fetcher.next(keyword='整点秒杀')
    seckill_list = Fetcher.result()
    seckill_ids = list()
    for each in seckill_list:
        seckill_ids.append(int(each['id']))
    diypage_info = client.diypage.page_info(1603, 10)
    diypage_content = json.loads(diypage_info['content'])
    seckill_contents = client.diypage.PageContent.fetch_content(diypage_content, 'seckill')
    for index, each in enumerate(seckill_contents):
        diypage_content[each[0]] = client.diypage.PageContent.secKill_edit(each[1],
                                                                           params__activityData__id=
                                                                           seckill_ids[-1 - index])
    diypage_info['content'] = diypage_content
    if client.diypage.page_eidt(**diypage_info):
        client.logger.info('Done!')


def seckill(client):
    start_dt = '2022-04-14 14:00:00'
    data = {
        'create_time[]': ['2022-03-13 00:00', '2022-04-11 00:00'],
        'category_id': 3396
    }
    client.app.MySecKill.add_mySecKill_with_filter_and_time(start_dt, **data)

def daily_seckill(client):
    """
    随机获取1/7的商品，加入每日特价组，按大促的价格，并编辑主页内容，实现每日特价功能
    :param client:
    :return:
    """
    goods_ids = client.goods.filter_goods(key='category__0__category_id', value=3396, judge='!=')
    goods_count = len(goods_ids)
    goods_ids = random.sample(goods_ids, int(round(goods_count / 7)))
    GroupFetcher = client.group.FetchGroupsList
    if client.group.update_groups('每日特价', *goods_ids):
        client.logger.info(f'{len(goods_ids)}个商品成功加入每日特价')

    start_time = '2022-04-14 00:00:00'
    duration = 24 * 3600
    if client.seckill.seckill_add_quick(*goods_ids, start_time=start_time, duration=duration, title='每日特价'):
        client.logger.info('每日特价秒杀活动新建成功')

if __name__ == '__main__':
    with Factory() as client:
        pass

