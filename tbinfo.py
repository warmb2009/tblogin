# -*- coding:utf-8 -*-

import re
from tbk.TbkSeniorAPI import *
from tbk.loggingset import create_logger
import requests
import json

Loger = create_logger()
post_url = 'http://127.0.0.1:8080/tkapis/'
create_url = 'http://127.0.0.1:8080/tkapis/create/'
update_url = 'http://127.0.0.1:8080/tkapis/update/'
tbk = TBK()


# 上传数据
def post_info(url, dic, item_id):
    # 先根据item_id, 查看数据库是否有数据，　如果有数据，则更新数据，　如果没有，则创建数据
    request_url = url + item_id + '/'
    r = requests.get(request_url)
    Loger.info('测试　是否存在ｉｔｅｍ．．．．．．．')
    Loger.info(r.text)
    request_info = r.text

    if request_info == '[]':  # 不存在Item
        Loger.info('创建数据')
        switch_url = create_url
        r = requests.post(switch_url, data=dic)
        Loger.info(r.text)
    else:
        Loger.info('更新数据')
        switch_url = update_url + item_id + '/'
        r = requests.put(switch_url, data=dic)
        Loger.info(r.text)

# 正则表达式获取券链接和商品链接
def get_commodity_info(text, pid):
    # 处理获取的信息
    Loger.info(text)
    match_obj = re.findall(r'(.*)领[券|劵](.*)抢购(.*https?://[ -~]+.*id=\d{11,12})(.*)', text)
    Loger.info('1:')
    Loger.info(match_obj)

    if not match_obj:
        match_obj = re.findall(r'(.*)领[券|劵](.*)抢购(.*https?://[ -~]+[A-Za_z])(.*)', text)
        Loger.info('2')
        Loger.info(match_obj)
        if not match_obj:
            match_obj = re.findall(r'(.*)领取(.*)抢购(.*https?://[ -~]+[A-Za_z])(.*)', text)
            Loger.info('3')
            Loger.info(match_obj)
            if not match_obj:
                return False
        else:
            return False

    link = match_obj[0]

    title = link[0].strip()
    coupon_url = link[1].strip()[1:]  # 优惠券链接
    commodity_url = link[2].strip()[1:]  # 商品链接
    content = link[3].strip()
        
    # 测试商品链接并转换
    commodity_url = test_commodity(commodity_url)
        
    # 获取推广链接及商品图片 模拟登陆
    #    promotion_text, img_src = get(commodity)

    # 获取item_id
    item_id = tbk.get_item_id(commodity_url)

    # 将商品加入定向计划 调用全局变量, 传入商品url
    base_url, activity_id = tbk.convert_url(coupon_url, item_id, pid)
    my_coupon_url = base_url + 'activityId=' + activity_id + '&pid=' + pid + '&itemId=' + item_id + '&af=1'

    # 获取优惠券详细信息
    my_coupon_info = tbk.get_coupon_info(item_id, activity_id)

    # 通过api获取商品信息
    commodity_info = tbk.get_commodity_info(item_id)

    # 淘口令
    model = tbk.get_tpwd(title, my_coupon_url)

    Loger.info('---------------------------')
    Loger.info(commodity_info)
    Loger.info('---------------------------')
    dic = dict()
    dic['item_id'] = item_id  # item id
    dic['item_title'] = title  # 标题
    dic['item_reserve_price'] = commodity_info['reserve_price']  # 原始价格［没有进行任何活动的价格］
    dic['item_price'] = commodity_info['zk_final_price']  # 活动后的价格
    dic['item_coupon'] = my_coupon_url  # 加入优惠券后的淘抢购链接
    dic['item_url'] = commodity_info['item_url']  # 商品链接
    dic['item_content'] = content  # 内容文案
    dic['item_image'] = commodity_info['pict_url']  # 图片
    dic['item_model'] = model  # 淘口令
    dic['item_location'] = commodity_info['provcity']  # 产地
    dic['item_volume'] = commodity_info['volume']  # 产量
    dic['item_cat_leaf_name'] = commodity_info['cat_leaf_name']  # 分类名字
    dic['item_cat_name'] = commodity_info['cat_name']  # 分类名字

    if my_coupon_info['coupon_total_count'] != 0:
        dic['coupon_amount'] = my_coupon_info['coupon_amount']  # 优惠额度
        dic['coupon_start_fee'] = my_coupon_info['coupon_start_fee']  # 满减条件
        dic['coupon_remain_count'] = my_coupon_info['coupon_remain_count']  # 剩余数量
        dic['coupon_total_count'] = my_coupon_info['coupon_total_count']  # 总量
        dic['coupon_start_time'] = my_coupon_info['coupon_start_time']  # 开始时间
        dic['coupon_end_time'] = my_coupon_info['coupon_end_time']  # 结束时间

    print_dic(dic)
    Loger.info('开始向django传输数据')
    post_info(post_url, dic, item_id)
    return dic


def print_dic(dic):
    for key in dic.keys():
        Loger.info((key, '-', dic[key]))


# 测试url是否需要跳转,获取跳转后链接 
def test_commodity(url):
    Loger.info(url)
    f_url = url[0:26]
    Loger.info(f_url)
    if f_url == 'https://s.click.taobao.com':
        url = tbk.get_true_url(url)
    return url
