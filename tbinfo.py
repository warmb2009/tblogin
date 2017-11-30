# -*- coding:utf-8 -*-

import re
from tbk.TbkSeniorAPI import *
from tbk.loggingset import create_logger
import requests
import json

Loger = create_logger()
postURL = 'http://127.0.0.1:8080/tkapis/'
tbk = tbk()

def postInfo(url, dic, itemID):
#    datas = json.dumps(dic)
    url = url #+ 'item_id=' + itemID + '/'
    r = requests.post(url, data = dic)
    print(r)
    Loger.info('post info')
    
# 正则表达式获取券链接和商品链接
def getCommodityInfo(text, pid):
    # 处理获取的信息
    matchObj = re.findall( r'(.*)领券(.*)抢购(.*https?://[ -~]+.*id=\d{11,12})(.*)', text)
    print(matchObj)
    if not matchObj:
        matchObj = re.findall( r'(.*)领券(.*)抢购(.*https?://[ -~]+[A-Za_z])(.*)', text)
        if not matchObj:
            return False

    link = matchObj[0]

    title = link[0].strip()
    price = ''
    couponURL = link[1].strip()[1:]#优惠券链接
    commodityURL = link[2].strip()[1:]#商品链接
    content = link[3].strip()
        
    # 测试商品链接并转换
    commodityURL = testCommodity(commodityURL)
        
    # 获取推广链接及商品图片 模拟登陆
    #    promotion_text, img_src = get(commodity)
    itemID = tbk.getItemID(commodityURL)
    
    # 将商品加入定向计划 调用全局变量, 传入商品url
    my_coupon_url = tbk.conver_url(couponURL, itemID, pid)
    # 通过api获取商品信息
    commodityInfo = tbk.getCommodityInfo(itemID)
    img_src = commodityInfo['pic']
    item_url = commodityInfo['item_url']
    location = commodityInfo['location']
    
    # 淘口令
    model = tbk.getTpwd(title, my_coupon_url)

    dic = {}
    dic['item_id'] = itemID
    dic['item_title'] = title
    # dic['item_price'] = price
    dic['item_coupon'] = my_coupon_url
    dic['item_url'] = item_url
    dic['item_content'] = content
    dic['item_image'] = img_src
    dic['item_model'] = model
    dic['item_location'] = location
    
    printdic(dic)
    postInfo(postURL, dic, itemID)
    return dic
    
def printdic(dic):
    for key in dic.keys():
        Loger.info((key, '-',dic[key]))

# 测试url是否需要跳转,获取跳转后链接 
def testCommodity(url):
    Loger.info(url)
    f_url = url[0:26]
    Loger.info(f_url)
    if f_url == 'https://s.click.taobao.com':
        url = tbk.getTrueURL(url)
    return url
