# README
***
|   author    |     YarnBlue      |
|:-----------:|:-----------------:|
| description |     人人商城后台管理      |
|   version   |       1.0.4       |
|   email   | zqb090325@126.com |

## 说明
该项目基于人人商城V5

用于人人商城后台管理，提升商城运营效率，突破平台限制，实现更丰富的商城运营手段

## 版本更新计划
- [x] 适配各代理商
- [x] 商品全属性编辑
- [x] 商品全属性筛选
- [x] 商品采集模块
- [ ] 页面编辑
- [ ] 评论模块
- [ ] 应用模块
- [ ] 待补充...

## 安装
pip install RenRen_Shop

## 主要结构
<details><summary>goods：商品模块</summary>
goods_info : 商品信息<br>
add_goods : 增加商品<br>
edit_goods : 编辑商品<br>
FetchGoods : 获取商品列表<br>
fetch_goodsId_list: 筛选商品id列表<br>
filter_goods: 全属性筛选商品<br>
goods_key_value: 商品属性值<br>
goods_copy: 商品一键复制（支持属性修改）
</details>
<br>
<details><summary>category：商品分类模块</summary>
category_list : 商品分类<br>
set_category: 批量设置分类
</details>
<br>
<details><summary>group：商品分组模块</summary>
groups_info : 商品分组信息<br>
FetchGroups : 获取商品分组列表<br>
add_group : 增加商品分组<br>
update_group : 更新商品分组
</details>
<br>
<details><summary>log：操作日志模块</summary>
log_info : 账户操作日志信息<br>
FetchLogList : 获取操作日志列表<br>
</details>
<br>
<details><summary>upload：上传模块</summary>
img_uploader : 上传图片<br>
</details>
<br>
<details><summary>photo_album：图册模块</summary>
add_album : 增加图片分组<br>
</details>
<br>
<details><summary>commission：分销模块</summary>
change_agent : 更换分销上下级<br>
FetchAgentList: 分销商列表<br>
FetchGoodsCommissionList: 分销商品列表<br>
cancel_goods_commission: 商品取消分销<br>
add_goods_commission: 商品开启分销
</details>
<br>
<details><summary>seckill：秒杀模块</summary>
seckill_add : 新增秒杀活动<br>
seckill_delete: 删除秒杀活动<br>
seckill_info: 秒杀活动信息<br>
seckill_edit: 编辑秒杀活动<br>
FetchSecKillList: 秒杀活动列表
</details>
<br>
<details><summary>diypage：页面模块</summary>
page_edit : 页面编辑<br>
page_info: 页面信息
</details>

## 使用
填入账号密码，登录后获取操作权，结束后自动登出<br>
例如：

```python
from RenRen_Shop.factory import Factory

with Factory(username='你的账号', password='你的密码', host='代理商主机地址') as client:
    print(client.shop_ids)  # 拥有管理权的店铺ID列表
    print(client.shop_names)  # 拥有管理权的店铺列表
    print(client.shop_id)  # 当前管理的店铺ID,初始化默认使用第一个店铺
    print(client.shop_name)  # 当前管理的店铺名
    client.switch_shop(myshop='你的店铺id或者店铺名')  # 店铺切换
    client.goods.goods_info(id=2658)  # 商品2658的信息
    goods = client.goods.FetchGoods
    goods.next(status=0)  # 增加筛选条件
    print(goods.result()) # 获取商品列表，翻页调用next()
```
以下代码实现将商品10844的第一个sku售价调整为70元
```python
from RenRen_Shop.factory import Factory

if __name__ == '__main__':
    with Factory(username='', password='') as client:
        if client.goods.edit_goods(10844, options__0__price=70):
            client.logger.info('Done!')
```

批量管理实例：
```python
from RenRen_Shop.factory import Factory

with Factory(username='', password='') as client:
    goods = client.goods.FetchGoods
    while goods.next(keywords='零食'):
        for result in goods.result():
            id = result['id']
            client.goods.EditGoods.edit_goods(id=id, is_commission=1, stock=100)

```
代码实现将所有标题中包含【零食】的商品，统一开启分销，设置库存为100

当然也可以使用内置方法MassUpdateGoods:
```python
from RenRen_Shop.factory import Factory

with Factory(username='', password='') as client:
    goods = [1254, 1255, 1256] # 你需要修改的商品id
    kwargs = {
        'stock': 100,
        'is_commission': 0,
        'status': 0
    }  # 你需要修改的商品属性
    client.app.MassUpdateGoods.mash_update_goods(*goods, **kwargs)
```
## 结语
基于本项目，可实现多种批量管理功能，例如批量导出商品信息，批量修改商品信息，批量上传商品，批量对商品进行商品分组；在实际生产过程，批量化操作多属于不可逆过程，请做好数据备份，本项目对生产问题概不负责，请谨慎操作。
